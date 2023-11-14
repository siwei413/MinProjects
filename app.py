from flask import Flask, request
from flask_cors import CORS
from gevent import pywsgi
import requests
import json
import logging

app = Flask(__name__)
CORS(app)


@app.route('/api/chat', methods=['POST'])
def example():
    logging.basicConfig(level=logging.DEBUG)
    # 静态设置access_token
    access_token = 'your_access_token'
    # 获取请求参数
    json_data = request.get_json()
    data = json_data.get('data')
    app.logger.info(data)
    get_response_text = get_response(access_token, data)
    app.logger.info(get_response_text)
    # picture = git_picture(data, access_token)
    return get_response_text


@app.route('/api/image', methods=['POST'])
def picture():
    # 静态设置access_token
    access_token = 'your_access_token'
    trans_access_token = 'your_access_token'
    # 获取请求参数
    json_data = request.get_json()
    data = json_data.get('image')
    trans = get_trans(trans_access_token, data)
    image = git_picture(trans, access_token)
    # access_token = get_access_token()
    return image


# 动态获取access_token
# def get_access_token(client_id，client_secret):
#     url = 'https://aip.baidubce.com/oauth/2.0/token'
#     # 请求的参数
#     data = {
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret
#     }
#     # 发送 POST 请求
#     response = requests.post(url, data=data)
#     # 获取返回结果的 JSON 数据
#     return response.json()['access_token']

# 获取响应结果
def get_response(access_token, user_data):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": user_data,
            }
        ],
        "system": "你叫移通超达，是人工智能时代下的产物，冉冉升起的新星，我是由重庆移通学院益达团队开发完成",
        "top_p": 1.0,
        "stream": False,
        "penalty_score": 1.0,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def git_picture(user_data, access_token):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl?access_token=" + access_token
    payload = json.dumps({
        "prompt":"one dog",
        "size": "1024x1024",
        "n": 1,
        "steps": 20,
        "sampler_index": "Euler a"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def get_trans(access_token, user_data):
    url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=" + access_token

    payload = json.dumps({
        "from": "zh",
        "to": "en",
        "q": user_data
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    dst_text = response_data['result']['trans_result'][0]['dst']
    return dst_text


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()
