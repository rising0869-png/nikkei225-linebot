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

def get_industries():
    industries = sorted(set(row["業種"] for row in rows))
    return "\n".join(industries)


def search_industry(industry):
    result = []

    for row in rows:
        if row["業種"] == industry:
            result.append(
                f"{row['銘柄コード']} {row['銘柄名']}"
            )

    if result:
        return "\n".join(result)

    return None

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

CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]

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

if user_text == "業種一覧":
    reply_text = get_industries()

else:
    industry_result = search_industry(user_text)

    if industry_result:
        reply_text = industry_result
    else:
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