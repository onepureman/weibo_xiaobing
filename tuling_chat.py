
import requests
import json
import time


def tuling_chat(info):
    Key = ''  # key 为创建的图灵机人的key,现在免费的接口每个机器人智能调用100次，共存的机器人最多五个
    url = 'http://www.tuling123.com/openapi/api'
    info.encode('utf-8')
    query = {'key': Key, 'info': info}
    headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
    r = requests.get(url, params=query, headers=headers)
    res = r.text
    answer_content = json.loads(res).get('text').replace('<br>', '\n').replace(" ", "，").replace(",", "，")
    time.sleep(1.5)

    if "当天请求次数" in answer_content:
        print("请更换图灵机器人")
    else:
        return answer_content  # 返回回答的结果


if __name__ == '__main__':
    tuling_chat("你说什么")