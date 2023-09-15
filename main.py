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
# 재귀 12번 실행하면서 26자리의 알파벳을 반복한다. => 엄청난 비효율
# 이 엄청난 비효율을 어떻게 해소할 수 있을까?
def makeUrl(pageUrl, n):
    # 도메인 이름은 대소문자 구분이 없기 때문에 소문자만 사용한다.
    # '', ""의 차이
    letters = 'abcdefghijklmnopqrstuvwxyz'
    if n > 12:
        return # 파이썬에서 종료는 어떻게 하지?
    for i in letters:
        makeUrl(pageUrl + i, n + 1)
        checkPage(pageUrl + '.career.greetinghr.com')

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
    makeUrl("https://", 0)
    accessPages(pages)

if __name__ == "__main__":
    main()