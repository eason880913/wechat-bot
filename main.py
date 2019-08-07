import hashlib

from flask import Flask, request, make_response
import xml.etree.ElementTree as ET


app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/wechat_api/', methods=['GET', 'POST'])
# 定义路由地址请与URL后的保持一致
def wechat():
    if request.method == 'GET':
        token = '24_xP_mRqkGuEi7l0aBcAns48ddgvRjZCAs6p7_mQU5-zkB6wYZP1XbFRyyLdayfILDbnDA7Zjh9FfHE1JA3invC3hmj_jLzpg-3Ss-Ug2E32gktCp-Kps7KCG-J-x5oXoM3NaRN8h36btaDjK_SANiADALTG'
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

#import os
if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port='80')