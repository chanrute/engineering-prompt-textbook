import openai


def call_chatgpt(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content


print(call_chatgpt("深呼吸してから、三毛猫の名前を3つ考えてください。"))
