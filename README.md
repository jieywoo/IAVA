# Interactive and Adaptive Virtual Agent (IAVA)
Code of Interactive and Adaptive Virtual Agent (IAVA) system, IVA 2023.\
Full Paper: "IAVA: Interactive and Adaptive Virtual Agent" [IVA 2023].\
Demo Paper: "Conducting Cognitive Behavioral Therapy with an Adaptive Virtual Agent" [IVA 2023].

## Description of IAVA
IAVA is an interactive virtual agent system that generates real-time adaptive behaviors in response to its human interlocutor.\
It ensures the two aspects:
- generating real-time adaptive behavior,
- managing natural dialogue.

The agent adapts to its interlocutor linguistically (choosing its next conversational move via the dialogue manager including a LLM-based automatic thought classifier) and nonverbally (displaying reciprocally adaptive facial gestures via the [ASAP](https://github.com/jieywoo/ASAP/tree/main) model).

Cognitive Behavioral Therapy (CBT) is chosen as our proof-of-concept, the agent acts as a therapist helping human users detect their negative automatic thoughts.

## Demo video
A dyadic interaction between a human user and an adaptive CBT agent simulated via our IAVA system. The system loop consisting of user multimodal signal perception, agent behavior generation, signal communication, and visualization is assured to the frame level of 25 fps.

[![IAVA DEMO](https://github.com/jieywoo/IAVA/assets/44306168/a4cea035-26f4-4574-ad81-9b3145cfaa98)](http://www.youtube.com/watch?v=9aZeSUxhf60)
Please click to see the full demo video.

## CBT-HAI Database
A database of 60 CBT human-agent interactions has been collected using the IAVA system.\
<img src="https://github.com/jieywoo/IAVA/assets/44306168/6ae520d3-b78e-4a77-a0fb-f9d03399a52f" alt="drawing" width="200"/>

If you are interested in the CBT HAI DB, please contact the authors of the IAVA system.

## Instructions
IAVA consists of 2 main modules:
- [Perception and Generation (PerceptNGen)](https://github.com/jieywoo/IAVA/tree/main/PerceptNGen): computes the user multimodal signal perception and the agent behavior generation (via ASAP model) in real-time and sends the agent's nonverbal generations to the Greta platform for the display,
- [IAVA for Greta (IAVA4Greta)](https://github.com/jieywoo/IAVA/tree/main/IAVA4Greta): contains IAVA elements of real-time signal communication and visualization which needs to be integrated into the Greta platform ([Greta Main GITHUB](https://github.com/isir/greta/tree/gpl-grimaldi)).

Each section will be detailed in the sub-readme files within each part's directory.

### Integration
Please follow the integration instructions in each sub-readme file.

## Usage guide
To use the system, please follow the following instructions:
1. Launch OpenFace streaming with ZeroMQ.\
   Select the "Record" options of :
    - Record AUs
    - Broadcast with ZeroMQ (port 5000)
    - Record pose
    - Record gaze
  ![openfacezmq](https://user-images.githubusercontent.com/44306168/223973351-1009bc81-34be-4747-83e2-4436a509ce5d.png)
2. Launch Greta platform and open one of the following configuration files:
    - "Greta-IAVA-Cereproc.xml":\
    Using the pop-up window of IAVA, launch the socket connection (with the "Enable" button) after entering your IP address (please leave the port number as it is).
    ![greta_socket](https://user-images.githubusercontent.com/44306168/223976415-0fa9620e-a079-4f30-b11f-0f2f82453be9.PNG)
    - "Greta - ASR IAVA.xml":
    The operation with ASR is done in two steps:
      1. Start by opening the ASR window. Using the Google Chrome navigator (in an incognito window), launch the ASR system with: *https://127.0.0.1:8087*
      ![greta_asr](https://user-images.githubusercontent.com/44306168/223978045-69ed7bb4-9570-46fc-bb4a-a664fd62c9f1.PNG)
      2. Using the pop-up window of IAVA, launch the socket connection (with the "Enable" button) after entering your IP address (please leave the port number as it is).
      Please refer to the image above for "Greta-IAVA-Cereproc.xml".
3. Launch real-time IAVA system:
    Start by changing the socket connection configurations by entering your IP addresses (please leave the port number as it is) in: *config.ini* 
    
    Run the system using the main script of "realtime_PerceptNGen.py" with:
    ```
    python realtime_PerceptNGen.py
    ```
    After closing the system program, the following output CSV files will be available (detailed in the [realtimeASAP sub-readme](https://github.com/jieywoo/IAVA/blob/main/PerceptNGen/README.md)):
        - Audio signals of the user
        - OpenFace and openSMILE features of the user and agent
    
##
*The original code for the ASAP model can be found here: [ASAP GITHUB](https://github.com/jieywoo/ASAP)*
