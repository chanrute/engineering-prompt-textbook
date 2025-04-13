import magi_tot
question = '''
持ち家か賃貸か、どちらが良いですか？
できるだけ簡潔に答えと理由を提案してください。
家族構成: 30代夫婦で子供が2人
世帯年収: 500万円
居住地域: 東京近郊
'''.strip()
roles = ['不動産の専門家', '経営コンサルタント', '賢い母親']
magi_tot.max_tokens = 350
magi_tot.magi_tot(roles, question)
