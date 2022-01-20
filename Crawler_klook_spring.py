import requests
from bs4 import BeautifulSoup
from sqldatabase import Database
import datetime

class Spring_item:
    def __init__(self):
        self.id = None
        self.location = None
        self.title = None
        self.rate = None
        self.market_price = None
        self.sell_price = None
        self.link = None


class Klook:

    def __init__(self):
        # https: // www.klook.com / zh - TW / addtocart?is_merge = 1 & shoppingcart_id = 74349624 #購物車
        self.url_base = 'https://www.klook.com'
        self.url_login = 'https://log.klook.com/v2/frontlogsrv/log/web'
        self.url_api = 'https://www.klook.com/v1/experiencesrv/category/activity?frontend_id_list={}&size={}'  # api frontend_id_list=23==>溫泉,3==主題樂園  size=資料筆數
        # url_hot_springs = 'https://www.klook.com/zh-TW/experiences/cate/23-hot-springs/?frontend_id_list=23&size=24' #溫泉頁面網址
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            'Accept-Language': 'zh-TW',
            'currency': 'TWD',
            'referer': 'https://www.klook.com/zh-TW/experiences/cate/23-hot-springs/?frontend_id_list=23&size=24',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        #登入用cookie
        f = open(".\\cookie.txt", 'r')
        self.cookie3 = f.read()
        f.close()

    def getItemlist(self, list_id: int):
        '''
        get Item List in [list_id] category
        :param list_id: category id
        :return: Item List
        '''
        # 先獲取總共筆數
        url_api_format = self.url_api.format(list_id, 24)
        res = requests.get(url_api_format, headers=self.headers)
        ans = res.json()
        total_len = ans['result']['total']
        url_api_format = self.url_api.format(23, total_len)
        res = requests.get(url_api_format, headers=self.headers)
        result = res.json()['result']['activities']  # 現有資料結構

        spring_list: list[Spring_item] = list()
        for i in result:
            spring_item = Spring_item()
            spring_item.id = i['activity_id']
            spring_item.location = i['location_title']
            spring_item.title = i['title']
            spring_item.rate = i['review_star']
            spring_item.sell_price = i['sell_price']['amount_display']
            try:
                spring_item.market_price = i['market_price']['amount_display'] #該欄位不一定有值
            except:
                print(f'{spring_item.id} :　無市價')
            spring_item.link = self.url_base + i['deep_link']
            spring_list.append(spring_item)

        self.save2db(spring_list)

        return spring_list

    def save2db(self,item_list):
        datas = list()
        for i in item_list:
            data = list()
            data.append(i.id)
            data.append(i.location)
            data.append(i.title)
            data.append(i.rate)
            data.append(i.market_price)
            data.append(i.sell_price)
            data.append(i.link)
            data.append(int(datetime.datetime.now().timestamp()))
            datas.append(data)

        db = Database()
        db.SaveData2MySQL(datas)


    def login(self):
        '''
        using cookie login
        :return:
        '''
        url ='https://www.klook.com/zh-TW/wishlist'
        # for i in self.cookie.split("; "):
        #     cookies = cookies+{i.split("=")[0]:i.split("=")[1]}
        #     print(cookies)
        cookies = {i.split("=")[0]:i.split("=")[1] for i in self.cookie3.split("; ")}
        # print(cookies)

        url_api_format = self.url_api.format(23, 24)
        res = requests.get(url, headers=self.headers,cookies = cookies)
        print(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')


    def addWishList(self,id:int):
        url_add = 'https://www.klook.com/v1/usrcsrv/wishlist/add'
        cookies2 = {i.split("=")[0]:i.split("=")[1] for i in self.cookie3.split("; ")}
        payload = {"object_id":str(id),"object_type":"act"}
        res = requests.post(url_add,cookies = cookies2 ,json =payload )
        result = res.json()
        print(f'Add wishlist {result["result"]}')
        return result['success']

    def cancelWishList(self,id:int):
        url_add = 'https://www.klook.com/v1/usrcsrv/wishlist/cancel'
        cookies2 = {i.split("=")[0]: i.split("=")[1] for i in self.cookie3.split("; ")}
        payload = {"object_id": str(id), "object_type": "act"}
        res = requests.post(url_add, cookies=cookies2, json=payload)
        result = res.json()
        print(f'Cancel wishlist {result["result"]}')

        return result['success']




test = Klook()
# test.login()
test.getItemlist(23)
# test.addWishList(50339)
# test.cancelWishList(50339)
