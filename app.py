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

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        json_data = json.loads(body)  # json 格式化收到的訊息
        tk = json_data['events'][0]['replyToken']  # 取得 reply token
        tp = json_data['events'][0]['message']['type']  # 取得 message 的類型
        
        if tp == 'text':
            msg = json_data['events'][0]['message']['text']  # 取得使用者發送的訊息
            line_bot_api.reply_message(tk, TextSendMessage(text=msg))
        elif tp == 'sticker':
            stickerId = json_data['events'][0]['message']['stickerId']  # 取得 stickerId
            packageId = json_data['events'][0]['message']['packageId']  # 取得 packageId
            line_bot_api.reply_message(tk, StickerSendMessage(sticker_id=stickerId, package_id=packageId))
            
    except Exception as e:
        print('error:', e)
        abort(400)
    
    return 'OK'
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)