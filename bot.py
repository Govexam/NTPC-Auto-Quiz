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
        # Load Sheet
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8' # Hindi text sahi dikhne ke liye
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        
        # DATE FIX: Sheet format DD-MM-YYYY read karega
        today = datetime.now().strftime("%d-%m-%Y")
        
        # Data Cleaning: Date aur Correct column ko sahi format mein laana
        df['Date'] = df['Date'].astype(str).str.strip()
        
        # Filtering today's questions
        todays_qs = df[df['Date'] == today]

        if todays_qs.empty:
            print(f"Bhai, aaj ({today}) ki date ka koi sawal nahi mila!")
            return

        print(f"Sawal mil gaye! Total: {len(todays_qs)}. Posting to Telegram...")

        for index, row in todays_qs.iterrows():
            options = [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])]
            
            # Branding & Clickable Link
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
                "explanation": full_explanation[:190], # 200 char limit safe
                "explanation_parse_mode": "HTML"
            }
            requests.post(url, json=payload)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_quiz()
