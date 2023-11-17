# IAVA for Greta (IAVA4Greta)

The IAVA for Greta (IAVA4Greta) of the IAVA system which needs to be integrated internally into the Greta platform.\
It receives the generated agent's nonverbal features of the ASAP model for every frame (from the Perception and Generation (PerceptNGen) module) and displays them via the Greta virtual agent.

## Requirements:
 - Greta platform: [GRETA GITHUB](https://github.com/isir/greta)

## Configuration:
The configuration file of the system is: "Greta-IAVA-Cereproc.xml".

![IAVA_config](https://user-images.githubusercontent.com/44306168/213601696-225e9a5e-6d93-46ef-a9c0-b6b182e884b8.png)

The generated agent's nonverbal features can be selected to be visualized or not via an interactive window.

![IAVA_window](https://user-images.githubusercontent.com/44306168/213602148-510a2438-47eb-4afe-b230-5b45888fa4b8.png)

## ASR & Flipper2.0 Feedback
Additional functionalities were added to the configuration file which is: "Greta - ASR IAVA.xml".\
They were added in order to allow the Greta virtual agent to interact with the user automatically.

The user speech is transcripted for every phrase using an Automatic Speech Recognition (ASR) system and the phrase transcript is passed to the Greta platform via ActiveMQ. The phrase transcript can be used to select the next phrase that will be said by the agent. After verifying that the user has been terminated to speak, the Greta agent speaks the prescripted speech (while also verifying that its previous speech has been terminated).

![IAVA_config](https://user-images.githubusercontent.com/44306168/213603260-4ef7439b-2033-4632-a066-78eb75ee2051.png)

New functionalities include:
 - Automatic Speech Recognition (ASR): [GRETA ASR](https://github.com/isir/greta/wiki/ASR-Flipper2.0-MeaningMiner-Integration-Demo)\
 Sending the phrase transcript of the user's speech obtained via ASR to the Greta platform. 
 - Feedback module of Flipper2.0: [GRETA Flipper2.0](https://github.com/isir/greta/wiki/ASR-Flipper2.0-MeaningMiner-Integration-Demo)\
 Verifying whether the Greta agent has finished talking its previous speech before launching the next one.
 
 A scenario script can be written with the aforementioned functionalities in the "templates" directory: \
 "[project location]\bin\Common\Data\FlipperResources\templates".

## CBT Automatic Thought Classifier (ATcls)
 For the Cognitive Behavioral Therapy (CBT) scenario, we built a French BERT-based (LLM-based) automatic thought classifier (ATcls) model based on [Shidara+2022](https://www.frontiersin.org/articles/10.3389/fcomp.2022.762424/full)'s work to identify if the user's utterance is an automatic thought. The ATcls renders a binary result indicating whether the user utterance is an automatic thought or not.

 The same CBT scenario, translated and culturally adapted into French, was used as in the work of [Shidara+2022](https://www.frontiersin.org/articles/10.3389/fcomp.2022.762424/full).\
 The French CBT scenario can be found in the "fmltemplates" directory:
 "[project location]\bin\Common\Data\FlipperResources\fmltemplates"
 
## Flipper2.0 - External Program (CBT ATcls) Link
 Another functionality that we have added is the link established between the Greta platform's Flipper2.0 module and an external python program.\
 For our research use, we have linked a pretrained automatic thought classifier (ATcls) model for our Cognitive Behavioral Therapy (CBT) scenario.\
 The passed user speech transcript is passed to the automatic thought classifier (when activated) which computes if it is an automatic thought or not. The next scenario phrase is selected and spoken depending on this result.\
 This part can be easily modified and applied to any other scenario that requires the result of an external program.
 
 The scripts of the external program can be placed in: \
 "[project location]\bin\Scripts".
 
 ## Integration instructions:
To start, the components must be added to the Greta platform.
 - "iava" directory -> "[project location]\auxiliary\IAVA\src\greta\auxiliary"
 - "IAVAServer.java" -> "[project location]\core\Intentions\src\greta\core\intentions"
 - "IAVASimpleAUPerformer.java" -> "[project location]\core\Signals\src\greta\core\keyframes\face"
 - "CharacterManager.java" -> "[project location]\core\Util\src\greta\core\util"
 - "Speech.java" -> "[project location]\core\Util\src\greta\core\util\speech"
 - "Audio.java" -> "[project location]\core\Util\src\greta\core\util\audio"
 - "ASRInputManager.java" -> "[project location]\auxiliary\DialogueManager\FlipperDemoExample\src\greta\FlipperDemo\input"
 - "FeedbackReceiver.java" -> "[project location]\auxiliary\DialogueManager\FlipperDemoExample\src\greta\FlipperDemo\input"
 - "FeedbackManager.java" -> "[project location]\auxiliary\DialogueManager\FlipperDemoExample\src\greta\FlipperDemo\input"
 - "build.xml" -> "[project location]\auxiliary\IAVA" 
 - "build-impl.xml" -> "[project location]\auxiliary\IAVA\nbproject"
 - "project.properties.xml" -> "[project location]\auxiliary\IAVA\nbproject"
 - "project.xml" -> "[project location]\auxiliary\IAVA\nbproject"
 - "Scripts" directory -> "[project location]\bin"
 - "fmltemplates" directory -> "[project location]\bin\Common\Data\FlipperResources"
 - "templates" directory -> "[project location]\bin\Common\Data\FlipperResources"
 
The configuration files ("Greta-IAVA-Cereproc.xml" and "Greta - ASR IAVA.xml") in the "configurations" directory must also be included in: "[project location]\bin\Configurations\Greta".

## Usage guide:
After the verification of the inclusion of all files, the system can be executed.\
Launching the Greta platform with one of the configuration files.

### "Greta-IAVA-Cereproc.xml"
A pop-up window of IAVA will be shown. Launch the socket connection after entering your IP address (please leave the port number as it is).

### "Greta - ASR IAVA.xml"
After opening the configuration file, start by opening the ASR window. Using the Google Chrome navigator (in an incognito window), launch the ASR system.\
After like the previous configuration, launch the socket connection after entering your IP address (please leave the port number as it is).

For both configurations, the whole system starts working when the PerceptNGen module is launched. Please follow the [PerceptNGen module instructions](https://github.com/jieywoo/IAVA/blob/main/PerceptNGen/README.md).

