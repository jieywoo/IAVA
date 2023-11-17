import soundfile as sf
import numpy as np

fs = 44100
rec2wav = np.genfromtxt('userAudio_asnumpy.csv', delimiter=',')
print(rec2wav.shape)
sf.write('recording_userAudio.wav', rec2wav, fs)

#61740