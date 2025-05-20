import queue
import sounddevice as sd
from config import SAMPLE_RATE

class AudioHandler:
    """오디오 스트림 처리를 위한 클래스"""
    
    def __init__(self):
        self.queue = queue.Queue()
    
    def audio_callback(self, indata, frames, time, status):
        """sounddevice 콜백 함수"""
        try:
            if status:
                print(f"오디오 상태 알림: {status}")
            self.queue.put(bytes(indata))
        except Exception as e:
            print(f"오디오 처리 중 오류 발생: {e}")
    
    def get_audio_chunk(self, block=True, timeout=None):
        """큐에서 오디오 데이터 청크를 가져옵니다"""
        try:
            return self.queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None

def start_stream(callback=None, blocksize=8000):
    """
    오디오 입력 스트림을 시작합니다.
    
    Args:
        callback (callable, optional): 오디오 데이터를 처리할 콜백 함수.
        blocksize (int, optional): 오디오 블록 크기. 기본값은 8000.
        
    Returns:
        tuple:
            sd.RawInputStream: 설정된 오디오 스트림 객체.
            AudioHandler: 스트림 종료 및 후처리를 담당하는 핸들러 인스턴스.
        
    Raises:
        sd.PortAudioError: 오디오 스트림을 시작할 수 없는 경우.
    """
    audio_handler = AudioHandler()
    callback_func = callback if callback else audio_handler.audio_callback

    try:
        stream = sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=blocksize,
            dtype='int16',
            channels=1,
            callback=callback_func
        )
        return stream, audio_handler
    except sd.PortAudioError as e:
        print(f"오디오 스트림을 시작할 수 없습니다: {e}")
        raise
