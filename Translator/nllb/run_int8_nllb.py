from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import AutoTokenizer, pipeline

# ① INT8 ONNX 모델 로드
model = ORTModelForSeq2SeqLM.from_pretrained(
    "./model/nllb_onnx_int8",
    provider="CPUExecutionProvider",
    export=False
)
tokenizer = AutoTokenizer.from_pretrained("./model/nllb_onnx_int8", src_lang="eng_Latn")

# ② 파이프라인 구성
translator = pipeline(
    "translation",
    model=model,
    tokenizer=tokenizer,
    src_lang="eng_Latn",
    tgt_lang="kor_Hang",
    device=-1  # CPU
)

# ③ 번역 테스트
print(translator("hello world", max_length=20)[0]["translation_text"])
