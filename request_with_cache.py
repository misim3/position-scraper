import requests
from cachecontrol import CacheControl

# 캐시와 관련된 http 헤더의 값 변경을 통해 페이지가 변경되었는지 확인한다.

session = requests.session()
cached_session = CacheControl(session)

# 첫 시도는 캐시되어 있지 않으므로 서버에서 추출한 이후 캐시한다.
response = cached_session.get('https://example.com')
print(response.from_cache)

# 두 번째는 ETag와 Last-Modified 값을 사용해 업데이트됐는지 확인한다.
response = cached_session.get('https://example.com')
print(response.from_cache)

# @Redis에 캐시를 저장할 수도 있다. 자세한 사항은 CacheControl 문서 참고
# @공고 리스트 페이지에서 한 가지 채용 공고가 변해도 페이지의 값이 변경되는 지 확인하고, 그 결과에 따라 대처하자.