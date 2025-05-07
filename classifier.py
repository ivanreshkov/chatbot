from openai import OpenAI
import pandas as pd
import time

API_KEY = "ADD OPENAI API KEY"

client = OpenAI(
    api_key=API_KEY,
)

CATEGORIES = [
    "Freespin issues",
    "Deposit or payment issues",
    "Account access or status issues",
    "Withdrawal issues",
    "Technical or game issues",
    "No useful information"
]

def classify_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": (
                    "You are an assistant that classifies customer support messages into one of the following actionable categories:\n"
                    "- Freespin issues\n"
                    "- Deposit or payment issues\n"
                    "- Account access or status issues\n"
                    "- Withdrawal issues\n"
                    "- Technical or game issues\n"
                    "- No useful information\n\n"
                    "Your response must be only the category name from the list above. No extra text, no explanations."
                )},
                {"role": "user", "content": message}
            ],
            temperature=0.0,
        )
        category = response.choices[0].message.content.strip()
        return category
    except Exception as e:
        print(f"Error: {e}")
        return "No useful information"
    
def classify_dataframe(df, message_column="message"):
    df["predicted_category"] = None
    for idx, row in df.iterrows():
        message = row[message_column]
        if not isinstance(message, str):
            df.at[idx, "predicted_category"] = "No useful information"
            continue

        cat = classify_message(message)
        df.at[idx, "predicted_category"] = cat
        print(f"[{idx}] {cat} <- {message[:80]}")
        time.sleep(1)  # Respect rate limits
    return df