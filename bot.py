import os
import requests
import pandas as pd
from datetime import datetime

# Config
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
# Aapki CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtjzNJ-ENITXsVxZlgkmfKrLWeKR4ffPYFiXEXuf0e8fv1mk0otCoN6J4RNmekecz_Z6PIUVCVJn0W/pub?output=csv"

def send_quiz():
    try:
        # Load Sheet
        df = pd.read_csv(CSV_URL)
        
        # Filter for Today's Questions (YYYY-MM-DD format)
        today = datetime.now().strftime("%Y-%m-%d")
        todays_qs = df[df['Date'] == today]

        if todays_qs.empty:
            print(f"Aaj ({today}) ke liye koi question nahi mila bhai!")
            return

        print(f"Total {len(todays_qs)} questions mile. Posting to Telegram...")

        for index, row in todays_qs.iterrows():
            options = [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])]
            
            # Telegram Poll API
            url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"
            payload = {
                "chat_id": CHAT_ID,
                "question": f"[{row['Subject']}] {row['Question']}",
                "options": options,
                "is_anonymous": False,
                "type": "quiz",
                "correct_option_id": int(row['Correct']),
                "explanation": str(row['Explanation'])[:190] # Safe limit
            }
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                print("Question posted successfully!")
            else:
                print(f"Error: {res.text}")

    except Exception as e:
        print(f"Kuch gadbad hui: {e}")

if __name__ == "__main__":
    send_quiz()
