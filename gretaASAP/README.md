# Greta ASAP integration

The Greta ASAP integration is a part of the ASAP-Greta module which needs to be integrated interally to the Greta platform.\
It receives the generated generated agent's nonverbal features of the ASAP model for every frame (from the real-time ASAP system) and displays them via the Greta virtual agent.

## Requirements:
 - Greta platform: [GRETA GITHUB](https://github.com/isir/greta)

## Configuration:
The configuration file of the system is "Greta - ASR ASAP.xml".
![Alt text](/ASAP-Greta/gretaASAP/img/asap-greta_config_asap.png "Configuration of ASAP-Greta module")

## Instructions:
The components must be added to the Greta platform.
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




(To continue...)
