import os
import requests
import pandas as pd
from io import StringIO

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
# Aapka Naya Published Link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtjzNJ-ENITXsVxZlgkmfKrLWeKR4ffPYFiXEXuf0e8fv1mk0otCoN6J4RNmekecz_Z6PIUVCVJn0W/pub?output=csv"

def send_quiz():
    try:
        # Data download
        r = requests.get(CSV_URL)
        r.encoding = 'utf-8'
        
        # Header=0 ka matlab pehli line headers hai, par hum iloc (position) use karenge
        df = pd.read_csv(StringIO(r.text))
        
        print(f"Total {len(df)} rows mili hain.")

        # Sirf pehle 5 sawal bhejne ka loop
        for index, row in df.head(5).iterrows():
            
            # --- YAHAN JADU HAI (Position Mapping) ---
            # Hum naam nahi, column ka number use kar rahe hain
            # CSV: Date(0), Exam(1), Subject(2), Question(3), A(4), B(5), C(6), D(7), Correct(8), Expl(9)
            
            subject = str(row.iloc[2])      # 3rd Column (Subject)
            question = str(row.iloc[3])     # 4th Column (Question)
            opt_a = str(row.iloc[4])        # 5th Column
            opt_b = str(row.iloc[5])
            opt_c = str(row.iloc[6])
            opt_d = str(row.iloc[7])
            correct = int(row.iloc[8])      # 9th Column (0,1,2,3)
            expl = str(row.iloc[9])         # 10th Column (Explanation)

            # Message taiyar
            payload = {
                "chat_id": CHAT_ID,
                "question": f"🆔 @mission_merit\n\n[{subject}] {question}",
                "options": [opt_a, opt_b, opt_c, opt_d],
                "type": "quiz",
                "correct_option_id": correct,
                "explanation": f"{expl}\n\nJoin @mission_merit"
            }
            
            # Bhej do
            resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", json=payload)
            print(f"Status: {resp.status_code} | Question: {question[:15]}...")

    except Exception as e:
        print(f"❌ Error aaya: {e}")

if __name__ == "__main__":
    send_quiz()
