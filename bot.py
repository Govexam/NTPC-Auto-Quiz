import os, requests, pandas as pd
from io import StringIO

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHANNEL_ID")
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtjzNJ-ENITXsVxZlgkmfKrLWeKR4ffPYFiXEXuf0e8fv1mk0otCoN6J4RNmekecz_Z6PIUVCVJn0W/pub?output=csv"

def send_quiz():
    try:
        # Data download
        r = requests.get(CSV_URL)
        r.encoding = 'utf-8'
        df = pd.read_csv(StringIO(r.text))
        
        # --- FIX: Column ke naam se spaces hatana ---
        df.columns = df.columns.str.strip()
        
        print(f"Sheet se {len(df)} sawal mile.")
        print(f"Columns mile: {list(df.columns)}") # Debugging ke liye

        # Ab ye safely chalega
        for index, row in df.head(5).iterrows():
            # Agar Subject column nahi mila, to default 'GK' use karega
            subject = row['Subject'] if 'Subject' in row else 'GK'
            
            payload = {
                "chat_id": CHAT_ID,
                "question": f"🆔 @mission_merit\n\n[{subject}] {row['Question']}",
                "options": [str(row['Opt_A']), str(row['Opt_B']), str(row['Opt_C']), str(row['Opt_D'])],
                "type": "quiz",
                "correct_option_id": int(row['Correct']),
                "explanation": "Join @mission_merit"
            }
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPoll", json=payload)
            print(f"Posted: {row['Question'][:20]}...")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_quiz()
