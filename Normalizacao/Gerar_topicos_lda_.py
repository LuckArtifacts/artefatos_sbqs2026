import sys, os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import unicodedata

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Normalizacao.stopwordsC import STOPWORDS

# ── Configuracao ──────────────────────────────────────────────────────────────
N_TOPICOS = 10

nomes_topicos = {
    1: "Bugs_Configuracoes_UI",
    2: "Falhas_Hardware_Energia",
    3: "Bugs_Audio_Bluetooth",
    4: "Feedback_Comunidade",
    5: "Bugs_Interface_Desempenho",
    6: "Bugs_Apps_Notificacoes",
    7: "Bugs_Conectividade_Rede",
    8: "Falhas_Acesso_Sistema",
    9: "Bugs_Chamada_Audio",
    10: "Roadmap_Lancamento",

}

def remover_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )
    
# ── Leitura ───────────────────────────────────────────────────────────────────
BASE            = os.path.dirname(os.path.abspath(__file__))
caminho_entrada = os.path.join("Normalizacao/CSVs/dataset_que_talvez_ta_certo.csv")
caminho_saida   = os.path.join("pfv_funciona/dataset_topicos_lda.csv")

df = pd.read_csv(caminho_entrada, on_bad_lines="skip")
df["Conteudo_Original"] = df["Conteudo_Original"].fillna("").astype(str)
df["Conteudo_Original"] = df["Conteudo_Original"].apply(remover_acentos)

print(f"Posts carregados: {len(df)}")

# ── Vetorizacao com CountVectorizer ───────────────────────────────────────────
vectorizer = CountVectorizer(
    stop_words=STOPWORDS,
    max_features=2000,
    ngram_range=(1, 2),
    min_df=3,
    max_df=0.90
)
matriz = vectorizer.fit_transform(df["Conteudo_Original"])

print(f"Vocabulario: {len(vectorizer.get_feature_names_out())} termos")

# ── LDA ───────────────────────────────────────────────────────────────────────
lda = LatentDirichletAllocation(
    n_components=N_TOPICOS,
    max_iter=50,
    learning_method="online",
    random_state=42,
    n_jobs=1        # n_jobs=1 evita warnings de multiprocessing no Python 3.13
)
distribuicao = lda.fit_transform(matriz)

# ── Top palavras por topico ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TOPICOS ENCONTRADOS — analise e renomeie em nomes_topicos")
print("=" * 60)
nomes_termos = vectorizer.get_feature_names_out()
for i, topico in enumerate(lda.components_):
    top_idx      = topico.argsort()[-15:][::-1]
    top_palavras = [nomes_termos[j] for j in top_idx]
    print(f"\nTopico {i+1} ({nomes_topicos.get(i+1, '?')}):")
    print("  " + " | ".join(top_palavras))
print("=" * 60)

# ── Classificacao ─────────────────────────────────────────────────────────────
df["topico_id"]        = distribuicao.argmax(axis=1) + 1
df["topico_confianca"] = distribuicao.max(axis=1).round(3)
df["topico_nome"]      = df["topico_id"].map(nomes_topicos)

# ── Salvar ────────────────────────────────────────────────────────────────────
df.to_csv(caminho_saida, index=False, encoding="utf-8-sig")

print(f"\nSalvo em: {caminho_saida}")
print(f"\nDistribuicao dos topicos:")
print(df["topico_id"].value_counts().sort_index())
print(f"\nConfianca media por topico:")
print(df.groupby("topico_nome")["topico_confianca"].mean().round(3).sort_values(ascending=False))