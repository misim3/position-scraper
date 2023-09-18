# https://classum.career.greetinghr.com
# */robots.txt -> 구글이나 빙의 검색 서비스를 이용해서 회사의 공고를 찾으면 안된다.
# 정말 url의 조합을 통해 회사 홈페이지를 찾아야 한다.
# 그러므로 일단 맨 위의 형식과 같은 홈페이지부터 찾아보자.
# 위의 url 형식을 사용하지 않고 그리팅하이어의 서비스를 이용하는 경우에는 어떻게 찾을 수 있을까?
# 그 회사의 채용 홈페이지에 들어가서 /robots.txt 검색 후 내용에 그리팅하이어에서 제작하였다는
# 문구가 적혀있으면 찾았다.
# 구글이나 빙의 검색 서비스를 이용하지 않고 회사의 채용 홈페이지를 어떻게 자동으로 찾을 수 있을까?
import requests # request에 대한 이해도 필요
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

pages = set()

# 아래의 checkPage의 과정이 그리팅 하이어 서버에 부하를 주는가? 에 대한 정보가 필요하다.
# 엄청난 부하를 준다. 죄송하네.. 없는 페이지의 정보를 요청하는 것도 부하를 가한다... 큰일이네.
# gpt의 대답에 의하면, 서버에 부하를 가하지 않고 페이지의 존재 유무를 파악할 수 있는 방법은 없다고 한다.
# 그래서 요청 최적화, 요청 주기 조절하는 방식으로 부하 최소화해야 한다.
# requests.get보다 requests.head를 사용하라고 하던데 왜 그런지 자세히 알아보자.
# python module인 requests의 코드를 살펴보니 urlopen을 이용해서 데이터를 요청한다.
# 그러면 urlopen과 requests의 차이점은 뭐냐하면, requests가 사용자를 위한 전처리가 되어있다는 점이다.
# 여기서 전처리라 함은 예외처리나 나같은 아마추어가 생각하지 못하는 부분에 대한 처리를 의미한다.
# 추가적으로 urlopen에서의 get과 head의 차이?
# 추가적으로 urlopen의 코드?
def checkPage(pageUrl):
    global pages
    try:
        #response = requests.get(pageUrl)
        response.raise_for_status()  # 상태 코드가 200이 아닌 경우 예외 발생
        print("페이지가 존재합니다.")
        pages.add(pageUrl)
        # 여기에 상태 코드가 200인 경우 수행하고자 하는 동작을 추가하세요.
    except requests.exceptions.HTTPError as e:
        print("페이지가 존재하지 않습니다. 상태 코드:", e.response.status_code)
    except requests.exceptions.RequestException as e:
        print("오류 발생:", e)

# 회사의 영어 이름은 모두 12자리이내라고 가정하자.
# 재귀 12번 실행하면서 26자리의 알파벳을 반복한다. => 엄청난 비효율 26**12 = 95,428,956,661,682,176
# 이 엄청난 비효율을 어떻게 해소할 수 있을까?

def makeUrl(pageUrl, n):
    # 도메인 이름은 대소문자 구분이 없기 때문에 소문자만 사용한다.
    # '', ""의 차이
    letters = 'abcdefghijklmnopqrstuvwxyz'
    if n < 2:
        for i in letters:
            makeUrl(pageUrl + i, n + 1)
            #checkPage(pageUrl + '.career.greetinghr.com')

def findOpenPositionPage(pageUrl):
    driver = webdriver.Edge()
    driver.get(pageUrl)
    details = driver.find_elements(By.TAG_NAME, "a")
    urls = []
    for d in details:
        urls.append(d.get_attribute('href'))
    for u in urls:
        if "apply" or "career" in u:
            getPositionData(u)
    driver.quit()

def getPositionData(pageUrl):
    #동시에 driver 사용이 불가능하다.
    #따라서 병렬 처리를 해주거나 아예 다른 방법을 사용해야 한다.
    #requests와 selenium을 이용한 방식 등 에 대해 자세히 알아볼 필요가 있다.
    driver = webdriver.Edge()
    driver.get(pageUrl)
    details = driver.find_elements(By.TAG_NAME, "a")
    position_url = driver.current_url + 'o/'
    urls = []
    for d in details:
        urls.append(d.get_attribute('href'))
    for u in urls:
        if position_url in u:
            driver.get(u)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            print(soup.title.get_text())
            driver.back()
    driver.quit()

def accessPages(pages):
    for page in pages:
        findOpenPositionPage(page)

def main():
    #makeUrl("https://", 0)
    #print("done makeUrl!")
    pages.add("https://classum.career.greetinghr.com")
    accessPages(pages)
    print("done accessPages!")

if __name__ == "__main__":
    main()