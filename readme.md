# **웹 크롤링 스크레이핑**

#### **시작전**
domain.com/robots.txt를 한 번 확인해보자.

## **Xpath**  
###기본 표현법
- **nodename** : 노드명이 nodename인 노드 선택  
- **//** : 문서 전체에서 찾기  
- **/** :  root 노드로 부터 선택(하위에서 찾기)  
- **.**: 현재 노드 선택  
- **..** : 부모 노드 선택  
- **.//** : 선택된 문서 부분에서 찾기
- **@** : 현재 노드의 속성 선택  

ex) `div[@class="descriptions-inner"]div[@class="name"]/text() `

**`a/text()`** : tag a 밑에 있는 텍스트  
**`a/@href`** : tag a의 href 속성의 값  
**`a/descendant-or-self::text()`** : tag a 밑에 있는 모든 텍스트 (a 하위에 복잡한 구조일 때)  
**`a/descendant-or-self::text()[not(ancestor::script)]`** : tag a 밑에 있는 모든 텍스트 중 script tag는 제외하고 가져옴  
**`a/descendant-or-self::text()[not(ancestor::script or ancestor::style)]`** : 위에서 or로 조건 추가  

# 네이버 뉴스 예제
네이버 뉴스에서 뉴스를 검색  
검색 결과 중 네이버뉴스 링크가 있는 기사들의 링크를 수집.
각 링크에서 본문 수집.   
list 우선 수집후 detail 수집  
>예제코드
```python
import requests
from lxml import html

url = 'https://news.naver.com'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
html_req = requests.get(url, headers=headers)

tree = html.fromstring(html_req.content)
titles = tree.xpath('//div[@class = "hdline_article_tit"]/a/text()')

results = []
test = []
for title in titles:
    title_clean = title.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()  # 새줄, 탭, 새 문단 태글를 없앤다.
    results.append(title_clean)

print(len(results))
for i in range(len(results)):
    print(results[i])
```
  
**코드 부분 설명**
```python
tree = html.fromstring(html_req.content)
titles = tree.xpath('//div[@class = "hdline_article_tit"]/a/text()')
```
1. `html.fromstring()` : 문서의 내용을 html 구조로 해석  
2. `html_req.content()` : encoding 하지 않은 상태의 수집문서  
*cf)* `html_req.text()` : 자동으로 encoding 결과를 가져오나 오류가 발생할 수 있어 .content 사용이 일반적  
3. `tree.xpath` : tree 내용 중에서 xpath 규칙에 맞는 부분 추출  
4. `title_clean = title.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()`  
    글에서 띄어쓰기 tab 등을 공백으로 치환하고 앞 뒤 공백을 자른다.   
    
  


## 3.1 기사 list 수집  
1. 글목록 페이지에서 우선 각 글목록 리스트를 추출한 후
2. 각 글목록 덩어리 안에서 '글제목'과 '본문 url'을 `for loop`으로 추출합니다.  
리스트 단위를 적절히 설정해야 누락값이 있을시 데이터가 섞이는걸 방지합니다.
  
>예제코드
```python
keyword = '코로나'
page_num = 1

url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=' + keyword + '&sort=1&photo=0\
    &field=0&pd=3&ds=2021.01.01&de=2021.05.31&mynews=0&office_type=0&office_section_code=0&news_office_checked=\
    &nso=so:dd,p:from20210101to20210531,a:all&start='+str(page_num)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
html_req = requests.get(url, headers=headers)
tree = html.fromstring(html_req.content)
titles = tree.xpath('//div[@class="title"]/p[@class="tit"]/a[@class="best-title"]/text()')

bodies = tree.xpath('//ul[@class="list_news"]/li')
print(len(bodies))

results = []

for body in bodies:
    #.이 있는것에 유의. 전체 문서가 아닌 덩어리에서만 가져온다는 뜻.
    news_title = body.xpath('.//a[@class="news_tit"]/@title')[0] #속성으로 값이 있으면 속성으로 가져오는것이 좋다.
    news_date = body.xpath('.//span[@class="info"]/text()')[0]
    try:
        news_url = body.xpath('.//a[@class="info"]/@href')[0]
    except:
        news_url = ''
    news_title_clean = news_title.replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
    news_date_clean = news_date.replace(".", "")
    results.append((news_title_clean, news_date_clean, news_url))

print(results)
```
  
`bodies = tree.xpath('//ul[@class="list_news"]/li')` 를 통해 기사리스트 단위로 가져올 준비를 함  
`for loop`를 돌면서 각 기사별로 정보 수집  
```python
try:
    news_url = body.xpath('.//a[@class="info"]/@href')[0]
except:
    news_url = ''
```
네이버링크가 없는 기사를 처리해준다.  
프로젝트에 따라 사용가능 하긴 함. ex) 화면 캡쳐 가능.
# 기사 Detail 수집  
\-




# API 활용
## 공공데이터 포털 API 연결 및 데이터 수집
API는 request와 response 형태로 통신한다  

\-
  
# Selenium 

위 lxml 예제에선 xpath를 사용해 정보를 가져옴 (선택 == 정보를 가져온다)  
선택과 동작이 분리되어있지 않음  
   
- 정보를 가져옴  
- 정보를 입력함.  
- 캡쳐, 클릭, 스크롤등 동작 가능   
  
xpath로 위치를 찾고 위 동작들을 수행 가능  
선택과 액션이 분리되어있음  


# selenium  
# Browser navigation  
  
**이동하기**  
```python
driver.get('https://selenium.dev')
```
  
**현재 주소 가져오기**  
```python
driver.current_url 
```

**뒤로가기/ 앞으로가기**  
```python
driver.back()
driver.forward()
```
  
**새로고침**  
```
driver.refresh()
```  
  
# Windows and tabs  
webDriver는 창과 탭을 구분하지 않는다.  
  
**현재 창 핸들 가져오기(ID)**  
```python
driver.current_window_handle
```  
  
**탭 변경하기**  
webDriver는 현재 os에서 active중인 창을 모르기 떄문에 탭을 이동하는 명령이 필요하다.  
`driver.switch_to.window(window_handle)`   
*ex)*
```python
# Open URL
driver.get("https://seleniumhq.github.io")

# Store the ID of the original window
original_window = driver.current_window_handle

# Click the link which opens in a new window
driver.find_element(By.LINK_TEXT, "new window").click()

# Loop through until we find a new window handle
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break
```

**탭 생성하며 변경하기**  
```python
# Opens a new tab and switches to new tab
driver.switch_to.new_window('tab')

# Opens a new window and switches to new window
driver.switch_to.new_window('window')
```

**탭 닫기**
```python
#Close the tab or window
driver.close()

#Switch back to the old tab or window
driver.switch_to.window(original_window)
```
탭을 닫고 핸들러를 옮겨주는걸 잊지 말자  
옮기지 않으면 `No Such Window Exception`이 발생한다.  
  
**세션 마지막에 브라우저 종료**  
```python
driver.quit()
```
- WebDriver와 관련된 모든 탭과 창이 닫힌다.  
- driver process를 닫는다.  
- background driver process를 닫는다. 
- Gird에 brower가 더 이상 쓰이지 않는다고 알린다. (selenium gird를 사용하는 경우)
  
quit 실패는 background process를 남기고 이는 나중에 문제가 될 수 있다. 다음 코드를 고려해볼 수 있다.  
```python
try:
    #do something
finally:
    driver.quit()

#selenium support python context manager
with webdriver.Firefox() as driver:
    #do something

# WebDriver will automatically quit after indentation
```

**Frames, Iframes**
```html
<div id="modal">
  <iframe id="buttonframe" name="myframe"  src="https://seleniumhq.github.io">
   <button>Click here</button>
 </iframe>
</div>
```
```python
#WebElement 사용
iframe = driver.find_element(By.CSS_SELECTOR, "#modal > iframe")
driver.switch_to.frame(iframe)
driver.find_element(By.TAG_NAME, 'button').click()

#name ID 사용
dirver.switch_to.frame('buttonframe')
driver.find_element(By.TAG_NAME, 'button').click()
```
**frame 빠져 나오기**  
`driver.switch_to.default_content()`  


# Locating elements  
**id로 찾기**
```python
cheese = driver.find_element(By.ID, "cheese")
cheddar = cheese.find_elements_by_id('cheddar')
```
|Locator|Description|
|-------|-----------|
|class name|Locates elements whose class name contains the search value (compound class names are not permitted)
|css selector|Locates elements matching a CSS selector|
|id|Locates elements whose ID attribute matches the search value|
|name|Locates elements whose NAME attribute matches the search value|
|link text|Locates anchor elements whose visible text matches the search value|
|partial link  text|Locates anchor elements whose visible text contains the search value.  If multiple elements are matching, only the first one will be selected.|
|tag name|Locates elements whose tag name matches the search value|
|xpath|Locates elements matching an XPath expression|
---
- id는 페이지 내에서 유니크한 값이기에 원하는 element를 찾기 가장 좋다.
- xpath는 범용성이 좋아 보통 각 브라우저에서 퍼포먼스 테스트를 하지 않아 약간 느린 경항이 있다. 
- tag name 페이지 내에 중복되는 부분이 많으므로 쓰지 않는 편이 좋다. 
- locator를 단순하고 읽기 쉽도록 하라.
- 탐색범위를 좁히는 편이 좋다.
 
 






















