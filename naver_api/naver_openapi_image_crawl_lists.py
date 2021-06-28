import requests
import time
import json

project = 'naver_openapi_image'
keyword = '킥보드'
display = 10
sort = 'date'

image_path = 'images/'

output_file_name = project + "_list_" + time.strftime("%y%m%d_%H%M%S") + '.txt'
output_file = open(output_file_name, "w", encoding="utf-8")
output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('start', 'num', 'title', 'link', 'thumbnail', 'sizeheight', 'sizewidth'))
output_file.close()


def fwrite_news(start, num, title, link, thumbnail, sizeheight, sizewidth):
    print([start, num, title, link, thumbnail, sizeheight, sizewidth])
    output_file = open(output_file_name, "a", encoding="utf-8")
    output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(start, num, title, link, thumbnail, sizeheight, sizewidth))
    return


def fcrawl_news(start):

    url = 'https://openapi.naver.com/v1/search/image?query='+keyword+'&display='+str(display)+'&start='+str(start)+'&sort='+sort
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'X-Naver-Client-Id': '3Ba7woBMp4X0FH6YGvwp',
               'X-Naver-Client-Secret': 'E_VqtPnNk7'}
    response = requests.get(url, headers=headers)
    elements = json.loads(response.text)['items']
    # elements = tree.iter(tag="items")

    print(len(elements))
    print(elements)

    num = display * (start - 1)

    for element in elements:
        num += 1
        try:
            title = element['title']
            link = element['link']
            thumbnail = element['thumbnail']
            sizeheight = element['sizeheight']
            sizewidth = element['sizewidth']
            image_file_name = link.split('/')[-1]

            img = requests.get(link).content
            open(image_path+str(start)+'_'+str(num)+'_'+image_file_name, 'wb').write(img)
            time.sleep(1)

            fwrite_news(start, num, title, link, thumbnail, sizeheight, sizewidth)
        except:
            continue

    output_file.close()

    return


def fmain():
    for start in range(1, 3):
        print(start)
        fcrawl_news(start)
        time.sleep(6)

fmain()