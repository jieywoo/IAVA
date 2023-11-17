import soundfile as sf
import numpy as np

# @author Jieyeon Woo

###############################################################################
# Retransform saved audio data csv to wav audio file
###############################################################################

fs = 44100
rec2wav = np.genfromtxt('userAudio_asnumpy.csv', delimiter=',')
sf.write('recording_userAudio.wav', rec2wav, fs)
