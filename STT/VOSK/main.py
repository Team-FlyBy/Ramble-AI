import json
import argparse
from audio_stream import start_stream, q
from recognizer import DualRecognizer, SingleRecognizer
from language_selector import select_language

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Speech recognition with single or dual model.")
parser.add_argument('--mode', choices=['single', 'dual'], default='single', 
                    help="Choose recognition mode: 'single' or 'dual'")
parser.add_argument('--lang', choices=['en', 'ko'], default='en', 
                    help="Choose recognition mode: 'en' or 'ko'")
args = parser.parse_args()

print("모델 로딩 중...")

# Initialize recognizer based on mode
if args.mode == 'single':
    recognizer = SingleRecognizer(args.lang)
else:
    recognizer = DualRecognizer()
print("완료! 말해보세요. (Ctrl+C로 종료)")

with start_stream():
    try:
        while True:
            data = q.get()
            if args.mode == 'single':
                result = recognizer.recognize(data)
                if result:
                    result = json.loads(result)
                    text = result.get("text", "")
                    if text:
                        print(f"🇰🇷 {text}")
            else:
                ko_text, en_text = recognizer.recognize(data)
                lang, text = select_language(ko_text, en_text)
                if text:
                    flag = "🇰🇷" if lang == "ko" else "🇺🇸"
                    print(f"{flag} {text}")

    except KeyboardInterrupt:
        print("\n종료합니다.")