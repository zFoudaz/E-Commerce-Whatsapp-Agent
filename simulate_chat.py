from Agent.agent import create_chat, send_message

history = [
    {"role": "user",  "parts": [{"text": "My name is Fouda"}]},
    {"role": "model", "parts": [{"text": "Nice to meet you, Fouda!"}]},
]

chat = create_chat(history=history)


while True:
    message = str(input("Human: "))
    if message.lower().strip() == 'exit':
        break
    response = send_message(chat, message)
    print(f"AI: {response.text}")
    print([h.model_dump() for h in chat.get_history()])