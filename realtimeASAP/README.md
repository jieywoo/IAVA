# Real-time ASAP system

The real-time ASAP system is a part of the ASAP-Greta module.\
It computes the ASAP model for every frame and passes the generated agent's nonverbal features to the Greta platform for display.

## Requirements
- OpenFace extracting user's visual features (AUs, pose, gaze) streaming in real-time via ZeroMQ;
- Greta platform executing with the configuration of "Greta-ASAP-Cereproc.xml" or "Greta - ASR ASAP.xml";
- Environment requirements:
  - Python 3.9.7
  - Tensorflow 2.4.1
  - numpy 1.23.5
  - scipy 1.4.1
  - zeromq 4.3.3
  - sounddevice 0.4.4
  - soundfile 0.10.3.post1
  - opensmile 2.4.1

## Scripts
- "realtime_ASAP.py": main script to compute ASAP and communicate with the Greta platform in real-time;
- "ASAP.py": ASAP model functions;
- "smoothingFilter.py": smoothing filter function;
- "recnumpy2wav.py": converts recorded audio signals to a WAV file.

## Configuration files
- "config.ini": main configuration file (Socket connection configs of IP and port, ASAP model configs, openSMILE parameters);
- "opensmile_realtime.conf": configuration of openSMILE.

## Pretrained model
- "ASAP_pretrainedWeights.hdf5": pretrained weights of ASAP model.

## Outputs
"realtime_ASAP.py" renders 2 output CSV files.
It records the audio signals of the user along with OpenFace and openSMILE features extracted from the user and agent for each frame (every 0.04s). 

- "userAudio_asnumpy.csv":
record the audio signals of the user and can be converted in WAV file using "recnumpy2wav.py"

- "userNagentOFOSdata.csv":
record OpenFace and openSMILE features of the user and agent with features listed in the order of:
  - [timestamp, userOF, userOS, agentOF, agentOS] where:
    - OF: [' pose_Rx', ' pose_Ry', ' pose_Rz', ' AU01_r', ' AU02_r', ' AU04_r', ' AU05_r', ' AU06_r', ' AU07_r', ' AU12_r', ' gaze_angle_x', ' gaze_angle_y']
    - OS: ['voiceProb', 'F0env', 'loudness', 'mfcc[0]', 'mfcc[1]', 'mfcc[2]', 'mfcc[3]', 'mfcc[4]', 'mfcc[5]', 'mfcc[6]', 'mfcc[7]', 'mfcc[8]', 'mfcc[9]', 'mfcc[10]', 'mfcc[11]', 'mfcc[12]']

## Usage guide
To run the real-time ASAP system, OpenFace and the Greta platform must be running before launching the main script of "realtime_ASAP.py".

Start by changing the socket connection configurations by entering your IP addresses (please leave the port number as it is) in: *config.ini*\
After launching the ASAP socket communication within the Greta platform, run the system.

To run the system, run with:
```
python realtime_ASAP.py
```

After closing the system program, the output CSV files will be available.

