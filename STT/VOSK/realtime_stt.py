import queue
import sounddevice as sd
import sys
import json
from vosk import Model, KaldiRecognizer

# STEP 1: 모델 경로 설정 (네가 다운로드한 모델 폴더 경로로 수정)
MODEL_PATH = "/Users/jiwan/Documents/GitHub/Remble-AI/STT/VOSK/model/vosk-model-small-ko-0.22"
# MODEL_PATH = "/Users/jiwan/Documents/GitHub/Remble-AI/STT/VOSK/model/vosk-model-small-en-us-0.15"

# STEP 2: 오디오 설정
SAMPLE_RATE = 16000  # 샘플레이트는 모델이 요구하는 값 (보통 16kHz)
q = queue.Queue()

# STEP 3: 콜백 함수 (마이크 입력 데이터를 큐에 넣음)
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# STEP 4: 모델 로딩
print("모델 로딩 중...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("모델 로딩 완료. 이제 말해보세요 (Ctrl+C로 종료)")

# STEP 5: 실시간 스트리밍 시작
with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    try:
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("👉 인식:", result.get("text"))
            else:
                # 부분 인식도 출력하고 싶으면 이 부분 주석 해제
                # partial = json.loads(recognizer.PartialResult())
                # print("부분:", partial.get("partial"))
                pass
    except KeyboardInterrupt:
        print("\n종료합니다.")
