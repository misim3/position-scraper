# https://classum.career.greetinghr.com
# */robots.txt -> 구글이나 빙의 검색 서비스를 이용해서 회사의 공고를 찾으면 안된다.
# 정말 url의 조합을 통해 회사 홈페이지를 찾아야 한다.
# 그러므로 일단 맨 위의 형식과 같은 홈페이지부터 찾아보자.
# 위의 url 형식을 사용하지 않고 그리팅하이어의 서비스를 이용하는 경우에는 어떻게 찾을 수 있을까?
# 그 회사의 채용 홈페이지에 들어가서 /robots.txt 검색 후 내용에 그리팅하이어에서 제작하였다는
# 문구가 적혀있으면 찾았다.
# 구글이나 빙의 검색 서비스를 이용하지 않고 회사의 채용 홈페이지를 어떻게 자동으로 찾을 수 있을까?
import re
import requests # request에 대한 이해도 필요
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import mysql.connector

# 아래의 checkPage의 과정이 그리팅 하이어 서버에 부하를 주는가? 에 대한 정보가 필요하다.
# 엄청난 부하를 준다. 죄송하네.. 없는 페이지의 정보를 요청하는 것도 부하를 가한다... 큰일이네.
# gpt의 대답에 의하면, 서버에 부하를 가하지 않고 페이지의 존재 유무를 파악할 수 있는 방법은 없다고 한다.
# 그래서 요청 최적화, 요청 주기 조절하는 방식으로 부하 최소화해야 한다.
# requests.get보다 requests.head를 사용하라고 하던데 왜 그런지 자세히 알아보자.
# python module인 requests의 코드를 살펴보니 urlopen을 이용해서 데이터를 요청한다.
# 그러면 urlopen과 requests의 차이점은 뭐냐하면, requests가 사용자를 위한 전처리가 되어있다는 점이다.
# 여기서 전처리라 함은 예외처리나 나같은 아마추어가 생각하지 못하는 부분에 대한 처리를 의미한다.
# 추가적으로 urlopen에서의 get과 head의 차이?
# head는 메타데이터와 같은 get보다 더 적은 양의 데이터를 요청하기 때문에 head로 페이지가 존재하는지 확인하는 게 좋다.
# 추가적으로 urlopen의 코드?
# 결국 http connection pool의 send 메소드로 이어진다.
# http connection pool의 여러 장점이 있다. 그리고 이번 프로젝트의 경우 한 서버에서만 요청을 하기 때문에, 부합한다.
# @추가적으로 고려해야하는 것은 26**12의 경우를 어느정도의 페이지를 어떤 주기로 확인해야하는지이다.

pages = set()

def loadUrlDb():
    global pages
    cnx = mysql.connector.connect(user='', password='', host='', database='')
    cursor = cnx.cursor()

    query = ("SELECT url FROM pages ")

    # Insert new employee
    cursor.execute(query)

    for url in cursor:
        pages.add(url)

    cursor.close()
    cnx.close()

def checkPage(pageUrl):
    try:
        response = requests.head(pageUrl)
        response.raise_for_status()  # 상태 코드가 200이 아닌 경우 예외 발생
        print("페이지가 존재합니다.")
        # storeUrl(pageUrl)
        # 여기에 상태 코드가 200인 경우 수행하고자 하는 동작을 추가하세요.
    except requests.exceptions.HTTPError as e:
        print("페이지가 존재하지 않습니다. 상태 코드:", e.response.status_code)
    except requests.exceptions.RequestException as e:
        print("오류 발생:", e)

# 회사의 영어 이름은 모두 12자리이내라고 가정하자.
# 재귀 12번 실행하면서 26자리의 알파벳을 반복한다. => 엄청난 비효율 26**12 = 95,428,956,661,682,176
# @이 엄청난 비효율을 어떻게 해소할 수 있을까?
# 추가적으로 존재하는 페이지 정보를 db에 저장하고 새로운 페이지 확인하면 추가하자.
# @그리고 해당 회사의 채용 공고를 확인하는 것에 대한 주기도 따로 고려하자.


# 여기서 문제점이 있다. db에 저장된 url 데이터를 읽고 그것을 제외한 나머지의 페이지만 탐색하려고 했는데,
# 그러면 모든 makePage에 url 데이터를 함께 파라미터로 넣어줘야한다.
# 그러면 엄청난 재귀에서 url 데이터도 함께 하여 또 엄청난 비효율이 발생한다.
# 읽어온 url 데이터를 글로벌 변수로 만들어서 makePage에서 url 데이터에 이미 존재하는 url은 제외시키고 checkPage를 호출하자.
def storeUrl(page):
    cnx = mysql.connector.connect(user='', password='', host='', database='')
    cursor = cnx.cursor()

    add_page = ("INSERT INTO pages "
                    "(url) "
                    "VALUES (%s)")

    # Insert new employee
    cursor.execute(add_page, page)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def makeUrl(pageUrl, n):
    # 도메인 이름은 대소문자 구분이 없기 때문에 소문자만 사용한다.
    # '', ""의 차이
    letters = 'abcdefghijklmnopqrstuvwxyz'
    if n < 12:
        for i in letters:
            makeUrl(pageUrl + i, n + 1)
            # if pageUrl not in pages:
                # checkPage(pageUrl + '.career.greetinghr.com')

def findOpenPositionPage(pageUrl):
    html = requests.get(pageUrl)
    bs = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'.*(apply|career).*')
    # findAll이 아닌 이유는 그리팅 하이어 서비스의 경우 여러 페이지에서 공고를 확인할 수 있다.
    # 따라서 걸리는 것 하나에서만 찾으면 된다.
    # apply나 career 페이지가 없고 바로 공고만 존재하는 경우는 어떻게 처리할 것인지 고려
    link = bs.find('a', href=pattern)
    if link:
        getPositionData(link)
    else:
        getPositionData(pageUrl)

def getPositionData(pageUrl):
    # 동시에 driver 사용이 불가능하다.
    # 따라서 병렬 처리를 해주거나 아예 다른 방법을 사용해야 한다. -> 기존에는 findOpenPositionData와 getPositionData가 모두 selenium을
    # 사용했었는데, findOpenPositionData를 requests로 변경했다.
    # requests와 selenium을 이용한 방식 등 에 대해 자세히 알아볼 필요가 있다.
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
            # data = {
            #   'company': company,
            #   'name': name,
            #   'experience': experience,
            #   'type': type,
            #   'url': url,
            # }
            # storePositionData(data)
            driver.back()
    driver.quit()

def storePositionData(data_position):
    cnx = mysql.connector.connect(user='', password='', host='', database='')
    cursor = cnx.cursor()

    add_position = ("INSERT INTO positions "
                    "(company, name, experience, type, url) "
                    "VALUES (%s, %s, %s, %s, %s)")

    # Insert new employee
    cursor.execute(add_position, data_position)
    # emp_no = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def accessPages(pages):
    for page in pages:
        findOpenPositionPage(page)

def main():
    # loadUrlDb()
    # makeUrl("https://", 0)
    # print("done makeUrl!")
    page_classum = 'https://classum.career.greetinghr.com'
    accessPages(page_classum)
    print("done accessPages!")

if __name__ == '__main__':
    main()

# @자바스크립트를 실행할 수 있는 크롤러(상대적으로 페이지 처리 시간 길고, 메모리 소비가 크다) vs 없는 크롤러
# @병렬 처리를 통해 처리 속도 향상, 데이터 저장 관련 속도 문제 고려
# @robots.txt, robots meta 태그, xml 사이트맵과 사이트맵 인덱스(robots.txt의 Sitemap 디렉티브에 적혀있다.)
# @동시 접속 최대 6개(병렬 처리시 최대 6개), 최소 요청 간격 1초, robots.txt의 Crawl-delay 디렉티브 = 크롤링 시간 간격
# @최대한 html 추출 외의 수단 사용, cache
# @크롤러 내 연락처 명시
# @상태코드와 오류 처리 - http 통신 오류 대처

# @다 제끼고 일단 시간을 정해야 한다. makeUrl에서 만든 주소에 페이지가 존재하는지 확인하는 시간 간격 + 실존 페이지에 접근해서 채용 공고를
# @채용 공고를 가져오는 시간 간격. 모두 1초로 하자.
# @일단 12자리 말고 4자리로 해서 db에 저장하고 거기서 존재하는 페이지만 출력하는 것을 목표로 10월 전에 배포하자.
# @ 1번 클라썸 채용 공고 페이지에서 필요한 데이터 가져오는 코드 완성
# @ 2번 가져온 데이터 db에 저장하는 코드 완성
# @ 3번 db에 저장된 데이터 웹에 리스트로 출력하는 spring 코드 완성(필요없는 거 쳐내) - front도 포함
# @ 4번 aws rds 데이터베이스 연결
# @ 5번 배포.