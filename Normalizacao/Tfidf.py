import sys, os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Normalizacao.stopwordsC import STOPWORDS

# ── Configuracao ──────────────────────────────────────────────────────────────
TOP_N = 25  # quantas palavras mostrar por topico

# ── Leitura ───────────────────────────────────────────────────────────────────
# Le o dataset_topicos_lda.csv gerado pelo gerar_topicos_lda.py
BASE          = os.path.dirname(os.path.abspath(__file__))
caminho_lda   = os.path.join("pfv_funciona/dataset_topicos_lda.csv")
caminho_saida = os.path.join("pfv_funciona/relatorio_tfidf_topicos.csv")

df = pd.read_csv(caminho_lda, on_bad_lines="skip")
df["Conteudo"] = df["Conteudo"].fillna("").astype(str)

topicos = sorted(df["topico_id"].unique())
print(f"Posts carregados : {len(df)}")
print(f"Topicos encontrados: {topicos}")

# ── TF-IDF por topico ─────────────────────────────────────────────────────────
# Para cada topico, roda TF-IDF so nos posts daquele grupo.
# Use a saida para identificar:
#   - palavras de hardware que escaparam → adicionar nas stopwords
#   - palavras genericas que poluem → adicionar nas stopwords
#   - palavras que realmente definem o topico → confirmar o nome do topico
print("\n" + "=" * 60)
print("RELATORIO TF-IDF POR TOPICO")
print("Use para identificar palavras ruins e atualizar stopwordsC.py")
print("=" * 60)

resumo = []

for topico_id in topicos:
    posts = df[df["topico_id"] == topico_id]["Conteudo"].tolist()

    if len(posts) < 2:
        print(f"\nTopico {topico_id}: posts insuficientes ({len(posts)}), pulando.")
        continue

    vectorizer = TfidfVectorizer(
        stop_words=STOPWORDS,
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.90
    )

    try:
        matriz = vectorizer.fit_transform(posts)
    except ValueError as e:
        print(f"\nTopico {topico_id}: erro ao vetorizar — {e}")
        continue

    # media dos pesos TF-IDF por termo em todo o topico
    media_tfidf  = matriz.mean(axis=0).A1
    nomes_termos = vectorizer.get_feature_names_out()
    top_idx      = media_tfidf.argsort()[-TOP_N:][::-1]
    top_palavras = [(nomes_termos[i], round(float(media_tfidf[i]), 4)) for i in top_idx]

    # nome do topico se existir
    if "topico_nome" in df.columns:
        nome = df[df["topico_id"] == topico_id]["topico_nome"].mode()[0]
    else:
        nome = f"Topico_{topico_id}"

    print(f"\nTopico {topico_id} — {nome} ({len(posts)} posts)")
    print("-" * 50)
    for palavra, peso in top_palavras:
        print(f"  {palavra:<40} {peso}")

    resumo.append({
        "topico_id"   : topico_id,
        "topico_nome" : nome,
        "n_posts"     : len(posts),
        "top_palavras": " | ".join([p for p, _ in top_palavras])
    })

# ── Resumo ────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("RESUMO — top 10 palavras por topico")
print("=" * 60)
resumo_df = pd.DataFrame(resumo)
print(resumo_df[["topico_id", "topico_nome", "n_posts", "top_palavras"]].to_string(index=False))

resumo_df.to_csv(caminho_saida, index=False, encoding="utf-8-sig")
print(f"\nRelatorio salvo em: {caminho_saida}")
print("\nProximo passo: revise as palavras acima e adicione em stopwordsC.py")
print("as que forem hardware, suporte, genericas ou lixo de normalizacao.")
print("Depois rode gerar_topicos_lda.py novamente e repita ate os topicos ficarem limpos.")