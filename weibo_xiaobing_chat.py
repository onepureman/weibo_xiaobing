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
            "Cookie": "login_sid_t=b7694b933cc512f7e85688a0a2a78345; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=2827453773357.5864.1557798619194; SINAGLOBAL=2827453773357.5864.1557798619194; ULV=1557798619202:1:1:1:2827453773357.5864.1557798619194:; SSOLoginState=1557798630; SCF=And8B39Te5KxeDr9Pud1IA5-fOK2tDqhP1Lx0EmploZ6K3V5XQ1cgGXglVwh1ps-zPm_pq2IW_A0Zj6pxJbN7T4.; un=18513606786; wvr=6; __guid=218532681.3481864489142050300.1557798693954.86; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvENqAp4M9zN4V_biSY6qa5JpX5KzhUgL.Foqce0eR1hef1K22dJLoIEXLxK-LBozL1h2LxKqL1-eL1hnLxKBLB.zLBK-LxKnL12BL1KzLxKnL122L1-et; SUB=_2A25x2KZoDeRhGeBI6FEZ-C3Jwj2IHXVSr5CgrDV8PUNbmtAKLUrukW9NRpov0Uw7ntDVLjSiJcEeTOp8f01ouKqZ; SUHB=0btMvYWmOAOXau; ALF=1589512631; monitor_count=17",
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