example.xml contains the CBT template for IAVA system.

It contains the following functionalities:
- ASR-Flipper2.0 connection: Transcribes the User utterance to text via ASR and selects the next Agent utterance (FML scenario file) with Flipper2.0
- Feedback: Constantly updates the Agent's speaking state ("isSpeaking")
- CBT ATcls: Checks if the User utterance is an automatic thought (binary classification) based on a LLM-based (BERT-based) model.