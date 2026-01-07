import os
import requests
import pandas as pd
from io import StringIO

# Config
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtjzNJ-ENITXsVxZlgkmfKrLWeKR4ffPYFiXEXuf0e8fv1mk0otCoN6J4RNmekecz_Z6PIUVCVJn0W/pub?output=csv"

def send_quiz():
    try:
        # 1. Sheet Load Karo
        print("Sheet download kar raha hoon...")
        r = requests.get(CSV_URL)
        r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        
        # 2. Columns saaf karo
        df.columns = df.columns.str.strip()
        print(f"Sheet mein total {len(df)} rows mili hain.")

        # 3. FORCE TEST: Sirf pehle 2 sawal uthao (No Date Filter)
        test_qs = df.head(2)

        for index, row in test_qs.iterrows():
            print(f"Sawal bhej raha hoon: {row['Question']}")
            
            options = [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])]
            
            payload = {
                "chat_id": CHAT_ID,
                "question": f"TEST QUIZ: {row['Question']}",
                "options": options,
                "type": "quiz",
                "correct_option_id": 0
            }
            
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", json=payload)
            print(f"Telegram ka jawab: {res.text}")

    except Exception as e:
        print(f"Galti ho gayi: {e}")

if __name__ == "__main__":
    send_quiz()
