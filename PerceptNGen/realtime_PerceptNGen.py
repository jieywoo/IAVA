from ASAP import build_model, singleRun_ASAP
from smoothingFilter import leastSquareFilter
import numpy as np
import sys
import time
import zmq
import socket
import opensmile
import sounddevice as sd
from scipy.io.wavfile import write
import select
import queue
import pickle
from threading import Thread, Event
from configparser import ConfigParser

# @author Jieyeon Woo

# Options
save_data = True
save_raw_audio = True
smooth_data = True

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# ASAP model configurations & parameters
asap_config = config_object["ASAPCONFIG"]
in_seq_len = int(asap_config["inseqlen"])
nb_inputs = int(asap_config["nbinputs"])
nb_outputs = int(asap_config["nboutputs"])
path_pretrained_model = asap_config["modelpath"]
asap_param = config_object["ASAPPARAM"]
d_mha = int(asap_param["dmha"])
nb_h_mha = int(asap_param["nbhmha"])
pruning_state = asap_param["pruning"] == "True"
d_lstm = int(asap_param["dlstm"])
d_dense = int(asap_param["ddense"])

# Real-time data smoothing
if smooth_data:
	smoothing_config = config_object["SMOOTHINGCONFIG"]
	nb_smoothdata = int(smoothing_config["nbsmoothdata"])
	list_str_window_size = smoothing_config["windowsize"].split(',')
	list_window_size = [int(x) for x in list_str_window_size]
	list_str_filter_idx_size = smoothing_config["filteridxsize"].split(',')
	list_filter_idx_size = [int(x) for x in list_str_filter_idx_size]
	agent_U1V_pred_ts = np.zeros((nb_smoothdata,nb_outputs), dtype=float)

# IPs & Ports
socket_param = config_object["SOCKETCONFIG"]
ip_lis = socket_param["iplis"]
port_lis = int(socket_param["portlis"])
ip_send = socket_param["ipsend"]
port_send = int(socket_param["portsend"])
address_send = (ip_send, port_send)

# Opensmile parameters
opensmile_param = config_object["OPENSMILEPARAM"]
fs = int(opensmile_param["fs"])
seconds = float(opensmile_param["sec"])
feat_set = opensmile_param["featset"]
feat_lvl = opensmile_param["featlvl"]
smile = opensmile.Smile(
	feature_set=feat_set,
	feature_level=feat_lvl,
)

# Params for Model
params_model = {'cell_multiheadatt' : d_mha,
				'num_head_multiheadatt' : nb_h_mha,
				'pruning_stat' : pruning_state,
				'cell_lstm' : d_lstm,
				'cell_dense' : d_dense,
				}

model = build_model(params_model)

# Load pretrained weights
model.load_weights(path_pretrained_model)

# Declaration & Initialization of variables
xij_prev_t = np.zeros((in_seq_len,nb_inputs), dtype=float)
agent_U1V_pred_t = np.zeros((nb_outputs), dtype=float)
user_U2V_t = np.zeros((nb_outputs), dtype=float)
agent_U1A_t = np.zeros((int((nb_inputs-nb_outputs*2)/2)), dtype=float)
user_U2A_t = np.zeros((int((nb_inputs-nb_outputs*2)/2)), dtype=float)
q_audio = queue.Queue()
timestep = 0.
timestep_t = np.zeros((1))
real_timestep = 0.04
real_timestep_t = np.zeros((1))
tic_asap = 0.

# Socket connections
# ZMQ connection for openface
context = zmq.Context()
print("Connecting to zmq server")
socket_zmq = context.socket(zmq.SUB)
socket_zmq.connect("tcp://localhost:5000")
socket_zmq.setsockopt(zmq.SUBSCRIBE, b'')

# Listening for Agent's opensmile features from Greta
s_lis = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_lis.bind((ip_lis,port_lis))
# Sending next Agent's behavior to Greta
s_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_send.connect(address_send)


# Save data option: create file to save data
if save_data:
	# User raw audio signal to csv (later convert csv_numpy data to wav: use recnumpy2wav.py)
	if save_raw_audio:
		with open("userAudio_asnumpy.csv", "w") as my_empty_csv:
			pass
		user_rawaudio_csvfile=open('userAudio_asnumpy.csv','a')
	# (Timestep, User openface,User opensmile,Agent openface,Agent opensmile) signal to csv
	with open("userNagentOFOSdata.csv", "w") as my_empty_csv:
		pass
	save_OSOF_csvfile=open('userNagentOFOSdata.csv','a')
	
# Audio callback function for input audio stream
def audio_callback(indata, frames, time, status):
	global q_audio
	signal = indata.copy()
	if save_data:
		# Save/append user raw audio signal to csv every 0.04s(later convert csv_numpy to wav file)
		np.savetxt(user_rawaudio_csvfile, signal, delimiter=',')
	q_audio.put(signal)

# Get openface features of the human user in real-time
def openface_user():
	global user_U2V_t, socket_zmq
	while True:
		#openface zmq
		openface_msg=socket_zmq.recv().decode("utf-8") 

		# openface message received as (b'data, frame, face_id, timestamp, confidence, success, 3 gaze0_pose, 3 gaze1_pose, gaze_angle_x, gaze_angle_y, 3 head_pose, 3 head_rot, 17 AU_intensity, 17 AU_activ)
		openface_idx_list = [16,17,18,19,20,21,22,23,24,27,11,12] # Head Rot, AU, Gaze
		openface_msg_list = openface_msg.split(",")

		user_U2V_wParamName = [openface_msg_list[msg] for msg in openface_idx_list]
		if user_U2V_wParamName[0] != 'pose_Rx':
			user_U2V_t = [float(x) for x in user_U2V_wParamName]
			user_U2V_t = [0 if x<0 else x for x in user_U2V_t] # Force egative to zero

# Get opensmile features of the human user in real-time
def opensmile_user():
	global user_U2A_t, q_audio
	stream = sd.InputStream(callback=audio_callback, blocksize=int(fs*0.04))
	with stream:
		while True:
			# get audio signal
			signal = q_audio.get()
			rec = np.reshape(signal, (1,-1))
			user_U2A_t = smile.process_signal(rec, fs).mean().values.tolist()

# Get opensmile features of the agent received by Greta in real-time
def opensmile_agent():
	global agent_U1A_t, s_lis
	while True:
		s_lis.setblocking(0)
		ready = select.select([s_lis], [], [], seconds)
		if ready[0]:
			data, address = s_lis.recvfrom(1024)
			agent_U1A_t = pickle.loads(data).tolist()
		else:
			agent_U1A_t = [0]*int((nb_inputs-nb_outputs*2)/2)

# Compute ASAP with features obtained in real-time
def compute_ASAP():
	global xij_prev_t, agent_U1V_pred_t, agent_U1A_t, user_U2V_t, user_U2A_t, timestep, real_timestep, timestep_t, real_timestep_t, s_send, tic_asap, save_OSOF_csvfile
	while True:
		xij_prev_new_t, agent_U1V_pred_new_t = singleRun_ASAP(model, xij_prev_t, agent_U1V_pred_t, agent_U1A_t, user_U2V_t, user_U2A_t)
		xij_prev_t = xij_prev_new_t
		# Denormalization of AUs
		agent_U1V_pred_new_t[3:-2] = [au*2.75 for au in agent_U1V_pred_new_t[3:-2]]
		# Adapt intensity of HeadRot
		agent_U1V_pred_new_t[:3] = [rot*0.5 for rot in agent_U1V_pred_new_t[:3]]
		# Adapt intensity of Gaze
		agent_U1V_pred_new_t[-2:] = [gaze*0.5 for gaze in agent_U1V_pred_new_t[-2:]]
		
		if smooth_data:
			# Smoothing - LeastSquares-Filter
			agent_U1V_pred_ts[:-1,:] = agent_U1V_pred_ts[1:,:]
			agent_U1V_pred_ts[-1,:] = agent_U1V_pred_new_t
			agent_U1V_pred_t = leastSquareFilter(agent_U1V_pred_ts, list_window_size, list_filter_idx_size)
		else:
			agent_U1V_pred_t = agent_U1V_pred_new_t
		

		# convert to openface feature list before sending to Greta
		timestamp = [timestep]
		gaze01_openface_format = [0]*6
		gaze = agent_U1V_pred_t[-2:]
		poseT_openface_format = [0]*3
		headrot = agent_U1V_pred_t[:3]
		au1_7 = agent_U1V_pred_t[3:-3]
		au9_10_openface_format = [0]*2
		au12 = [agent_U1V_pred_t[-3]]
		au14_45_openface_format = [0]*8
	
		agent_openface_format = []
		agent_openface_format.extend(timestamp)
		agent_openface_format.extend(gaze01_openface_format)
		agent_openface_format.extend(gaze)
		agent_openface_format.extend(poseT_openface_format)
		agent_openface_format.extend(headrot)
		agent_openface_format.extend(au1_7)
		agent_openface_format.extend(au9_10_openface_format)
		agent_openface_format.extend(au12)
		agent_openface_format.extend(au14_45_openface_format)

		#Send prediction to Greta
		msg_agent_U1V_pred_t = [str(x) for x in agent_openface_format]
		msg_agent_U1V_pred_t = ','.join(msg_agent_U1V_pred_t) + '\r\n'
		s_send.sendto(msg_agent_U1V_pred_t.encode('utf-8'),address_send)

		timestep += 0.04
		timestep_t = [timestep]

		toc_asap = time.time()
		single_loop_time = toc_asap-tic_asap
		tic_asap = time.time()
		if single_loop_time < 100:
			real_timestep += single_loop_time
		print("single loop time:", single_loop_time)
		print("real accumulated time:", real_timestep)
		real_timestep_t = [real_timestep]

		# Adjust speed (25 fps)
		if ((timestep-real_timestep) > 0):
			time.sleep(timestep-real_timestep)

		if save_data:
			# Save/append signals (timestep, user OF, user OS, agent OF, agent OS) to csv every 0.04s
			np.savetxt(save_OSOF_csvfile, [np.concatenate((timestep_t,real_timestep_t,user_U2V_t, user_U2A_t, agent_U1V_pred_t, agent_U1A_t),axis=0)], delimiter=',')

	
if __name__ == "__main__":
	t_ofu = Thread(target=openface_user)
	t_osu = Thread(target=opensmile_user)
	t_osa = Thread(target=opensmile_agent)
	t_asap = Thread(target=compute_ASAP)

	t_ofu.start()
	t_osu.start()
	t_osa.start()
	t_asap.start()

