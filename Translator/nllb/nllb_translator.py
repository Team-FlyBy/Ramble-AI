# nllb_translator.py

import onnxruntime as ort
from transformers import AutoTokenizer, pipeline
from optimum.onnxruntime import ORTModelForSeq2SeqLM

class NLLBTranslator:
    def __init__(
        self,
        model_path: str,
        src_lang: str = "eng_Latn",
        tgt_lang: str = "kor_Hang",
        provider: str = None
    ):
        """
        model_path: ONNX 파일이 들어있는 디렉토리 경로
        src_lang/tgt_lang: Hugging Face NLLB 언어 코드
        provider: ONNXRuntime 실행 프로바이더 (예: "CPUExecutionProvider" or "CUDAExecutionProvider")
        """

        # 1) ONNXRuntime provider 결정
        if provider:
            ort_providers = [provider]
        else:
            ort_providers = (
                ["CUDAExecutionProvider"]
                if ort.get_device().upper() == "GPU"
                else ["CPUExecutionProvider"]
            )

        # 2) 토크나이저 로드 (src_lang 지정)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, src_lang=src_lang)

        # 3) ONNX 모델 로드(export=False로 변환 스텝 건너뜀)
        self.model = ORTModelForSeq2SeqLM.from_pretrained(
            model_path,
            provider=ort_providers[0],
            export=False
        )

        # 4) HF pipeline 생성 (device=-1→CPU, 0→첫 번째 CUDA)
        device = 0 if ort_providers[0].startswith("CUDA") else -1
        self.pipe = pipeline(
            task="translation",
            model=self.model,
            tokenizer=self.tokenizer,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            device=device
        )

        # 5) 언어 설정 보관
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang

    def translate(self, text: str, max_length: int = 40) -> str:
        """
        text: 번역할 문자열
        max_length: 생성할 최대 토큰 길이
        """
        outputs = self.pipe(text, max_length=max_length)
        return outputs[0]["translation_text"]
