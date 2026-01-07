import os, requests, pandas as pd
from datetime import datetime
from io import StringIO

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1X9vGvI2fO5Wc-5_mUfW9tS9i8_V8z3J1XW-n9u-GvX_Y1/pub?output=csv"

def send_quiz():
    try:
        r = requests.get(CSV_URL)
        r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        df.columns = df.columns.str.strip()
        
        # Dono formats check karega (YYYY-MM-DD aur DD-MM-YYYY)
        today1 = datetime.now().strftime("%Y-%m-%d")
        today2 = datetime.now().strftime("%d-%m-%Y")
        
        df['Date'] = df['Date'].astype(str).str.strip()
        todays_qs = df[(df['Date'] == today1) | (df['Date'] == today2)]

        if todays_qs.empty:
            print("No questions found for today's date.")
            return

        for _, row in todays_qs.iterrows():
            payload = {
                "chat_id": CHAT_ID,
                "question": f"🆔 @mission_merit\n\n[{row['Subject']}] {row['Question']}",
                "options": [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])],
                "is_anonymous": False,
                "type": "quiz",
                "correct_option_id": int(row['Correct']),
                "explanation": f"{row['Explanation']}\n\n🔗 Join: @mission_merit"[:190],
                "explanation_parse_mode": "HTML"
            }
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", json=payload)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_quiz()
