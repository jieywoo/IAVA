import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM
import numpy as np
import time
from configparser import ConfigParser

# @author Jieyeon Woo

###############################################################################
# ASAP model
# # Features from both Human & Agent (28 Features each)
# # Visual features: 3 head rotations & 7 AUs (6 Upperface AUs + AU12(Smile)) & 2 Gaze
# # # openface_feat_list = [' pose_Rx', ' pose_Ry', ' pose_Rz', ' AU01_r', ' AU02_r', ' AU04_r', ' AU05_r', ' AU06_r', ' AU07_r', ' AU12_r', ' gaze_angle_x', ' gaze_angle_y']
# # Audio features: 16 audio features
# # # opensmile_feat_list = ['voiceProb', 'F0env', 'loudness', 'mfcc[0]', 'mfcc[1]', 'mfcc[2]', 'mfcc[3]', 'mfcc[4]', 'mfcc[5]', 'mfcc[6]', 'mfcc[7]', 'mfcc[8]', 'mfcc[9]', 'mfcc[10]', 'mfcc[11]', 'mfcc[12]']
###############################################################################

# Input features (ALL visual and audio features = tot of 28 features; 12 visual & 16 audio for each)
IND_xij_U1V_rot = [i for i in range(0,3)]		
IND_xij_U1V_au = [i for i in range(3,3+7)]		
IND_xij_U1V_gaze = [i for i in range(3+7,3+7+2)]
IND_xij_U1V = np.concatenate((IND_xij_U1V_rot, IND_xij_U1V_au, IND_xij_U1V_gaze), axis=0)	# Head Rotation(x,y,z) + Upper AUs (1,2,4,5,6,7) + Smile(AU12) of U1
IND_xij_U1A = [i for i in range(12, 28)]
IND_xij_U1 = np.concatenate((IND_xij_U1V, IND_xij_U1A), axis=0)

IND_xij_U2V_rot = [i for i in range(28,28+3)]
IND_xij_U2V_au = [i for i in range(28+3,28+3+7)]
IND_xij_U2V_gaze = [i for i in range(28+3+7,28+3+7+2)]
IND_xij_U2V = np.concatenate((IND_xij_U2V_rot, IND_xij_U2V_au, IND_xij_U2V_gaze), axis=0)	# Head Rotation(x,y,z) + Upper AUs (1,2,4,5,6,7) + Smile(AU12) of U2
IND_xij_U2A = [i for i in range(28+12, 28+28)]
IND_xij_U2 = np.concatenate((IND_xij_U2V, IND_xij_U2A), axis=0)

IND_xij = np.concatenate((IND_xij_U1, IND_xij_U2), axis=0)

# Output features (ONLY visual features of Human)
IND_yij_U1V_rot = IND_xij_U1V_rot	
IND_yij_U1V_au = IND_xij_U1V_au
IND_yij_U1V_gaze = IND_xij_U1V_gaze
IND_yij_U1 = np.concatenate((IND_yij_U1V_rot, IND_yij_U1V_au, IND_yij_U1V_gaze), axis=0)

IND_yij_U2V_rot = [i for i in range(12,12+3)]
IND_yij_U2V_au = [i for i in range(12+3,12+3+7)]
IND_yij_U2V_gaze = [i for i in range(12+3+7,12+3+7+2)]
IND_yij_U2 = np.concatenate((IND_yij_U2V_rot, IND_yij_U2V_au, IND_yij_U2V_gaze), axis=0)

IND_yij = np.concatenate((IND_yij_U1, IND_yij_U2), axis=0)

# Model predicts the visual features of the agent for every frame
nb_inputs, nb_outputs = len(IND_xij), len(IND_yij_U1)

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
asap_config = config_object["ASAPCONFIG"]
in_seq_len = int(asap_config["inseqlen"])

class MultiHeadAttention(tf.keras.layers.Layer):
  def __init__(self, d_model, num_heads, causal=False, dropout=0.0):
    super(MultiHeadAttention, self).__init__()
    assert d_model % num_heads == 0
    depth = d_model // num_heads
    self.num_heads = num_heads
    self.w_query = tf.keras.layers.Dense(d_model)
    self.split_reshape_query = tf.keras.layers.Reshape((-1,num_heads,depth))  
    self.split_permute_query = tf.keras.layers.Permute((2,1,3))      
    self.w_value = tf.keras.layers.Dense(d_model)
    self.split_reshape_value = tf.keras.layers.Reshape((-1,num_heads,depth))
    self.split_permute_value = tf.keras.layers.Permute((2,1,3))
    self.w_key = tf.keras.layers.Dense(d_model)
    self.split_reshape_key = tf.keras.layers.Reshape((-1,num_heads,depth))
    self.split_permute_key = tf.keras.layers.Permute((2,1,3))
    self.attention = tf.keras.layers.Attention(causal=causal, dropout=dropout)
    self.join_permute_attention = tf.keras.layers.Permute((2,1,3))
    self.join_reshape_attention = tf.keras.layers.Reshape((-1,d_model))
    self.pruning = Dense(num_heads, activation='hard_sigmoid')
    self.split_permute_pruning = tf.keras.layers.Permute((3,2,1))
    self.dense = tf.keras.layers.Dense(d_model)

  def call(self, inputs, mask=None, training=None, pruning=False):
    q = inputs[0]
    v = inputs[1]
    k = inputs[2] if len(inputs) > 2 else v
    query = self.w_query(q)
    query = self.split_reshape_query(query)    
    query = self.split_permute_query(query)
    value = self.w_value(v)
    value = self.split_reshape_value(value)
    value = self.split_permute_value(value)
    key = self.w_key(k)
    key = self.split_reshape_key(key)
    key = self.split_permute_key(key)

    if mask is not None:
      if mask[0] is not None:
        mask[0] = tf.keras.layers.Reshape((-1,1))(mask[0])
        mask[0] = tf.keras.layers.Permute((2,1))(mask[0])
      if mask[1] is not None:
        mask[1] = tf.keras.layers.Reshape((-1,1))(mask[1])
        mask[1] = tf.keras.layers.Permute((2,1))(mask[1])

    attention = self.attention([query, value, key], mask=mask)
    
    if pruning:
      # Pruning attention heads
      pruning_mask = self.pruning(self.split_permute_pruning(attention))
      pruning_mask = tf.round(pruning_mask)
      pruning_mask = self.split_permute_pruning(pruning_mask)
      attention = attention*pruning_mask

    attention = self.join_permute_attention(attention)
    attention = self.join_reshape_attention(attention)

    x = self.dense(attention)

    return x

def build_model(params_model):
    cell_lstm = params_model["cell_lstm"]
    cell_dense = params_model["cell_dense"]
    cell_att = params_model["cell_multiheadatt"]
    num_head_att = params_model["num_head_multiheadatt"]
    pruning_stat = params_model["pruning_stat"]

    inputs = keras.layers.Input(shape=(in_seq_len, nb_inputs))

    # Self-Attention using Multi-head-Attention of inputs
    mha = MultiHeadAttention(d_model=cell_att,num_heads=num_head_att)
    x = mha([inputs,inputs,inputs], pruning=pruning_stat)

    x = LSTM(cell_lstm, input_shape=(in_seq_len, nb_inputs))(x)
    x = Dense(cell_dense, activation='relu')(x)

    # U1 Only
    output_RotXYZ = Dense(3, activation='linear', name='RotXYZ')(x)
    output_au1_intensity = Dense(1, activation='relu', name='AU1_int')(x)
    output_au2_intensity = Dense(1, activation='relu', name='AU2_int')(x)
    output_au4_intensity = Dense(1, activation='relu', name='AU4_int')(x)
    output_au5_intensity = Dense(1, activation='relu', name='AU5_int')(x)
    output_au6_intensity = Dense(1, activation='relu', name='AU6_int')(x)
    output_au7_intensity = Dense(1, activation='relu', name='AU7_int')(x)
    output_au12_intensity = Dense(1, activation='relu', name='AU12_int')(x)
    output_GazeXY = Dense(2, activation='linear', name='GazeXY')(x)

    output_RotX = tf.identity(output_RotXYZ[:,0], name="RotX")
    output_RotY = tf.identity(output_RotXYZ[:,1], name="RotY")
    output_RotZ = tf.identity(output_RotXYZ[:,2], name="RotZ")
    output_GazeX = tf.identity(output_GazeXY[:,0], name="GazeX")
    output_GazeY = tf.identity(output_GazeXY[:,1], name="GazeY")
    
    output_list = [output_RotX, output_RotY, output_RotZ,\
                   output_au1_intensity, output_au2_intensity, output_au4_intensity, output_au5_intensity, output_au6_intensity, output_au7_intensity, output_au12_intensity,\
                   output_GazeX, output_GazeY]
    
    model = Model(inputs=inputs, outputs=output_list)

    return model


def singleRun_ASAP(model, xij_prev_t, agent_U1V_pred_t, agent_U1A_t, user_U2V_t, user_U2A_t, print_time=False):
    # Use previous prediction as input (rot and au of Agent)
    if (print_time):
      tic_asap = time.time()

    xij_prev_t = np.delete(xij_prev_t, [0], axis=0)
    agent_t = np.concatenate((agent_U1V_pred_t, agent_U1A_t))
    user_t = np.concatenate((user_U2V_t, user_U2A_t))
    xij_new_t = np.concatenate((user_t, agent_t))
    xij_new_t = np.reshape(xij_new_t,(1,len(xij_new_t)))
    xij_t = np.vstack((xij_prev_t,xij_new_t))
    xij_t_in = np.reshape(xij_t,(1,xij_t.shape[0],xij_t.shape[1]))
    agent_U1V_pred_new_t = model.predict_on_batch(xij_t_in)
    agent_U1V_pred_new_t[:len(IND_yij_U1V_rot)] = [pred[0] for pred in agent_U1V_pred_new_t[:len(IND_yij_U1V_rot)]]
    agent_U1V_pred_new_t[len(IND_yij_U1V_rot):len(IND_yij_U1V_rot)+len(IND_yij_U1V_au)] = [pred[0,0] for pred in agent_U1V_pred_new_t[len(IND_yij_U1V_rot):len(IND_yij_U1V_rot)+len(IND_yij_U1V_au)]]
    agent_U1V_pred_new_t[len(IND_yij_U1V_rot)+len(IND_yij_U1V_au):] = [pred[0] for pred in agent_U1V_pred_new_t[len(IND_yij_U1V_rot)+len(IND_yij_U1V_au):]]
    
    if (print_time):
      toc_asap = time.time()
      print("asap time:", toc_asap-tic_asap)

    return xij_t, np.array(agent_U1V_pred_new_t)
