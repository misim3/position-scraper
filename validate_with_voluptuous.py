# 페이지의 변화 탐지
from voluptuous import Schema, Match

# 다음 4개의 규칙을 가진 스키마 정의
schema = Schema({ # 규칙1: 객체는 dict 자료형
    'name': str, # 규칙2: name은 str 자료형
    'price': Match(r'^[0-9,]+$'), # 규칙3: price가 정규표현식에 맞는지 확인
}, required=True) # 규칙4: dict의 키는 필수

