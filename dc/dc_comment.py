import requests
import json
#post 방식으로 가져오기
#postman 을 사용하면 코드화 하기 편한다.

url = "https://gall.dcinside.com/board/comment/"

payload='id=hit&no=16460&cmt_id=hit&cmt_no=16460&e_s_n_o=3eabc219ebdd65f438&comment_page=1&sort=&GALLTYPE_=G'
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
  'Connection': 'keep-alive',
  'Content-Length': '100',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie': '_ga=GA1.2.1526455112.1577515160; trc_cookie_storage=taboola%2520global%253Auser-id%3De5a52a4a-dff5-471e-b579-0ad4c1ba4c95-tuct5007e19; adfit_sdk_id=22d66a72-a4ca-4694-9c57-4b4303b44ae6; WMONID=K9UDewkwbFS; _cc_id=b08a38ec1b165aa4552d59d9dc21f65c; ck_lately_gall=dx%7Cbp%7CAY%7C3ke%7C1do; panoramaId=46076a47fc0482f838b1ccef4a954945a7025fc9bf1666274dfafdf2b607323b; panoramaId_expiry=1625451465668; last_notice_no=25612; PHPSESSID=92f4b9dd9b21ea218a482592c23caeee; ci_c=34dedbd9d5e522c96b5c9c129ac4bdc6; remember_secret=mQkvMJMJWI; __utma=118540316.1526455112.1577515160.1624852424.1624925835.141; __utmc=118540316; __utmz=118540316.1624925835.141.118.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; wcs_bt=f92eaecbc22aac:1624925843; __utmb=118540316.7.10.1624925835; alarm_popup=1; last_alarm=1624925853; gallRecom=MjAyMS0wNi0yOSAwOToxODoxNC84N2JlZmU2NzFjYjBjNzFjYmFkZDYyODNiOTNmY2U0YzYwZTIxZDUwYzFlOGNlMDA0OTRlZjMwNzMwMjVkMjM5; service_code=21ac6d96ad152e8f15a05b7350a2475909d19bcedeba9d4face8115e9bc1fd4efd6be5d33ba3815c459b467e5c9accf6e66020b7f0326cd249b91335d030e474c2027e4143d09035b9268bd96437458939c9e1439bab5a93a1bdf529ca8404b69c24e156d40b41d18d0ed896c31de3f6acdfbfb1b1f1d05559e6b95e5435976a6d8b7aca26baed9527907f97b3ac7f96bd5bcb0d2229eab553b73bc0e6bdeec2b5a9270596214eed8cb348bd264df1a01260a3cd5422a92c4d7f91ce3a00b3737e800f; sf_ck_tst=test; PHPSESSID=ee375d7f78a17d1d039d483be960e09b; ci_c=5147ee474595c0ddf422b73b97ff28d0',
  'Host': 'gall.dcinside.com',
  'Origin': 'https://gall.dcinside.com',
  'Referer': 'https://gall.dcinside.com/board/view/?id=hit&no=16460&page=1',
  'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
  'sec-ch-ua-mobile': '?0',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest'
}


response = requests.request("POST", url, headers=headers, data=payload)
elements = json.loads(response.text)['comments']

for element in elements:
    print(element['memo'])

