import openai

client = openai.OpenAI()

messages = []

def call_chatgpt_chat(user_text):
    messages.append({"role": "user", "content": user_text})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    res = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": res})
    return res


while True:
    user = input("あなた: ")
    if user == 'quit' or user == 'exit':
        break
    if user == '': continue
    res = call_chatgpt_chat(user)
    print(f"AI: {res}")
