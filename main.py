import hashlib
#from wechatpy.utils import check_signature
from flask import Flask, request, make_response
import xml.etree.ElementTree as ET


app = Flask(__name__)
app.debug = True


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/wechat_api/', methods=['GET', 'POST'])
# 定义路由地址请与URL后的保持一致
def wechat():
    if request.method == 'GET':
        token = '24__2kZPog1-kGUQtGTAoBzjd_AFey2IxCTfNdMaikkghAQPr3cAupwEYWYxLCPhm-P3oeSQvtJh0SKJyqQxUcRPMnARoz2oHT7oKdiNTySfIIK6A_dungDKBM2muoCWPgAGAYSL'
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
    elif request.method == 'POST':
        response = make_response(self.xml)
        response.content_type = 'application/xml'
        return response
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
