from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


GRANDMA_USER_ID = os.getenv("GRANDMA_USER_ID")
GRANDMA_CHANNEL_ID = os.getenv("GRANDMA_CHANNEL_ID") 
@app.post("/")
async def recevi_form(request: Request):
    data = await request.form()
    question = data.get("question")

    if not question:
        return {"error": "question is required"}
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text" : question
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)

    if resp.status_code == 200:
        return {"status": "Сообщение отправлено в Telegram"}
    else:
        return {"error": "Ошибка при отправке в Telegram", "details": resp.text}



    # data = {"chat_id": CHAT_ID, "text": question}
    # async with httpx.AsyncClient() as client:
    #     await client.post(url, data=data)

    return question


@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        print("FULL INCOMING DATA:", data)

        message = data.get("message")
        if not message:
            return {"status": "no message"}

        reply_to_message = message.get("reply_to_message")
        if not reply_to_message:
            return {"status": "not a reply"}

        chat_id = message["chat"]["id"]
        
        print(f"Using BOT_TOKEN: {BOT_TOKEN[:5]}...")
        print(f"Forwarding to: {GRANDMA_CHANNEL_ID}")

        forward_url = f"https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage"
        payload = {
            "chat_id": GRANDMA_CHANNEL_ID,
            "from_chat_id": chat_id,
            "message_id": reply_to_message["message_id"]
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(forward_url, json=payload)
            print("Telegram API response:", resp.status_code, resp.text)

        return {"status": "ok"}

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"status": "error", "details": str(e)}
