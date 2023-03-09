# ASAP-Greta
ASAP-Greta module (awaiting to be integrated into isir/greta)

The ASAP-Greta module consists of two parts:
- realtimeASAP: computes the ASAP model in real-time and sends agent's nonverbal generations to the Greta platform for the display.
- gretaASAP: contains ASAP-Greta module elements which needs to be integrated into the Greta platform

Each section will be detailed in the sub-readme files within each part's directory.

## Integration
Please follow the integration instruction in each sub-readme files.

## Usage guide
To use the system, please follow in following instruction:
1. Launch OpenFace streaming with ZeroMQ. Select the "Record" options of :
    - Record AUs
    - Broadcast with ZeroMQ (port 5000)
    - Record pose
    - Record gaze
  ![openfacezmq_asap](https://user-images.githubusercontent.com/44306168/223973351-1009bc81-34be-4747-83e2-4436a509ce5d.png)
2. Launch Greta platform and open one of the following configuration files:
    - "Greta-ASAP-Cereproc.xml":
    Using the pop-up window of ASAP, launch the socket connection (with the "Enable" button) after entering your IP address (please leave the port number as it is).
    ![greta_socket_asap](https://user-images.githubusercontent.com/44306168/223976415-0fa9620e-a079-4f30-b11f-0f2f82453be9.PNG)
    - "Greta - ASR ASAP.xml":
    The opertation with ASR is done in two steps:
      1. Start by opening the ASR window. Using the Google Chrome navigator (in an incognito window), launch the ASR system with: *https://127.0.0.1:8087*
      ![greta_asr_asap](https://user-images.githubusercontent.com/44306168/223978045-69ed7bb4-9570-46fc-bb4a-a664fd62c9f1.PNG)
      2. Using the pop-up window of ASAP, launch the socket connection (with the "Enable" button) after entering your IP address (please leave the port number as it is).
      Please refer to the image above for "Greta-ASAP-Cereproc.xml".
3. Launch real-time ASAP system:
  
  To complete
  


##
*The original code for the ASAP model can be found here: [ASAP GITHUB](https://github.com/jieywoo/ASAP)*
