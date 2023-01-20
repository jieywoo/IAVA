# Greta ASAP integration

The Greta ASAP integration is a part of the ASAP-Greta module which needs to be integrated interally to the Greta platform.\
It receives the generated generated agent's nonverbal features of the ASAP model for every frame (from the real-time ASAP system) and displays them via the Greta virtual agent.

## Requirements:
 - Greta platform: [GRETA GITHUB](https://github.com/isir/greta)

## Configuration:
The configuration file of the system is: "Greta-ASAP-Cereproc.xml".

![asap-greta_config_asap](https://user-images.githubusercontent.com/44306168/213601696-225e9a5e-6d93-46ef-a9c0-b6b182e884b8.png)

The generated agent's nonverbal features can be selected to be visualized or not via an interactive window.

![asap-greta_window](https://user-images.githubusercontent.com/44306168/213602148-510a2438-47eb-4afe-b230-5b45888fa4b8.png)

## ASR & Flipper2.0 Feedback
Additional functionalities were added to the configuration file which is: "Greta - ASR ASAP.xml".\
They were added in order to allow the Greta virtual agent to interact with the user automatically.

The user speech is transcripted for every phrase using an Automatic Speech Recognition (ASR) system and the phrase transcript is passed to the Greta platform via ActiveMQ. The phrase transcript can be used to select the next phrase that will be said by the agent. After verifying that the user has terminated to speak, the Greta agent speaks the prescripted speech (while also verifying that its previous speech has been terminated).

![asap-greta_config](https://user-images.githubusercontent.com/44306168/213603260-4ef7439b-2033-4632-a066-78eb75ee2051.png)

The new fuctionalities includes:
 - Automatic Speech Recognition (ASR): [GRETA ASR](https://github.com/isir/greta/wiki/ASR-Flipper2.0-MeaningMiner-Integration-Demo)\
 Sending the phrase transcript of the user's speech obtained via ASR to the Greta platform. 
 - Feedback module of Flipper2.0: [GRETA ASR](https://github.com/isir/greta/wiki/ASR-Flipper2.0-MeaningMiner-Integration-Demo)\
 Verifying wheither the Greta agent has finished talking its previous speech before launching the next one.
 
 A scenario script can be written with the aforementionned functionalities in: [project location]\bin\Common\Data\FlipperResources\templates".
 

## Flipper2.0 - External program Link
 Another functionality that we have added is the link established between the Greta platform's Flipper2.0 module and an external python program.\
 For our research use, we have linked a pretrained automatic thought classifier model for our Cognitive Behavioral Therapy (CBT) scenario.\
 The passed user speech transcript is passed to the automatic thought classifier (when activated) which computes if it is an automatic thought or not. The next scenario phrase is selected and spoken depending on this result.\
 This part can be easily modified and applied to any other scenario that requires the result of an external program.
 
 ## Instructions:
To start, the components must be added to the Greta platform.
 - "asap" directory -> "[project location]\auxiliary\ASAP\src\greta\auxiliary"
 - "ASAPServer.java" -> "[project location]\core\Intentions\src\greta\core\intentions"
 - "ASAPSimpleAUPerformer.java" -> "[project location]\core\Signals\src\greta\core\keyframes\face"
 - "CharacterManager.java" -> "[project location]\core\Util\src\greta\core\util"
 - "Speech.java" -> "[project location]\core\Util\src\greta\core\util\speech"
 - "Audio.java" -> "[project location]\core\Util\src\greta\core\util\audio"
 - "build.xml" -> "[project location]\auxiliary\ASAP" 
 - "build-impl.xml" -> "[project location]\auxiliary\ASAP\nbproject"
 - "project.properties.xml" -> "[project location]\auxiliary\ASAP\nbproject"
 - "project.xml" -> "[project location]\auxiliary\ASAP\nbproject"
 
The configuration files ("Greta-ASAP-Cereproc.xml" and "Greta - ASR ASAP.xml") in the "configurations" directory must also be included in: "[project location]\bin\Configurations\Greta".

After the verification of the inclusion of all files, the system can be executed.\
Launching the Greta platform with one of the configuration files.

### "Greta-ASAP-Cereproc.xml"
A pop-up window of ASAP will be shown. Launch the socket connection after entering your IP address (please leave the port number as it is).

### "Greta - ASR ASAP.xml"
After opening the configuration file, start by opening the ASR window. Using the Google Chrome navigator (in an incognito window), launch the ASR system.\
After like the previous configuration, launch the socket connection after entering your IP address (please leave the port number as it is).

For both configurations, the whole system starts working when the real-time ASAP system is launched. Please follow the real-time ASAP system instructions [realtimeASAP instructions](https://github.com/jieywoo/ASAP-Greta/blob/main/realtimeASAP/README.md).

