import os
import requests
import pandas as pd
from datetime import datetime

# Config
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtjzNJ-ENITXsVxZlgkmfKrLWeKR4ffPYFiXEXuf0e8fv1mk0otCoN6J4RNmekecz_Z6PIUVCVJn0W/pub?output=csv"

def send_quiz():
    try:
        df = pd.read_csv(CSV_URL)
        today = datetime.now().strftime("%Y-%m-%d")
        todays_qs = df[df['Date'] == today]

        if todays_qs.empty:
            print(f"No questions for {today}")
            return

        for index, row in todays_qs.iterrows():
            options = [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])]
            
            # Clickable link format (HTML)
            # Explanation ke andar humne thoda space diya hai
            footer_text = "\n\n━━━━━━━━━━━━━━━\n🔗 Join: @mission_merit"
            full_explanation = f"{row['Explanation']}{footer_text}"

            url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"
            payload = {
                "chat_id": CHAT_ID,
                "question": f"🆔 @mission_merit\n\n[{row['Subject']}] {row['Question']}",
                "options": options,
                "is_anonymous": False,
                "type": "quiz",
                "correct_option_id": int(row['Correct']),
                "explanation": full_explanation[:190], # Telegram limit
                "explanation_parse_mode": "HTML" # Isse @handle clickable ho jayega
            }
            requests.post(url, json=payload)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_quiz()
