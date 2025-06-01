from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


GRANDMA_USER_ID = os.getenv("GRANDMA_USER_ID")
GRANDMA_CHANNEL_ID = os.getenv("GRANDMA_CHANNEL_ID")  # её канал (можно id или @username)
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
    data = await request.json()
    
    # Проверяем, что это сообщение  
    message = data.get("message")
    if not message:
        return {"status": "no message"}

    from_user = message.get("from", {})
    user_id = from_user.get("id")
 
    # Проверяем, что это бабушка ответила
    if user_id != GRANDMA_USER_ID:
        return {"status": "not grandma"}

    # Проверяем, что сообщение - ответ на другое сообщение (реплай)
    reply_to_message = message.get("reply_to_message")
    if not reply_to_message:
        return {"status": "not a reply"}

    # Теперь пересылаем ответ бабушки в её канал
    message_id = message.get("message_id")
    chat_id = message.get("chat", {}).get("id")

    forward_url = f"https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage"
    payload = {
        "chat_id": GRANDMA_CHANNEL_ID,
        "from_chat_id": chat_id,
        "message_id": message_id
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(forward_url, json=payload)

    if resp.status_code == 200:
        return {"status": "message forwarded"}
    else:
        return {"error": "failed to forward", "details": resp.text}
