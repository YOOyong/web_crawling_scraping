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
> list 우선 수집후 detail 수집.
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
    
  


##리스트 단위로 수집  
1. 글목록 페이지에서 우선 각 글목록 리스트를 추출한 후
2. 각 글목록 덩어리 안에서 '글제목'과 '본문 url'을 `for loop`으로 추출합니다.
> 리스트 단위를 적절히 설정해야 누락값이 있을시 데이터가 섞이는걸 방지합니다.
  
코드
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
```
try:
    news_url = body.xpath('.//a[@class="info"]/@href')[0]
except:
    news_url = ''
```
네이버링크가 없는 기사를 처리해준다.  

셀레니움은 학습용, 속도, 붙이기도 애매하여 실무에선 잘 쓰지 않는다  
프로젝트에 따라 사용가능 하긴 함. ex) 화면 캡쳐 가능.
# ---페이지 내용 추후 정리--
### pass


# API 활용
## 공공데이터 포털 API 연결 및 데이터 수집
API는 request와 response 형태로 통신한다  

- 정부api 쓸 때는 sleep 안줘도 됨.  
  

#Selenium 

위 lxml 예제에선 xpath를 사용해 정보를 가져옴 (선택 == 정보를 가져온다)  

selenium  
- 정보를 가져옴  
- 정보를 입력함.  
- 캡쳐도 됨  
- 클릭, 스크롤 가능  
  
xpath로 위치를 찾고 위 동작들을 수행 가능  
선택과 액션이 분리되어있음  
 
 






















