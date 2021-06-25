import time
from lxml import html
import requests

keyword = '킥보드'
input_file_name = 'naver_news_킥보드_210625_093422.txt'

output_file_main_name = 'naver_news_main_' + keyword + "_" + time.strftime('%y%m%d_%H%M%S') + ".txt"
with open(output_file_main_name, 'w', encoding='utf-8') as f:
    f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('번호','키워드', '매체', '날짜', '제목', 'url', '본문'))

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

#파일 불러오기
def get_list():
    with open(input_file_name, 'r', encoding='utf-8') as f:
        input_text = f.read()
        lines = input_text.splitlines() # 라인별로 잘라서 리스트로
        lists = []

    for line in lines:
        elms = line.strip().split('\t')
        news_title = elms[2]

        try:
            url = elms[3]
        except:
            url = ''
        lists.append([news_title, url])

    return lists[1:]

def write_news_main(count, news_media, news_date, news_title, news_url, news_article):
    print([count, keyword, news_media, news_date, news_title, news_url, news_article])
    with open(output_file_main_name, 'a', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(count, keyword, news_media, news_date, news_title, news_url, news_article))
    return

def crawl_news_main(count, news_title, news_url):
    html_req = requests.get(news_url, headers = headers)
    tree = html.fromstring(html_req.content)

    try:
        news_media = tree.xpath('//div[@class="press_logo"]/a/img/@alt')[0]
    except:
        news_media = ''
    try:
        news_date = tree.xpath('//div[@class="sponsor"]/span/text()')[0]
    except:
        news_date = ''
    try:
        news_article = tree.xpath('//div[@id="articleBodyContents"]/descendant-or-self::text()[not(ancestor::script)]')
    except:
        news_article = ''

    news_article = " ".join(news_article).replace("\n"," ").replace("\t"," ").replace("\r"," ").strip()
    write_news_main(count, news_media , news_date, news_title, news_url, news_article)

    return

def main():
    lists = get_list()
    count= 1
    for list in lists[:]:
        print(list)
        news_title = list[0]
        news_url = list[1]
        if len(news_url) == 0:
            continue
        crawl_news_main(count, news_title, news_url)
        time.sleep(3)
        count += 1

main()

#엔터기사는 구조가 다르다!! 이름 어떻게 처리할까. 주소는 같으나 엔터기사로 리다이렉트됨








