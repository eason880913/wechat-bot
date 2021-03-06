import hashlib
#from wechatpy.utils import check_signature
from flask import Flask, request, make_response
#import xml.etree.ElementTree as ET
from lxml import etree
import time

app = Flask(__name__)
app.debug = True


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

class Message(object):
    def __init__(self, req): #req = <Request 'http://we-interface.herokuapp.com/wechat_api/?signature=0755d2637971ca656c50945c80343e8d6124ca8c&timestamp=1565688956&nonce=1129916171&openid=onFvxv87mAo_-B9iQ41rAxCD-b64' [POST]>
        self.request = req
        self.token = '24__2kZPog1-kGUQtGTAoBzjd_AFey2IxCTfNdMaikkghAQPr3cAupwEYWYxLCPhm-P3oeSQvtJh0SKJyqQxUcRPMnARoz2oHT7oKdiNTySfIIK6A_dungDKBM2muoCWPgAGAYSL'
        self.AppID = 'wxca926cd8097ad666'
        self.AppSecret = 'ffd6e016a9aff283e2af7ffa386630fb'

class Post(Message):
    def __init__(self, req):
        super(Post, self).__init__(req)
        self.xml = etree.fromstring(req.stream.read())
        self.MsgType = self.xml.find("MsgType").text
        #print(self.xml.find("MsgType").text)
        self.ToUserName = self.xml.find("ToUserName").text
        #print(self.xml.find("ToUserName").text)
        self.FromUserName = self.xml.find("FromUserName").text
        #print(self.xml.find("FromUserName").text)
        self.CreateTime = self.xml.find("CreateTime").text
        #print(self.xml.find("CreateTime").text)
        self.MsgId = self.xml.find("MsgId").text
        #print(self.xml.find("MsgId").text)
        print('text:'+self.xml.find("Content").text)
        hash_table = {
            'text': ['Content'],
            'image': ['PicUrl', 'MediaId'],
            'voice': ['MediaId', 'Format'],
            'video': ['MediaId', 'ThumbMediaId'],
            'shortvideo': ['MediaId', 'ThumbMediaId'],
            'location': ['Location_X', 'Location_Y', 'Scale', 'Label'],
            'link': ['Title', 'Description', 'Url'],
        }
        attributes = hash_table[self.MsgType]
        #print(attributes)
        self.Content = self.xml.find("Content").text if 'Content' in attributes else '?????????????????????????????????'
        self.PicUrl = self.xml.find("PicUrl").text if 'PicUrl' in attributes else '?????????????????????????????????'
        self.MediaId = self.xml.find("MediaId").text if 'MediaId' in attributes else '?????????????????????????????????'
        self.Format = self.xml.find("Format").text if 'Format' in attributes else '?????????????????????????????????'
        self.ThumbMediaId = self.xml.find("ThumbMediaId").text if 'ThumbMediaId' in attributes else '?????????????????????????????????'
        self.Location_X = self.xml.find("Location_X").text if 'Location_X' in attributes else '?????????????????????????????????'
        self.Location_Y = self.xml.find("Location_Y").text if 'Location_Y' in attributes else '?????????????????????????????????'
        self.Scale = self.xml.find("Scale").text if 'Scale' in attributes else '?????????????????????????????????'
        self.Label = self.xml.find("Label").text if 'Label' in attributes else '?????????????????????????????????'
        self.Title = self.xml.find("Title").text if 'Title' in attributes else '?????????????????????????????????'
        self.Description = self.xml.find("Description").text if 'Description' in attributes else '?????????????????????????????????'
        self.Url = self.xml.find("Url").text if 'Url' in attributes else '?????????????????????????????????'
        self.Recognition = self.xml.find("Recognition").text if 'Recognition' in attributes else '?????????????????????????????????'

class Reply(Post): # <Request 'http://we-interface.herokuapp.com/wechat_api/?signature=55df59ed9869663f1c4dfafc61a160e4f6b22aa4&timestamp=1565687475&nonce=444201171&openid=onFvxv87mAo_-B9iQ41rAxCD-b64' [POST]>
    def __init__(self, req):
        super(Reply, self).__init__(req)
        self.xml = f'<xml><ToUserName><![CDATA[{self.FromUserName}]]></ToUserName>' \
                   f'<FromUserName><![CDATA[{self.ToUserName}]]></FromUserName>' \
                   f'<CreateTime>{str(int(time.time()))}</CreateTime>'

    def text(self, Content):
        self.xml += f'<MsgType><![CDATA[text]]></MsgType>' \
                    f'<Content><![CDATA[{Content}]]></Content></xml>'

    def image(self, MediaId):
        pass

    def voice(self, MediaId):
        pass

    def video(self, MediaId, Title, Description):
        pass

    def music(self, ThumbMediaId, Title='', Description='', MusicURL='', HQMusicUrl=''):
        pass
        
    def reply(self):
        response = make_response(self.xml)
        response.content_type = 'application/xml'
        return response

@app.route('/wechat_api/', methods=['GET', 'POST'])
# ????????????????????????URL??????????????????
def wechat():
    if request.method == 'GET':
        token = '24__2kZPog1-kGUQtGTAoBzjd_AFey2IxCTfNdMaikkghAQPr3cAupwEYWYxLCPhm-P3oeSQvtJh0SKJyqQxUcRPMnARoz2oHT7oKdiNTySfIIK6A_dungDKBM2muoCWPgAGAYSL'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = sorted([timestamp, nonce, token])
        # ????????????
        s = ''.join(s)
        if hashlib.sha1(s.encode('utf-8')).hexdigest() == signature:
            # ???????????????????????????????????????????????????utf-8?????????sha1??????
            response = make_response(echostr)
            # response.headers['content-type'] = 'text' 
            # ??????SAE?????????????????????????????????
            return response
    elif request.method == 'POST': # <Request 'http://we-interface.herokuapp.com/wechat_api/?signature=55df59ed9869663f1c4dfafc61a160e4f6b22aa4&timestamp=1565687475&nonce=444201171&openid=onFvxv87mAo_-B9iQ41rAxCD-b64' [POST]>
        message = Reply(request)
        message.text(message.Content)
        return message.reply()
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
