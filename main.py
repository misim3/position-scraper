# https://classum.career.greetinghr.com
# */robots.txt -> 구글이나 빙의 검색 서비스를 이용해서 회사의 공고를 찾으면 안된다.
# 정말 url의 조합을 통해 회사 홈페이지를 찾아야 한다.
# 그러므로 일단 맨 위의 형식과 같은 홈페이지부터 찾아보자.
# 위의 url 형식을 사용하지 않고 그리팅하이어의 서비스를 이용하는 경우에는 어떻게 찾을 수 있을까?
# 그 회사의 채용 홈페이지에 들어가서 /robots.txt 검색 후 내용에 그리팅하이어에서 제작하였다는
# 문구가 적혀있으면 찾았다.
# 구글이나 빙의 검색 서비스를 이용하지 않고 회사의 채용 홈페이지를 어떻게 자동으로 찾을 수 있을까?
import requests
def checkPage(pageUrl):
    global pages
    try:
        response = requests.get(pageUrl)
        response.raise_for_status()  # 상태 코드가 200이 아닌 경우 예외 발생
        print("페이지가 존재합니다.")
        pages.add(pageUrl)
        # 여기에 상태 코드가 200인 경우 수행하고자 하는 동작을 추가하세요.
    except requests.exceptions.HTTPError as e:
        print("페이지가 존재하지 않습니다. 상태 코드:", e.response.status_code)
    except requests.exceptions.RequestException as e:
        print("오류 발생:", e)

# 회사의 영어 이름은 모두 12자리이내라고 가정하자.
def makeUrl(defaultPageUrl):

def findOpenPositionPage(pageUrl):

def storeData():

def getPositionData(pageUrl):

def accessPages(pages):


def main():
    pages = set()
    makeUrl("https://*.career.greetinghr.com")