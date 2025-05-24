# test.py

import json
import argparse
import sys
import os

# 상위 디렉토리에 두었다면 경로 추가
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from nllb_translator import NLLBTranslator

def main():
    parser = argparse.ArgumentParser(description="Simple NLLB translation test script.")
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="./model/nllb_int4_quantized",
        help="ONNX 모델 디렉토리 경로"
    )
    parser.add_argument(
        "--text", "-t",
        type=str,
        default="hello world",
        help="번역할 원문"
    )
    parser.add_argument(
        "--direction", "-d",
        choices=["en2ko", "ko2en"],
        default="en2ko",
        help="번역 방향: en2ko 또는 ko2en"
    )
    args = parser.parse_args()

    print("모델 로딩 중…")
    if args.direction == "en2ko":
        translator = NLLBTranslator(
            model_path=args.model,
            src_lang="eng_Latn",
            tgt_lang="kor_Hang",
            provider=None  # 자동으로 CPU 또는 GPU 선택
        )
    else:
        translator = NLLBTranslator(
            model_path=args.model,
            src_lang="kor_Hang",
            tgt_lang="eng_Latn",
            provider=None
        )

    print("완료! 번역 실행…")
    result = translator.translate(args.text)
    arrow = "→"
    lang_label = "EN→KR" if args.direction=="en2ko" else "KR→EN"
    print(f"{lang_label} {args.text} {arrow} {result}")

if __name__ == "__main__":
    main()
