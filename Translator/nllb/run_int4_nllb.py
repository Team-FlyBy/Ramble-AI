# run_int4_nllb.py

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, BitsAndBytesConfig

def main():
    save_dir = "./model/nllb_model"

    # ① 동일한 quant 설정
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )

    # ② 토크나이저·모델 로드
    tokenizer = AutoTokenizer.from_pretrained(save_dir, src_lang="eng_Latn")
    model     = AutoModelForSeq2SeqLM.from_pretrained(
        save_dir,
        quantization_config=bnb_config,
        device_map="auto"
    )

    # ③ pipeline 생성
    en2ko = pipeline(
        "translation",
        model=model,
        tokenizer=tokenizer,
        src_lang="eng_Latn",
        tgt_lang="kor_Hang",
        device_map="auto"
    )
    ko2en = pipeline(
        "translation",
        model=model,
        tokenizer=tokenizer,
        src_lang="kor_Hang",
        tgt_lang="eng_Latn",
        device_map="auto"
    )

    # ④ 테스트
    print("EN→KR:", en2ko("hello world", max_length=20)[0]["translation_text"])
    print("KR→EN:", ko2en("안녕하세요", max_length=20)[0]["translation_text"])

if __name__ == "__main__":
    main()
