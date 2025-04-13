import plan_and_solve, json, time
question = '''
お店で320円のプリンと210円のチョコをいくつかを買って1万円を支払いました。
お釣りは450円でした。チョコとプリンを何個ずつ買ったのでしょうか？
結果は以下のようにJSON形式で出力してください。
`{"チョコ": チョコの個数, "プリン": プリンの個数}`
'''.strip()
q = question
success = False
for i in range(5):
    result, response = plan_and_solve.plan_and_solve(q)
    try:
        result = result.replace("'", '"')
        o = json.loads(result)
        print('結果:', o)
        total = o['プリン'] * 320 + o['チョコ'] * 210
        if total == (10000 - 450):
            print('=== 正解 ===')
            success = True
            break
        else:
            print('残念、失敗しました。')
            q = f'{question}\n### 失敗例:\n' + \
                '以下の応答は不正解でした。' + \
                f'間違いから学んで正しいプログラムを作成してください。\n{response}'
    except Exception as e:
        print('[ERROR] JSON形式のデータが出力されませんでした。\n', e)
    time.sleep(5)
    print(f'=== 再試行: {i+2}回目 ===')
if not success:
    print('試行回数が制限回数を超えました。')
