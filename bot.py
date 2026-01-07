import os
import requests
import pandas as pd
from datetime import datetime
from io import StringIO

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1X9vGvI2fO5Wc-5_mUfW9tS9i8_V8z3J1XW-n9u-GvX_Y1/pub?output=csv"

def send_quiz():
    try:
        # Cache bypass ke liye link thoda badla hai
        r = requests.get(f"{CSV_URL}&v={datetime.now().timestamp()}")
        r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        
        # Column cleaning
        df.columns = df.columns.str.strip()
        
        # System Date
        today = datetime.now().strftime("%Y-%m-%d")
        
        print(f"--- DEBUG INFO ---")
        print(f"System searching for: '{today}'")
        print(f"Dates found in your Sheet: {df['Date'].unique().tolist()}")
        print(f"Total rows in sheet: {len(df)}")
        print(f"------------------")

        # Date match karna
        df['Date'] = df['Date'].astype(str).str.strip()
        todays_qs = df[df['Date'] == today]

        if todays_qs.empty:
            print("❌ Koi sawal nahi mila match hone wali date par.")
            return

        for index, row in todays_qs.iterrows():
            payload = {
                "chat_id": CHAT_ID,
                "question": f"🆔 @mission_merit\n\n[{row['Subject']}] {row['Question']}",
                "options": [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])],
                "type": "quiz",
                "correct_option_id": int(row['Correct'])
            }
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", json=payload)
        print("✅ Quiz successfully posted!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_quiz()
