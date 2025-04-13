import openai, time

def call_chatgpt(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}])
    return completion.choices[0].message.content

user = input('何を尋ねますか? >')
user = user.replace('`', '"')

datetime_str = time.strftime('%Y年%m月%d日 %H:%M')
prompt = f'''
### 指示:
以下の前提情報を利用して質問に答えてください。
### 前提情報:
現在時刻: {datetime_str}
### 質問応答の例:
- 質問: 今何時ですか？
- 応答: 今は、{datetime_str}です。
### 質問:
```{user}```
'''

res = call_chatgpt(prompt)
print('AIの答え: ' + res)

