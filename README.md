# chatbot

requeremenets:
Python 3.12.6 with tkinter
numpy             2.2.5
openai            1.77.0
pandas            2.2.3

Note: OpenAI API KEY must be added as a string to the variable defined in the scripts "API_KEY" before running the program.

In the Python script, we first classify the messages. At the beginning, we check whether the current document already contains a column with the predicted categories. If a file has not yet been classified, we initiate the classification process, where each message is sent to OpenAI. Based on the instructions provided to the model, which define the available categories, it classifies each message accordingly. This process takes some time. Categories that are not defined in the instructions parameter of the create function cannot appear in the model’s response. Instead, such messages will be categorized as “No useful information.”

After the classification is complete, a Tkinter-based user interface is launched, allowing us to chat with the OpenAI LLM. I used the Assistant object from OpenAI, which enables uploading a CSV file from which the model can extract information based on user prompts. The chat history is managed using a list called "history", where all user inputs are saved and sent back to the model with each new message.

Limitations

The main limitations of the current system include conversational memory and context preservation. The model’s responses do not always fully satisfy the prompt. Conversational memory should be improved.

In a previous implementation using the OpenAI Completions API, history was maintained using message IDs. However, the current implementation using the Assistants API does not support this kind of history management, which is a limitation that needs to be addressed.

Access to the full conversation history would significantly improve classification accuracy and user comprehension. Currently, messages are classified in isolation. 

If full conversation history were available, I would implement context-aware classification, using surrounding dialogue to infer intent and category more accurately. This could be achieved using sequence models (such as transformer-based architectures) that analyze entire conversations or message threads. The classifier could then operate at the dialogue level, rather than on a per-message basis, resulting in better and more accurate tracking of user intent.

To validate classification performance, I would use the following methodology:
- Create a manually labeled test set of support messages, ideally annotated by domain experts.
- Conduct periodic human audits on a random sample of predictions to assess real-world accuracy.
