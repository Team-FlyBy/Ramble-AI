# 수정 예정
def select_language(ko_text, en_text):
    """
    두 언어로 인식된 텍스트 중에서 더 적합한 언어를 선택합니다.

    Args:
        ko_text (str): 한국어로 인식된 텍스트
        en_text (str): 영어로 인식된 텍스트
        
    Returns:
        tuple: (선택된 언어 코드, 해당 언어의 텍스트)
            언어 코드는 'ko', 'en', 또는 None(선택 불가능한 경우)
    """
    # 두 텍스트가 모두 비어있는지 확인
    if not ko_text and not en_text:
        return None, ""
        
    # 한쪽만 비어있는 경우 비어있지 않은 쪽 선택
    if not ko_text:
        return "en", en_text
    if not en_text:
        return "ko", ko_text
        
    # 두 텍스트 모두 내용이 있는 경우 길이 비교
    # 여기서 가중치나 신뢰도 점수를 추가할 수도 있음
    if len(ko_text) > len(en_text):
        return "ko", ko_text
    else:
        return "en", en_text