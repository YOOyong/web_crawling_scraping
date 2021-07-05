import time
import selenium.webdriver as webdriver
import sys


driver = webdriver.Chrome("C://chromedriver/chromedriver.exe")
url_start = 'https://news.naver.com'
end_page = 3
#값을 입력받도록 만들기. 실행 명령시에 입력받는다.
# if len(sys.argv) == 3:
#     end_page = int(sys.argv[2]) + 1
# elif len(sys.argv) == 2:
#     keywords = list(sys.argv[1].split(','))
# else:
#     keywords = ['킥보드', '자전거']
keywords = ['킥보드', '자전거']
#sys argv 는 기본적으로 값을 하나 가지고 있음
#sys argv가 2이상이라는 소리는 값을 받았다는 의미.

def input_keyword(keyword):
    driver.switch_to.window(driver.window_handles[0])
    driver.get(url_start)

    driver.implicitly_wait(10)  #implicity wait 는 로딩이 끝나면 자동으로 넘어감. 무조건 10초 기다리는 것이 아님.
                                #어디서 로딩이 발생할지 모르기 떄문에 액션마다 넣었다.
    driver.find_element_by_xpath('//input[@class="text_index"]').send_keys(keyword)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(10)
    driver.find_elements_by_xpath('//a[@role="option"]')[1].click()
    driver.implicitly_wait(10)

    return driver


def make_file(keyword):
    output_file = 'naver_news_' + keyword + "_" + time.strftime("%y%m%d_%H%M%S")+ '.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\t{}\n".format('페이지','키워드','제목', 'URL'))

    return output_file

def write_news(i, keyword, news_title_clean, news_url, output_file):
    print([i, keyword, news_title_clean, news_url])
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\t{}\n".format(i, keyword, news_title_clean,news_url))

    return

def crawl_news_selenium(driver, keyword, i, output_file):
    bodies = driver.find_elements_by_xpath('//ul[@class="list_news"]/li')

    for body in bodies:
        news_title_elm = body.find_elements_by_xpath('.//a[@class="news_tit"]')[0]
        news_title = news_title_elm.get_attribute('title')
        try:
            news_url_elm = body.find_elements_by_xpath('.//a[@class="info"]')[0]
            news_url = news_url_elm.get_attribute('href')
        except:
            news_url = ''

        news_title_clean = news_title.replace('\n', ' ').replace('\t',' ').replace('\r',' ').strip()
        write_news(i, keyword, news_title_clean, news_url, output_file)

    page_nav = driver.find_element_by_xpath('//div[@class="sc_page_inner"]')
    next_page = page_nav.find_element_by_link_text(str(int(i)+1)) #a 태그 사이에 있는 문자열을 선택. 여기선 페이지 번호
    next_page.click()
    driver.implicitly_wait(10)

    return


def main():
    for keyword in keywords:
        output_file = make_file(keyword)
        driver = input_keyword(keyword)

        for i in range(1,2 ):
            print(i)
            crawl_news_selenium(driver, keyword, i, output_file)
            time.sleep(6)

        driver.close()
    driver.quit() # close() 와 quit()의 차이
    return

main()
