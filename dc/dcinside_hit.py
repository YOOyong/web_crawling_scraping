import requests
from lxml import html


def create_article_urls_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\n".format('제목', '시간', 'url'))

    return filename

def crete_article_contents_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('제목','글쓴이','시간', '내용', 'url', '조회수', '추천수', '댓글수'))

    return filename

def crawl_article_urls(filename, page):
    #get article urls
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    for i in range(1, page+1):
        URL = 'https://gall.dcinside.com/board/lists/?id=hit&page=' + str(i)
        html_req = requests.get(URL, headers = headers)
        tree = html.fromstring(html_req.content)

        articles = tree.xpath('//tbody/tr[@class="ub-content us-post"]')
        with open(filename, 'a', encoding='utf-8') as f:
            for article in articles:
                title = article.xpath('.//td[@class="gall_tit ub-word"]/a/text()')[0].replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
                date = article.xpath('.//td[@class="gall_date"]/text()')[0]
                url = article.xpath('.//td[@class="gall_tit ub-word"]/a/@href')[0]
                url = 'https://gall.dcinside.com' + url
                print(title, date, url)
                f.write("{}\t{}\t{}\n".format(title, date, url))

#create_article_urls_file('test.txt')
# crawl_article_urls('test.txt', 5)

def get_article_url_list(filename):
    urls = []
    with open(filename, 'r', encoding='utf-8') as f:
        input_text = f.read()
        articles = input_text.splitlines()

    for article in articles:
        elements = article.strip().split('\t')
        urls.append(elements[2])

    return urls[1:]

def crawl_article_contents(filename, urls):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    for url in urls:
        html_req = requests.get(url, headers= headers)
        tree = html.fromstring(html_req.content)

        #title,date,content,url
        title = tree.xpath('//span[@class="title_subject"]/text()')[0]
        date = tree.xpath('//span[@class="gall_date"]/@title')[0]
        writer = tree.xpath('//span[@class="nickname in]/@title')
        content = tree.xpath('//div[@class="write_div"]/descendant-or-self::text()')
        content = " ".join(content).replace("\n"," ").replace("\t"," ").replace("\r"," ").strip()
        view_count = tree.xpath('//span[@class="gall_count"]/text()')[0].replace('조희 ', '')
        like_count = tree.xpath('//span[@class="gall_reply_num"]/text()')[0].replace('조희 ', '')
        comment_count = tree.xpath('//span[@class="gall_comment"]/a/text()')[0].replace('조희 ', '')
        print(title,date,content)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(title,writer ,date, content, url, view_count, like_count,comment_count))

def main():
    url_list_filename = create_article_urls_file('test.txt')
    contents_filename = crete_article_contents_file('dc_hit.txt')

    #url 크롤링
    crawl_article_urls(url_list_filename, 1)
    url_list = get_article_url_list(url_list_filename)

    #내용 포함 크롤링
    crawl_article_contents(contents_filename, url_list)


main()