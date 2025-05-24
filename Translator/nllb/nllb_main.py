import json
import argparse

import sys
import os
# 상위 디렉토리 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# print(sys.path)

from STT.VOSK.audio_stream import start_stream
from STT.VOSK.recognizer import DualRecognizer, SingleRecognizer
from STT.VOSK.language_selector import select_language
from nllb_translator import NLLBTranslator  # 여기서 번역기 import

parser = argparse.ArgumentParser(description="Speech recognition with single or dual model.")
parser.add_argument('--mode', choices=['single', 'dual'], default='single', help="Choose recognition mode: 'single' or 'dual'")
parser.add_argument('--lang', choices=['en', 'ko'], default='en', help="Choose recognition language: 'en' or 'ko'")
args = parser.parse_args()

print("모델 로딩 중...")

if args.mode == 'single':
    recognizer = SingleRecognizer(args.lang)
else:
    recognizer = DualRecognizer()

translator = NLLBTranslator(model_path=".\model\model-quant.onnx")  # 한 번만 로드

print("완료! 말해보세요. (Ctrl+C로 종료)")

stream, audio_handler = start_stream()

try:
    with stream:
        while True:
            data = audio_handler.get_audio_chunk()
            if args.mode == 'single':
                result = recognizer.recognize(data)
                if result:
                    result = json.loads(result)
                    text = result.get("text", "")
                    if text:
                        flag = "🇰🇷" if args.lang == "ko" else "🇺🇸"
                        print(f"{flag} {text}")
                        
                        # 번역 적용
                        if args.lang == "en":
                            translated = translator.translate(text)
                            print(f"🇰🇷 번역: {translated}")
                        elif args.lang == "ko":
                            # src/tgt 언어 설정 바꾸기 (필요 시)
                            translator.src_lang = "kor_Hang"
                            translator.tgt_lang = "eng_Latn"
                            translated = translator.translate(text)
                            print(f"🇺🇸 번역: {translated}")

            else:
                ko_text, en_text = recognizer.recognize(data)
                lang, text = select_language(ko_text, en_text)
                if text:
                    flag = "🇰🇷" if lang == "ko" else "🇺🇸"
                    print(f"{flag} {text}")

except KeyboardInterrupt:
    print("\n종료합니다.")
