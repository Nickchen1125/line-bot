from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('p7ZAjIyyIZ5Ou7w5ViLmmWOASbr0RJPklLo3Q1Zv+lBa3FXZXcofHupT4wQ7YyQwsPOlaKjkTmKVuojhU84dGifYTho008x3kn/q7ikBfxcO5siQVM9l3egbdULBp4u8IRQloG6ZALlM7R/C7z3+bAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5ea6f7ab6a91ab8445b3d2bb1117d091')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()