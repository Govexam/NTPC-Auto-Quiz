import os
import time  # Time module add kiya hai break ke liye
import requests
import pandas as pd
from io import StringIO

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtjzNJ-ENITXsVxZlgkmfKrLWeKR4ffPYFiXEXuf0e8fv1mk0otCoN6J4RNmekecz_Z6PIUVCVJn0W/pub?output=csv"

def send_quiz():
    try:
        r = requests.get(CSV_URL)
        r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        
        print(f"Total {len(df)} sawal mile. Ab sab bhej raha hoon...")

        # LIMIT HATA DI HAI: Ab ye df.head(5) nahi, balki puri 'df' chalayega
        for index, row in df.iterrows():
            
            # --- Position Mapping (Naam ka jhanjhat nahi) ---
            subject = str(row.iloc[2])      # Column 3
            question = str(row.iloc[3])     # Column 4
            opt_a = str(row.iloc[4])        # Column 5
            opt_b = str(row.iloc[5])
            opt_c = str(row.iloc[6])
            opt_d = str(row.iloc[7])
            correct = int(row.iloc[8])      # Column 9
            expl = str(row.iloc[9])         # Column 10

            payload = {
                "chat_id": CHAT_ID,
                "question": f"🆔 @mission_merit\n\n[{subject}] {question}",
                "options": [opt_a, opt_b, opt_c, opt_d],
                "type": "quiz",
                "correct_option_id": correct,
                "explanation": f"{expl}\n\nJoin @mission_merit"
            }
            
            resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", json=payload)
            
            if resp.status_code == 200:
                print(f"✅ Sent: {question[:20]}...")
            else:
                print(f"❌ Failed: {resp.status_code}")

            # 2 Second ka break taaki Telegram Ban na kare
            time.sleep(2)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_quiz()
