import requests
import json
import time


project = 'naver_openapi_image'
keyword = '킥보드'
display = 10
sort = 'date'

image_path = 'images/'

output_filename = 'test.txt'
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('start', 'num', 'title', 'link', 'thumbnail', 'sizeheight', 'sizewidth'))

def write_news(start, num, title, link, thumbnail, sizeheight, sizewidth):
    print([start,num,title,link,thumbnail,sizeheight, sizewidth])
    with open(output_filename, 'a', encoding='utf-8') as f:
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(start, num, title, link, thumbnail, sizeheight,sizewidth))
    
    return

def crawl_news(start):
    url = 'https://openapi.naver.com/v1/search/image?query='+keyword+'&display='+str(display)+'&start='+str(start)+'&sort='+sort
    print(url)

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'X-Naver-Client-Id': '0o4K8vveWoCmMuBNUFS3',
            'X-Naver-Client-Secret': '2_Exc_E41u'
            }
    response = requests.get(url, headers = headers)
    elements = json.loads(response.content)['items']
    print(len(elements))
    print(elements)

    num = display * (start - 1)

    for element in elements:
        num +=1 
        try:
            title = element['title']
            link = element['link']
            thumbnail = element['thumbnail']
            sizeheight= element['sizeheight']
            sizewidth = element['sizewidth']
            image_file_name = link.split('/')[-1]

            img = requests.get(link).content

            open(image_path+str(start)+'_'+str(num)+'_'+image_file_name, 'wb').write(img)
            time.sleep(1)

            write_news(start, num,title,link,thumbnail,sizeheight,sizewidth)
        except:
            continue
    return
        
def main():
    for start in range(1,2):
        print(start)
        crawl_news(start)
        time.sleep(3)
main()
