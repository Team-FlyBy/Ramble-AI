## VOSK Code 디렉터리 구조

```
vosk_multilang_stt/
├── __init__.py
├── config.py             # 경로/샘플레이트 등 설정
├── audio_stream.py       # 마이크 입력 처리
├── recognizer.py         # Vosk recognizer 초기화 및 처리
├── language_selector.py  # 어떤 언어 선택할지 결정
└── main.py               # 실행 엔트리포인트
```

## Installation

``` pip install vosk sounddevice ```

## model install

[모델 설치 주소](https://alphacephei.com/vosk/models)

## How to use

STT/VOSK/model 위치에 다운로드한 model 옮기기
STT/VOSK/config.py 파일 수정

``` 
mode: single or dual
lang: ko or en

python main.py --mode single --lang ko
```

## 언어 디렉토리 구조

```
vosk-model-small-ko-0.22/
├── am/                          # 음향 모델 (Acoustic Model)
│   ├── final.mdl                # DNN 기반 최종 모델
│   ├── tree                     # HMM/음소 결정 트리
│   └── ...                      # 기타 음향 모델 관련 파일
├── conf/
│   └── mfcc.conf                # MFCC 특징 추출 설정 파일
├── ivector/                     # 화자 적응용 i-vector 관련 파일
│   ├── final.dubm              # Diagonal UBM (GMM 기반 화자 모델)
│   ├── final.ie                # i-vector 추출기
│   └── ...
├── graph/                       # 디코딩 그래프 및 단어 매핑
│   ├── HCLG.fst                # 디코딩 그래프 (HMM + 언어모델 + 발음사전)
│   └── words.txt              # 단어 ID ↔ 단어 텍스트 매핑
├── phones/                      # 음소 관련 정보
│   └── ...
├── rescore/ (optional)          # RNNLM 등 재점수화(rescoring)용 파일 (거의 사용 안 함)
│   └── ...
└── README                       # 모델 설명 문서
```

| 이름                | 역할                                                                |
| ----------------- | ----------------------------------------------------------------- |
| `am/`             | **Acoustic Model** 디렉토리. DNN 기반 음향모델이 `final.mdl`, 발음 트리 등 |
| `conf/mfcc.conf`  | **MFCC 설정** 파일. 음성 피처 추출할 때 이 설정을 따름                            |
| `ivector/`        | 화자 특징 추출 (i-vector), 화자 적응(Speaker Adaptation)에 사용              |
| `graph/HCLG.fst`  | **디코딩 그래프**. 발음 사전, 언어 모델, 트랜지션 등을 합성한 그래프                       |
| `graph/words.txt` | **단어 ID → 단어 문자열** 매핑. 디코딩 결과를 사람이 이해할 수 있게 변환                   |
| `phones/`         | **음소 정보** 디렉토리. 디버깅이나 세부 조정에 사용됨.                                 |