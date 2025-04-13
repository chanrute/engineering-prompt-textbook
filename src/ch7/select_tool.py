import openai, time, json

SELECT_TOOL_TEMPLATE = '''
### 指示:
与えられたツールの一覧から相応しいツールを選んで、目標を達成するために努力してください。
### ツール一覧:
- 計算機: 引数に与えた計算式を計算します
  - 引数:
    - 計算式: 計算式を指定
- 検索: 指定したキーワードを検索します。
  - 引数:
    - キーワード: 検索キーワード
- 現在時刻: 現在時刻を返します。
### 目標:
```{input}```
### 出力例:
JSON形式で出力してください。
```json
{"行動": "ツール名", "引数": "ここに引数", "備考": "ここに備考"}
```
'''

def call_chatgpt(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}])
    return completion.choices[0].message.content

def selec_tool(prompt):
    prompt = prompt.replace('`', '"')
    st_prompt = SELECT_TOOL_TEMPLATE.replace('{input}', prompt)
    res = call_chatgpt(st_prompt)
    print('=== 応答 ===\n' + res)
    try:
        if '```json' in res:
            res = res.split('```json')[1].split('```')[0]
        data = json.loads(res)
        action = data['行動']
        arg = data['引数']
        memo = data['備考']
        if action == '計算機':
            val = eval(arg)
            return f'{memo}→{val}'
        elif action == '検索':
            return f'「{arg}」を検索します。(TODO)' + memo
        elif action == '現在時刻':
            return time.strftime('%Y年%m月%d日 %H:%M') + '→' + memo
        else:
            return 'ツールが見つかりませんでした。' + res
    except Exception as e:
        return 'JSONが取得できませんでした。' + e

if __name__ == '__main__':
    prompt = '4300円の柿を30箱、3000円の苺を50箱買いました。合計いくらですか？'
    res = selec_tool(prompt)
    print('=== 結果 ===\n' + res)

