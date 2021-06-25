import requests
import time
from xml.etree import ElementTree   #xml 파싱
from datetime import date
from dateutil.relativedelta import relativedelta  #월별 차이를 위한 라이브러리

region_info_file = 'region_code5.csv'
service_key = 'mEy0a05ak8HTdWqQVqABU6LkxP3euL9UVXLP8G5csYgmAfnieV1QR4MVANyAYE%2F7CoWRFoz%2BPL6CPyRncrdS4Q%3D%3D'
date_start = date(2021, 5, 1)
date_end = date(2021, 1, 1)

output_file = 'trade_apt_api_' + \
            time.strftime("%y%m%d_%H%M%S") + '.txt'
with open(output_file, "w", encoding='utf-8') as f:
    f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n"\
            .format('기준년월', '지역명', '지역코드', '법정동', '아파트', '거래금액', '년', '월', '일', '건축년도', '전용면적', '층'))

def get_list():
    """
    region_info_file : .csv
    """
    with open(region_info_file, 'r', encoding='euc-kr') as f:
        input_text = f.read()
        lines = input_text.splitlines()

    lists = []
    for line in lines:
        line = line.replace('"','')
        elms = line.strip().split(",")
        region_name = elms[0]
        region_code = elms[1]
        if region_code[:2] == "11":
            lists.append([region_name, region_code])

    return lists

def get_html(region_name, region_code, this_ym):
    headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD='+ region_code +'&DEAL_YMD=' + this_ym + '&serviceKey=' + service_key
    response = requests.get(url, headers = headers)
    tree = ElementTree.fromstring(response.content)
    elements = tree.iter(tag = "item")

    for element in elements:
        price = element.find("거래금액").text
        const_year = element.find('건축년도').text
        year = element.find('년').text
        month = element.find('월').text
        day = element.find('일').text
        dong = element.find('법정동').text
        apt_name = element.find('아파트').text
        square = element.find('전용면적').text
        stair = element.find('층').text
        elm_list = [this_ym, region_name,region_code, dong, apt_name, price, year, month, day, const_year, square, stair]
        print(elm_list)
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n"\
                    .format(*elm_list))

        return

def main():
    date_this = date_start
    region_infos = get_list()

    while date_this >= date_end:
        print(date_this)
        this_year = str(date_this.year)
        this_month = str(date_this.month)

        if len(this_month) == 1:
            this_month = "0" + str(this_month)

        this_ym = this_year + this_month
        print(this_ym)

        for region_info in region_infos:
            region_name = region_info[0]
            region_code = region_info[1]
            print(region_name, region_code)
            get_html(region_name, region_code, this_ym)

        date_this = date_this - relativedelta(months=1)
    return

main()

