import requests
from lxml import html

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

def create_article_urls_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\n".format('제목', '시간', 'url'))

    return filename

def create_article_content_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('제목','시간', '내용', 'url', '조회수', '추천수', '댓글수'))

    return filename

def crawl_article_urls(filename, page):
    for i in range(1, page+1):
        URL = 'https://pann.nate.com/talk/c20048?page=' + str(page)
        html_req = requests.get(URL, headers=headers)   
        tree = html.fromstring(html_req.content)

        articles = tree.xpath('//table[@class="talk_list"]/tbody/tr')

        with open(filename, 'a',encoding='utf-8') as f:
            for article in articles:
                try:
                    title = article.xpath('.//td[@class="subject"]/a/b/text()')[0].replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
                except:
                    title = article.xpath('.//td[@class="subject"]/a/text()')[0].replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()

                date = article.xpath('.//td[4]/text()')[0]  #xpath 안에서 인덱스는 1부터 시작한다.
                url = article.xpath('.//td[@class="subject"]/a/@href')[0]
                url = 'https://pann.nate.com' + url
                print(title, date, url)

                f.write("{}\t{}\t{}\n".format(title, date, url))

def get_article_url_list(filename):
    urls = []
    with open(filename, 'r', encoding='utf-8') as f:
        input_text = f.read()
        articles = input_text.splitlines()

    for article in articles:
        elements = article.strip().split('\t')
        urls.append(elements[2])

    return urls[1:]

def crawl_article_content(filename, urls):
    for url in urls:
        html_req = requests.get(url, headers=headers)
        tree = html.fromstring(html_req.content)

        title = tree.xpath('//h4/@title')[0]
        date = tree.xpath('//div[@class="info"]/span[@class="date"]/text()')[0]
        view_count = tree.xpath('//div[@class="info"]/span[@class="count"]/text()')[0].replace('"', '')
        content = tree.xpath('//div[@id="contentArea"]/descendant-or-self::text()')
        content = " ".join(content).replace("\n"," ").replace("\t"," ").replace("\r"," ").strip()
        like_count = tree.xpath('//div[@class="updown f_clear"]/div/div/span/text()')[0]
        comment_count = tree.xpath('//div[@class="cmt_tit"]/span/strong/text()')[0]

        print(title, url, view_count, like_count, comment_count)

        with open(filename, 'a',encoding='utf-8') as f:
            f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(title,date,content,url,view_count,like_count,comment_count))


def main():
    url_file_name = create_article_urls_file('test.txt')
    #글 주소를 크롤링하여 저장.
    crawl_article_urls(url_file_name, 1)

    pann_file_name = create_article_content_file('pann_con.txt')

    #글을 순회하면서 본문 저장.
    crawl_article_content(pann_file_name, get_article_url_list(url_file_name))


main()