import openai, time

client = openai.OpenAI()
max_tokens = 250

def gen_text(role, prompt, model='gpt-3.5-turbo'):
    system_msg = {'role': 'system', 'content': role}
    user_msg = {'role': 'user', 'content': prompt}
    response = client.chat.completions.create(
        model=model, max_tokens=max_tokens,
        temperature=0.7,
        messages=[system_msg, user_msg])
    time.sleep(0.5)
    return response.choices[0].message.content.strip()

def magi_tot(roles, question):
    print(f'=== 以下の質問に答えます ===\n{question}')
    answers = []
    for role in roles:
        role_p = f'あなたは{role}の代表です。' + \
            f'質問に真摯に向き合い、{role}らしい意見を述べます。'
        answer = gen_text(role_p, question)
        print(f'=== 役割: {role} ===\n{answer}')
        answers.append([role, answer])
    summary = magi_summarize(question, answers)
    prompt2 = \
        '### 指示:\nまず以下の質問に対する答えについて、賛否と意見を述べてください。\n' + \
        f'### 質問:\n{question}\n' + \
        f'### 答え:\n{summary}\n' + \
        '### 出力例:\n- 賛成 or 反対: ここに理由\n'
    print(f'=== 専門家にさらに質問します ===\n{prompt2}')
    answers = []
    for role in roles:
        role_p = f'あなたは{role}の代表です。建設的で率直な意見を述べます。'
        answer = gen_text(role_p, prompt2)
        print(f'=== 役割: {role} ===\n{answer}')
        answers.append([role, answer])
    summary = magi_summarize(question, answers)
    return summary

def magi_summarize(question, answers):
    answer_prompt = '\n'.join([
        f'### 専門家({role})の意見:\n{a}' for role, a in answers])
    summary_prompt = \
        '### 指示:\n以下の質問に答えてください。\n' + \
        'ただし以下の専門家たちの意見を要約して簡潔な結論と理由を提出してください。\n' + \
        f'### 質問:\n{question}\n' + \
        answer_prompt
    print('=== まとめ用プロンプト ===\n' + summary_prompt)
    summary = gen_text(
        'あなたは善良で公平な裁判官です。専門家の意見を元に結論を出します。',
        summary_prompt)
    print('=== 上記をまとめたもの ===\n' + summary)
    return summary

if __name__ == '__main__':
    question = \
        '事務職30代男性がメニューの豊富なファミレスでランチをします。' + \
        '今日頼むべきメニュー(日替わり/カレー/ハンバーグ/ラーメンなど)を提案してください。' + \
        '簡潔にメニューとその理由を一言で答えてください。'
    roles = ['栄養士', '愛情溢れる母親', '若い女性']
    magi_tot(roles, question)
