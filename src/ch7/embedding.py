from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('stsb-xlm-r-multilingual')

sentences = [
    '今日の天気予報によると雨が振ります。',
    'この会社はサバ缶を海外に輸出しています。',
    'Pythonを使ってEmbeddingを計算しています。',
    '空を見上げると雲が多いので傘を持っていこう。']
embeddings = model.encode(sentences)
cosine_scores = util.cos_sim(embeddings, embeddings)
result = []
for i, sentence in enumerate(sentences):
    score = cosine_scores[0][i]
    embedding = embeddings[i]
    result.append({'score': score, 'sentence': sentence})
    print("文章:", sentence)
    print("Embedding:", embedding[:5], '...')
    print("類似度:", score)
    print("---------")
result = list(sorted(result, key=lambda x: x['score'], reverse=True))
print("=== 最初の文と近い順に表示 ===")
for e in result:
    print(f"(類似度:{e['score']:.3f}) {e['sentence']}")

