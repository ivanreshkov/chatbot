import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
import re
import time
from openai import OpenAI

# Config
API_KEY = "ADD OPENAI API KEY"
DATA_FILE = "LLM-DataScientist-Task_Data.csv"

client = OpenAI(
    api_key=API_KEY,
)

history = [] # Variable to retain information from previous queries

uploaded_file = client.files.create(file=open(DATA_FILE, "rb"), purpose="assistants")
file_id = uploaded_file.id

assistant = client.beta.assistants.create(
    instructions="""You're a data assistant. Answer questions based on the uploaded CSV file using code interpreter.""",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],
    tool_resources={"code_interpreter": {"file_ids": [file_id]}}
)

thread = client.beta.threads.create()

print("Assistant and thread initialized.")
print("File successfully added to the system")

def load_data():
    df = pd.read_csv(DATA_FILE)
    return df

# Load and store data globally
df = load_data()

# Check if preclassified otherwise classify now
if "predicted_category" not in df.columns:
    print("Classifying messages...")
    from classifier import classify_dataframe
    df = classify_dataframe(df)
    df.to_csv("messages_with_categories.csv", index = False)
else:
    print("Preclassified data loaded")

# --- Generate Response ---
def get_chatbot_response(user_input):

    history.append({
        "role" : "user",
        "content" : user_input,
    })
    
    thread = client.beta.threads.create(
  messages=history
)

    # Start and poll the run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Retrieve the assistants messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
        
    # Get the last assistant message
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            return msg.content[0].text.value          
            
    return "No response from assistant."

# --- GUI Logic ---     
def on_submit(event=None):

    user_input = input_field.get()
    output_field.config(state='normal')
    output_field.insert('end', f'User: {user_input}\n', 'user')

    response = get_chatbot_response(user_input)
    output_field.insert('end', f'Bot: {response}\n\n', 'bot')

    input_field.delete(0, 'end')
    output_field.config(state='disabled')

# --- GUI Setup ---
root = tk.Tk()
root.title("Chatbot")

output_frame = tk.Frame(root)
output_frame.pack(side='top', fill='both', expand=True)

output_field = tk.Text(output_frame)
output_field.pack(side='left', fill='both', expand=True)
output_field.config(state='disabled', font=('Courier', 18))
output_field.tag_config('user', foreground='white')
output_field.tag_config('bot', foreground='green')

input_frame = tk.Frame(root)
input_frame.pack(side='bottom', fill='x')

input_field = tk.Entry(input_frame, width=100)
input_field.pack(side='left', fill='x', expand=True, padx=5, pady=5)
input_field.bind("<Return>", on_submit)

submit_btn = tk.Button(input_frame, text="Send", command=on_submit)
submit_btn.pack(side='right')

root.mainloop()