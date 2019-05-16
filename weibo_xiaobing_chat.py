import requests
from lxml import etree
import time
import json


class XiaoBing(object):

    def __init__(self):
        self.data = {
            'text': "",
            'uid': '5175429989',
            'extensions': '{"clientid":"7qfuu18z8g9lfwepu91visz6cp716ep"}',
            'is_encoded': '0',
            'decodetime': '1',
            'source': '209678993',
            }

        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "152",
            "Content-Type":"application/x-www-form-urlencoded",
            "Cookie": "",
            "Host": "api.weibo.com",
            "Origin": "https://api.weibo.com",
            "Referer": "https://api.weibo.com/chat/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
        }

    def post_query(self, query):
        self.data["text"] = query
        post_url = "https://api.weibo.com/webim/2/direct_messages/new.json"

        r_post_query = requests.post(post_url, data=self.data, headers=self.headers)
        print(r_post_query.content.decode())

    def get_response(self, query):

        self.post_query(query)
        times = 1
        #  刷新20次，获取第一条回答（except中的继续是测试一下能否继续下去获得正确）
        while times <= 20:
            times += 1
            response = requests.get("https://weibo.com/aj/message/getbyid?ajwvr=6&uid=5175429989&count=1&_t=0",
                                    headers={"Cookie": self.headers["Cookie"]})
            text_dict = json.loads(response.content.decode())
            try:
                html = text_dict["data"]["html"]
                html_content = etree.HTML(html)

                text = html_content.xpath("//p[@class='page']/text()")[0]  # 定位到回答的位置，并获取到回答

                if text == query:
                    time.sleep(0.5)  # 为了防止回答的页面还没有刷新，当刷到的还是问题，则稍微停一下，然后再获取
                    continue
                else:
                    return text  # 将回答的结果返回

            except Exception as e:
                time.sleep(0.3)  # 尝试出错时能否继续刷新获得正确的解析结果
                continue


if __name__ == '__main__':
    a = XiaoBing().get_response("那你知道什么")
    print(a)