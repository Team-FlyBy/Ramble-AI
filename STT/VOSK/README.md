pip list

pip install vosk
pip install sounddevice  # 마이크로 입력을 받으려면 필요

## 언어 디렉토리 구조

vosk-model-small-ko-0.22/
├── am/
│   ├── final.mdl            # acoustic model (DNN 등)
│   ├── tree                 # HMM/phonetic decision tree
│   └── ...                  # 추가 acoustic model 파일들
├── conf/
│   ├── mfcc.conf            # feature extraction config (MFCC)
├── ivector/
│   ├── final.dubm           # Diagonal UBM (GMM for speaker)
│   ├── final.ie             # i-vector extractor
│   └── ...                  # speaker adaptation용
├── graph/
│   ├── HCLG.fst             # decoding graph (HMM + LM + lexicon)
│   └── words.txt            # word ID <-> word mapping
├── phones/                 
│   ├── ...                  # phoneme 관련 정보
├── rescore/ (optional)      
│   └── ...                  # rescoring에 필요한 RNNLM 등 (거의 안 씀)
├── README


| 이름                | 역할                                                                |
| ----------------- | ----------------------------------------------------------------- |
| `am/`             | **Acoustic Model** 디렉토리. DNN 기반 음향모델이 `final.mdl`, 발음 트리 등 |
| `conf/mfcc.conf`  | **MFCC 설정** 파일. 음성 피처 추출할 때 이 설정을 따름                            |
| `ivector/`        | 화자 특징 추출 (i-vector), 화자 적응(Speaker Adaptation)에 사용              |
| `graph/HCLG.fst`  | **디코딩 그래프**. 발음 사전, 언어 모델, 트랜지션 등을 합성한 그래프                       |
| `graph/words.txt` | **단어 ID → 단어 문자열** 매핑. 디코딩 결과를 사람이 이해할 수 있게 변환                   |
| `phones/`         | **음소 정보** 디렉토리. 디버깅이나 세부 조정에 사용                                 |
