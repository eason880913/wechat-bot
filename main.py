import hashlib

from flask import Flask, request, make_response
import xml.etree.ElementTree as ET

WX_TOKEN = '24_Izj8pBDc6UKYbWfM7DUROUXwIAU8Vd0HMh3NE8vuLJ9b3y_grnoSw61XgAFJUEW7zq4ZqGaQK7V6Zy_'
# 这里填写公众号配置的token

app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/wechat_api/', methods=['GET', 'POST'])
# 定义路由地址请与URL后的保持一致
def wechat():
    if request.method == 'GET':
    token = WX_TOKEN
    data = request.args
    signature = data.get('signature', '')
    timestamp = data.get('timestamp', '')
    nonce = data.get('nonce', '')
    echostr = data.get('echostr', '')
    s = sorted([timestamp, nonce, token])
    # 字典排序
    s = ''.join(s)
    if hashlib.sha1(s.encode('utf-8')).hexdigest() == signature:
        # 判断请求来源，并对接受的请求转换为utf-8后进行sha1加密
        response = make_response(echostr)
        # response.headers['content-type'] = 'text' 
        # 新浪SAE未实名用户加上上面这句
        return response

if __name__ == '__main__':
app.run(host='0.0.0.0', port=80)
# app.run(host='0.0.0.0', port=5050)