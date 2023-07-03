from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler

from linebot.exceptions import InvalidSignatureError

from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import json
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#receive msg
def receive_msg(request):
    try:
        body = request.get_data(as_text=True)
        json_data = json.loads(body)                           # json 格式化收到的訊息
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']       # 取得 reply token
        tp = json_data['events'][0]['message']['type']  # 取得 message 的類型
        if tp == 'text':
            msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
            line_bot_api.reply_message(tk,TextSendMessage(text=msg))
        if tp == 'sticker':
            # 如果收到的訊息是表情貼圖
            stickerId = json_data['events'][0]['message']['stickerId'] # 取得 stickerId
            packageId = json_data['events'][0]['message']['packageId'] # 取得 packageId
            # 使用 StickerSendMessage 方法回傳同樣的表情貼圖
            line_bot_api.reply_message(tk,StickerSendMessage(sticker_id=stickerId, package_id=packageId))
    except:
        print('error', body)
    return 'OK'
def reply_msg(text):
    # 客製化回覆文字
    msg_dict = {
        'hi':'Hi! 你好呀～',
        'hello':'Hello World!!!!',
        '你好':'你好呦～',
        'help':'有什麼要幫忙的嗎？'
    }
    # 如果出現特定地點，提供地點資訊
    local_dict = {
        '總統府':{
            'title':'總統府',
            'address':'100台北市中正區重慶南路一段122號',
            'latitude':'25.040319874750914',
            'longitude':'121.51162883484746'
        }
    }
    # 如果出現特定圖片文字，提供圖片網址
    img_dict = {
        '皮卡丘':'https://upload.wikimedia.org/wikipedia/en/a/a6/Pok%C3%A9mon_Pikachu_art.png',
        '傑尼龜':'https://upload.wikimedia.org/wikipedia/en/5/59/Pok%C3%A9mon_Squirtle_art.png'
    }
    # 預設回覆的文字就是收到的訊息
    reply_msg_content = ['text',text]
    if text in msg_dict:
        reply_msg_content = ['text',msg_dict[text.lower()]]
    if text in local_dict:
        reply_msg_content = ['location',local_dict[text.lower()]]
    if text in img_dict:
        reply_msg_content = ['image',img_dict[text.lower()]]
    return reply_msg_content
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
