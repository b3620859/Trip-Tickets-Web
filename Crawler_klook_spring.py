import requests

url_base ='https://www.klook.com'
url_api = 'https://www.klook.com/v1/experiencesrv/category/activity?frontend_id_list={}&size={}'  #api frontend_id_list=23==>溫泉,3==主題樂園  size=資料筆數
# url_hot_springs = 'https://www.klook.com/zh-TW/experiences/cate/23-hot-springs/?frontend_id_list=23&size=24' #溫泉頁面網址
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    'Accept-Language': 'zh-TW',
    'currency':'TWD',
    'referer': 'https://www.klook.com/zh-TW/experiences/cate/23-hot-springs/?frontend_id_list=23&size=24',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
#先獲取總共筆數
url_api_format = url_api.format(23,24)
res = requests.get(url_api_format,headers = headers)
ans = res.json()
total_len = ans['result']['total']

url_api_format = url_api.format(23,total_len)
res = requests.get(url_api_format,headers = headers)
result=res.json()['result']['activities']   #現有資料結構

string_dash = "_"
print(string_dash*100)
print('| {:5s}| {:10s}| {:10s}| {:40s}| {:30s}|'.format('地點',  '評價', '特價','標題', '連結'))
for i in result:
    fix_title = i['title']  #處理標題過長
    if(len(fix_title)>35):
        fix_title = fix_title[:35]+'...'
    print('| {:5s}| {:10s}| {:10s}| {:40s}| {:30s}|'.format( i['location_title'], i['review_star'], i['sell_price']['amount_display'],fix_title, url_base+i['deep_link']))

