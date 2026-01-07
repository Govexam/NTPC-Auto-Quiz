import os
import requests
import pandas as pd
from datetime import datetime
from io import StringIO

# Config
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtjzNJ-ENITXsVxZlgkmfKrLWeKR4ffPYFiXEXuf0e8fv1mk0otCoN6J4RNmekecz_Z6PIUVCVJn0W/pub?output=csv"

def send_quiz():
    try:
        # Load Sheet with UTF-8 encoding
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        
        # Column names ko clean karna (extra space hatana)
        df.columns = df.columns.str.strip()
        
        # DATE FIX: Aaj ki date DD-MM-YYYY format mein
        today = datetime.now().strftime("%d-%m-%Y")
        
        # Date column ko string banakar filter karna
        df['Date'] = df['Date'].astype(str).str.strip()
        todays_qs = df[df['Date'] == today]

        if todays_qs.empty:
            print(f"Bhai, sheet mein {today} ki date nahi mili!")
            return

        print(f"Total {len(todays_qs)} sawal mile. Posting...")

        for index, row in todays_qs.iterrows():
            # Yahan column names ekdum wahi hain jo aapki sheet mein hain
            options = [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])]
            
            footer = "\n\n━━━━━━━━━━━━━━━\n🔗 Join: @mission_merit"
            # Explanation agar khali ho toh handle karna
            expl = str(row['Explanation']) if pd.notna(row['Explanation']) else "No explanation."
            full_expl = f"{expl}{footer}"

            url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"
            payload = {
                "chat_id": CHAT_ID,
                "question": f"🆔 @mission_merit\n\n[{row['Subject']}] {row['Question']}",
                "options": options,
                "is_anonymous": False,
                "type": "quiz",
                "correct_option_id": int(row['Correct']),
                "explanation": full_expl[:190],
                "explanation_parse_mode": "HTML"
            }
            requests.post(url, json=payload)

    except Exception as e:
        print(f"Error Details: {e}")

if __name__ == "__main__":
    send_quiz()
