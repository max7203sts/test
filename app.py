from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

#======python的函數庫==========
import os, crawler
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
@handler.add(MessageEvent, message=[TextMessage, StickerMessage])
def handle_message(event): 
    tp=event.message.type
    if tp == 'text':
        msg = event.message.text
        if '繳水電' in msg:
            reply = crawler.card()
            line_bot_api.reply_message(event.reply_token, reply)
        elif '行動支付' in msg:
            reply = crawler.payback()
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            line_bot_api.reply_message(event.reply_token, StickerSendMessage(sticker_id=16581263, package_id=8515))
    else:
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(sticker_id=10885, package_id=789))
    return


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
