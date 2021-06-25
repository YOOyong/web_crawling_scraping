import requests
from lxml import html
import time
# url = 'http://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=005930'
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
#             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
# html_req = requests.get(url, headers=headers)
#
# tree = html.fromstring(html_req.content)
# titles = tree.xpath('//div[@class="title"]/p[@class="tit"]/a[@class="best-title"]/text()')

# results = []
# test = []
# for title in titles:
#     title_clean = title.replace("\n", "").replace("\t", "").replace("\r", " ").strip()  # 새줄, 탭, 새 문단 태글를 없앤다.
#     results.append(title_clean)
#
# print(len(results))
# for i in range(len(results)):
#     print(results[i])


# //div[@class="descriptions-inner"]/div[@class="name"]/text() 쿠팡 킥보드
# //div[@class="bl_subject"]/a/text()  국민청원
# //ul[@id="basic1"]/li/dl/dt/a/text() 네이버 지식인 킥보드 <b> 태그 처리 방법은?
# //div[@class="title"]/p[@class="tit"]/a[@class="best-title"]/text() 팍스넷 종목토론
def create_file(keyword):
    output_file_name = 'naver_news_' + keyword +'_'+time.strftime("%y%m%d_%H%M%S") + '.txt'
    with open(output_file_name, "w", encoding ="utf-8") as f:
        f.write("{}\t{}\t{}\t{}\n".format('페이지', '키워드', '제목', 'url'))
    return output_file_name

def write_news(i, keyword, news_title_clean, news_url, output_file_name):
    with open(output_file_name, "a", encoding='utf-8') as f:
        f.write("{}\t{}\t{}\t{}\n".format(i, keyword, news_title_clean, news_url))
    return

# 네이버 뉴스 리스트 가져오기
def crawl_news(keyword, page_num, output_file_name):
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=' + keyword + '&sort=1&photo=0\
        &field=0&pd=3&ds=2021.01.01&de=2021.05.31&mynews=0&office_type=0&office_section_code=0&news_office_checked=\
        &nso=so:dd,p:from20210101to20210531,a:all&start='+str((page_num - 1) * 10 + 1)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    html_req = requests.get(url, headers=headers)
    tree = html.fromstring(html_req.content)
    titles = tree.xpath('//div[@class="title"]/p[@class="tit"]/a[@class="best-title"]/text()')

    bodies = tree.xpath('//ul[@class="list_news"]/li')
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
        write_news(page_num, keyword, news_title_clean, news_url, output_file_name)
    return results


#keywords = ['킥보드', '자전거']
#result_dict = {'킥보드':[], '자전거': []}
keywords = list(input("키워드 입력, 띄어쓰기 구분 : ").split())
end_page = input("어느 페이지 까지? : ")


for key in keywords:
    output_file_name = create_file(key)
    for i in range(1, int(end_page)):
        # result_dict[key].extend(crawl_news(key, i, output_file_name))
        crawl_news(key, i, output_file_name)

    # for k, v in result_dict.items():
    #     print(f"\n{k} 키워드 크롤링 결과\n")
    #     for article in v:
    #         print(article)