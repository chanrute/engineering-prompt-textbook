import openai
import subprocess, sys

PS_PROMPT = '''
### 指示:
以下の質問について次の手順通り考えてください。
### 手順:
1. 問題を整理してください。
2. 問題を解決する計画を立ててください。
3. 上記に基づいてPythonプログラムを作ってください。
### 質問:
{question}
### 出力例:
```python
# ここにPythonのプログラム
```
'''.strip()

max_tokens = 800
api_mode = 'openai'
azure_model = 'test-gpt-35-turbo'

def gen_text(prompt, model='gpt-3.5-turbo'):
    sys_msg = {
        'role': 'system',
        'content': 'You are an intelligent and diligent systems engineer.' + \
            'You analyze problems accurately and create programs.'}
    user_msg = {'role': 'user', 'content': prompt}
    if api_mode == 'azure':
        client = openai.AzureOpenAI()
        model = azure_model
    else:
        client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model, max_tokens=max_tokens,
        temperature=0.7,
        messages=[sys_msg, user_msg])
    return response.choices[0].message.content.strip()

def save_and_run(py):
    tempfile = '_temp.py'
    with open(tempfile, 'wt', encoding='utf-8') as f:
        f.write(py)
    cmd = [sys.executable, tempfile]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def plan_and_solve(question):
    prompt = PS_PROMPT.format(question=question)
    print('=== プロンプト ===\n' + prompt)
    res = gen_text(prompt)
    print('=== 応答 ===\n' + res)
    if '```' not in res:
        print('[ERROR] プログラムが生成されませんでした。')
        return '', res
    try:
        py = res.split('```python\n')[1].split('```')[0].strip()
        print('=== プログラム ===\n' + py)
        result = save_and_run(py)
        print('=== プログラムの実行結果 ===\n' + result)
        return result, res
    except Exception as e:
        print('[ERROR] プログラムが正しく実行できませんでした。\n', e)
        return '', res

if __name__ == '__main__':
    question = '''
AとBの2本のロウソクがあります。
それぞれ火を点けると1分間1.25cmずつ短くなります。
Aは20cmですが、同時に火を点けてBが3分の2になった時、Aは燃え尽きました。
Bのロウソクの長さと燃え尽きるまでの時間を計算してください。
なお、以下のJSON形式(ensure_ascii=False)で答えを出力してください。
{"Bの長さ": "答えcm", "Bが燃え尽きるまでの時間": "答え分"}
### ヒント:
火を点けて、Aの長さが0cmになった時、Bは2/3だけ残っていました。
つまり、Bの長さはAの3/2で、燃えつきる時間も3/2倍です。
'''.strip()
    plan_and_solve(question)


