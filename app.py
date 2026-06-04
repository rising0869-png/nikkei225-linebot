import gspread

gc = gspread.service_account(
    filename="bot-498411-78d452146270.json"
)

sheet = gc.open("日経平均225").sheet1

def search_stock(keyword):
    for row in rows:
        code = str(row["銘柄コード"])
        name = row["銘柄名"]

        if keyword in code or keyword in name:
            return (
                f"{code}\n"
                f"{name}\n"
                f"業種：{row['業種']}"
            )

    return "見つかりませんでした"

rows = sheet.get_all_records()
from flask import Flask, request
import os
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

CHANNEL_SECRET="mCDUULpq/8U3UDXhFIXSWRMYBuvJD6XM+LFGqikNeHjDuMo+oRSrT2jLiDFKh0OpDcPv9Mjl9qIXc6jL47LhExEjWHxMBzGjg/n+6rJgBUoJCwV0twQYLUbk3/srwrbY0uvcgIXx7MLcn8hGxuOAJwdB04t89/1O/w1cDnyilFU="
CHANNEL_ACCESS_TOKEN ="bfe03207ce7d9df623aafc4432d86fff"

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)

handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def home():
    return "225BOT OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    handler.handle(body, signature)

    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text

    reply_text = search_stock(user_text)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text=reply_text
                    )
                ]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)