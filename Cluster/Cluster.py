import sys, os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split
import hdbscan

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Normalizacao.stopwordsC import STOPWORDS

# ── Configuracao ──────────────────────────────────────────────────────────────
topicos_relevantes = [2, 4, 7, 8]

CONFIANCA_MINIMA_LDA     = 0.50
CONFIANCA_MINIMA_HDBSCAN = 0.50

SEED_AMOSTRA_FN = 42      
N_AMOSTRA_FN    = 120     

# ── Leitura ───────────────────────────────────────────────────────────────────
BASE           = os.path.dirname(os.path.abspath(__file__))
caminho_lda    = os.path.join("pfv_funciona/dataset_topicos_lda.csv")
caminho_limpo  = os.path.join("Cluster/CSVs/dataset_limpo_hdbscan.csv")
caminho_treino = os.path.join("Cluster/CSVs/dataset_treino_llm.csv")
caminho_val    = os.path.join("Cluster/CSVs/dataset_val_llm.csv")
caminho_teste  = os.path.join("Cluster/CSVs/dataset_teste_llm.csv")

# NOVO: diretorio para os descartados
DIR_DESC = os.path.join("Cluster/CSVs/descartados")
os.makedirs(DIR_DESC, exist_ok=True)

df = pd.read_csv(caminho_lda, on_bad_lines="skip")
df["Conteudo"] = df["Conteudo"].fillna("").astype(str)

# NOVO: registro do funil
funil = []
def registra(etapa, restantes, removidos, criterio):
    funil.append({"etapa": etapa, "restantes": restantes,
                  "removidos": removidos, "criterio": criterio})

TOTAL_INICIAL = len(df)
registra("0. Base carregada (pos-LDA)", TOTAL_INICIAL, 0, "posts com topico atribuido")

print(f"Dataset carregado: {len(df)} posts")
print(f"\nDistribuicao original dos topicos:")
print(df["topico_id"].value_counts().sort_index())

# ── Filtro 1: topicos relevantes (software) ───────────────────────────────────
quantidade_topicos = len(topicos_relevantes)
antes = len(df)

# NOVO: guarda os descartados por topico irrelevante
desc_topico = df[~df["topico_id"].isin(topicos_relevantes)].copy()
desc_topico["motivo_descarte"] = "topico_nao_relevante"
desc_topico["etapa_descarte"]  = "F1_topico"
desc_topico.to_csv(os.path.join(DIR_DESC, "F1_topico_nao_relevante.csv"),
                   index=False, encoding="utf-8-sig")

df_filtrado = df[df["topico_id"].isin(topicos_relevantes)].copy()
df_filtrado = df_filtrado.reset_index(drop=True)
registra("1. Filtro de topicos", len(df_filtrado), antes - len(df_filtrado),
         f"topico_id em {topicos_relevantes}")
print(f"\nApos filtrar topicos {topicos_relevantes}: {len(df_filtrado)} posts")

# ── Filtro 2: confianca minima do LDA ────────────────────────────────────────
antes = len(df_filtrado)

# NOVO
desc_conf_lda = df_filtrado[df_filtrado["topico_confianca"] < CONFIANCA_MINIMA_LDA].copy()
desc_conf_lda["motivo_descarte"] = f"confianca_lda_menor_{CONFIANCA_MINIMA_LDA}"
desc_conf_lda["etapa_descarte"]  = "F2_confianca_lda"
desc_conf_lda.to_csv(os.path.join(DIR_DESC, "F2_confianca_lda_baixa.csv"),
                     index=False, encoding="utf-8-sig")

df_filtrado = df_filtrado[df_filtrado["topico_confianca"] >= CONFIANCA_MINIMA_LDA].copy()
df_filtrado = df_filtrado.reset_index(drop=True)
registra("2. Confianca LDA", len(df_filtrado), antes - len(df_filtrado),
         f"topico_confianca >= {CONFIANCA_MINIMA_LDA}")
print(f"Apos filtro confianca LDA >= {CONFIANCA_MINIMA_LDA}: {len(df_filtrado)} posts "
      f"(removidos {antes - len(df_filtrado)})")

# ── Vetorizacao e LDA refinado ────────────────────────────────────────────────
vectorizer = CountVectorizer(
    stop_words=STOPWORDS,
    max_features=2000,
    ngram_range=(1, 2),
    min_df=3,
    max_df=0.90
)
matriz_filtrada = vectorizer.fit_transform(df_filtrado["Conteudo"])

lda = LatentDirichletAllocation(
    n_components=quantidade_topicos,
    max_iter=30,
    learning_method="online",
    random_state=42,
    n_jobs=1
)
distribuicao = lda.fit_transform(matriz_filtrada)

print("\nTopicos refinados (so software):")
print("=" * 50)
nomes_termos = vectorizer.get_feature_names_out()
for i, topico in enumerate(lda.components_):
    top_idx      = topico.argsort()[-12:][::-1]
    top_palavras = [nomes_termos[j] for j in top_idx]
    print(f"\nTopico {i+1}: {' | '.join(top_palavras)}")
print("=" * 50)

# ── HDBSCAN ───────────────────────────────────────────────────────────────────
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=80,
    min_samples=10,
    metric="euclidean",
    prediction_data=True
)
labels_hdbscan = clusterer.fit_predict(distribuicao)

df_filtrado["hdbscan_cluster"]   = labels_hdbscan
df_filtrado["hdbscan_confianca"] = clusterer.probabilities_

n_ruido    = (labels_hdbscan == -1).sum()
n_clusters = len(set(labels_hdbscan)) - (1 if -1 in labels_hdbscan else 0)

print(f"\nResultado HDBSCAN:")
print(f"  Clusters encontrados : {n_clusters}")
print(f"  Posts com cluster    : {(labels_hdbscan != -1).sum()}")
print(f"  Posts como ruido (-1): {n_ruido} ({n_ruido/len(df_filtrado)*100:.1f}%)")
print(f"\nDistribuicao por cluster:")
print(df_filtrado["hdbscan_cluster"].value_counts().sort_index())

# ── Palavras mais representativas por cluster HDBSCAN ─────────────────────────
print("\n" + "=" * 60)
print("Palavras mais representativas por cluster (HDBSCAN)")
print("=" * 60)

for cluster_id in sorted(df_filtrado[df_filtrado["hdbscan_cluster"] != -1]["hdbscan_cluster"].unique()):
    df_cluster = df_filtrado[df_filtrado["hdbscan_cluster"] == cluster_id]

    vec_cluster = CountVectorizer(
        stop_words=STOPWORDS,
        max_features=500,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    matriz_cluster = vec_cluster.fit_transform(df_cluster["Conteudo"])

    freq = matriz_cluster.sum(axis=0).A1
    termos = vec_cluster.get_feature_names_out()
    top_idx = freq.argsort()[-15:][::-1]
    top_palavras = [termos[i] for i in top_idx]

    print(f"\nCluster {cluster_id} ({len(df_cluster)} posts):")
    print(f"  {' | '.join(top_palavras)}")

print("=" * 60)

# ── Filtro 3: remove ruido HDBSCAN ───────────────────────────────────────────
antes = len(df_filtrado)

# NOVO: este e o arquivo mais importante para o rebuttal
desc_ruido = df_filtrado[df_filtrado["hdbscan_cluster"] == -1].copy()
desc_ruido["motivo_descarte"] = "ruido_estatistico_hdbscan"
desc_ruido["etapa_descarte"]  = "F3_ruido_hdbscan"
desc_ruido.to_csv(os.path.join(DIR_DESC, "F3_ruido_hdbscan.csv"),
                  index=False, encoding="utf-8-sig")
print(f"\n[SALVO] {len(desc_ruido)} posts de ruido HDBSCAN -> F3_ruido_hdbscan.csv")

df_limpo = df_filtrado[df_filtrado["hdbscan_cluster"] != -1].copy()
df_limpo = df_limpo.reset_index(drop=True)
registra("3. Ruido HDBSCAN", len(df_limpo), antes - len(df_limpo), "hdbscan_cluster != -1")
print(f"Apos remover ruido HDBSCAN: {len(df_limpo)} posts")

# ── Filtro 4: confianca minima HDBSCAN ───────────────────────────────────────
antes = len(df_limpo)

# NOVO
desc_conf_hdb = df_limpo[df_limpo["hdbscan_confianca"] < CONFIANCA_MINIMA_HDBSCAN].copy()
desc_conf_hdb["motivo_descarte"] = f"confianca_hdbscan_menor_{CONFIANCA_MINIMA_HDBSCAN}"
desc_conf_hdb["etapa_descarte"]  = "F4_confianca_hdbscan"
desc_conf_hdb.to_csv(os.path.join(DIR_DESC, "F4_confianca_hdbscan_baixa.csv"),
                     index=False, encoding="utf-8-sig")

df_limpo = df_limpo[df_limpo["hdbscan_confianca"] >= CONFIANCA_MINIMA_HDBSCAN].copy()
df_limpo = df_limpo.reset_index(drop=True)
registra("4. Confianca HDBSCAN", len(df_limpo), antes - len(df_limpo),
         f"hdbscan_confianca >= {CONFIANCA_MINIMA_HDBSCAN}")
print(f"Apos filtro confianca HDBSCAN >= {CONFIANCA_MINIMA_HDBSCAN}: {len(df_limpo)} posts "
      f"(removidos {antes - len(df_limpo)})")

# ── Filtro 5: remove posts curtos ────────────────────────────────────────────
antes = len(df_limpo)

# NOVO
mask_curto = (df_limpo["Conteudo_Original"].str.len() < 50) | \
             (df_limpo["Conteudo"].str.split().str.len() < 5)
desc_curto = df_limpo[mask_curto].copy()
desc_curto["motivo_descarte"] = "post_curto"
desc_curto["etapa_descarte"]  = "F5_post_curto"
desc_curto.to_csv(os.path.join(DIR_DESC, "F5_post_curto.csv"),
                  index=False, encoding="utf-8-sig")

df_limpo = df_limpo[~mask_curto].copy()
df_limpo = df_limpo.reset_index(drop=True)
registra("5. Posts curtos", len(df_limpo), antes - len(df_limpo),
         ">= 50 caracteres e >= 5 palavras")
print(f"Apos filtro posts curtos: {len(df_limpo)} posts "
      f"(removidos {antes - len(df_limpo)})")

# ── Filtro 6: remove posts sem contexto mobile ───────────────────────────────
# Termos de marca do dominio analisado, omitidos nesta versao publica por
# restricao contratual (ver secao DISPONIBILIDADE DE ARTEFATO do artigo).
# Ex.: ["<fabricante>", "<submarca>"]
TERMOS_DOMINIO = []

palavras_mobile = TERMOS_DOMINIO + [
    "android", "telefone", "celular",
    "app", "wifi", "bluetooth", "tela", "bateria", "firmware",
    "atualiz", "configurac", "notificac", "chamada", "rede",
    "internet", "conexao", "microfone", "audio"
]
antes = len(df_limpo)
mask = df_limpo["Conteudo_Original"].str.lower().apply(
    lambda x: any(p in x for p in palavras_mobile)
)

# NOVO
desc_mobile = df_limpo[~mask].copy()
desc_mobile["motivo_descarte"] = "sem_contexto_mobile"
desc_mobile["etapa_descarte"]  = "F6_sem_contexto_mobile"
desc_mobile.to_csv(os.path.join(DIR_DESC, "F6_sem_contexto_mobile.csv"),
                   index=False, encoding="utf-8-sig")

df_limpo = df_limpo[mask].copy()
df_limpo = df_limpo.reset_index(drop=True)
registra("6. Contexto mobile", len(df_limpo), antes - len(df_limpo),
         "contem ao menos um termo de dominio mobile")
print(f"Apos filtro contexto mobile: {len(df_limpo)} posts "
      f"(removidos {antes - len(df_limpo)})")

# ── Filtro 7: remove duplicatas por URL ──────────────────────────────────────
antes = len(df_limpo)
df_limpo = df_limpo.sort_values("hdbscan_confianca", ascending=False)

# NOVO
desc_dup = df_limpo[df_limpo.duplicated(subset="URL_Topico", keep="first")].copy()
desc_dup["motivo_descarte"] = "duplicata_url"
desc_dup["etapa_descarte"]  = "F7_duplicata"
desc_dup.to_csv(os.path.join(DIR_DESC, "F7_duplicata_url.csv"),
                index=False, encoding="utf-8-sig")

df_limpo = df_limpo.drop_duplicates(subset="URL_Topico", keep="first")
df_limpo = df_limpo.reset_index(drop=True)
registra("7. Duplicatas por URL", len(df_limpo), antes - len(df_limpo),
         "URL_Topico unica")
print(f"Apos remover duplicatas: {len(df_limpo)} posts "
      f"(removidos {antes - len(df_limpo)})")

# ── NOVO: consolidado de TODOS os descartados ────────────────────────────────
colunas_base = [c for c in df.columns]
todos_desc = []
for d in [desc_topico, desc_conf_lda, desc_ruido, desc_conf_hdb,
          desc_curto, desc_mobile, desc_dup]:
    if len(d) > 0:
        cols = [c for c in colunas_base if c in d.columns] + \
               ["motivo_descarte", "etapa_descarte"]
        todos_desc.append(d[cols])

df_todos_desc = pd.concat(todos_desc).reset_index(drop=True)
df_todos_desc.to_csv(os.path.join(DIR_DESC, "TODOS_descartados.csv"),
                     index=False, encoding="utf-8-sig")

print("\n" + "=" * 70)
print("FUNIL DO PIPELINE")
print("=" * 70)
df_funil = pd.DataFrame(funil)
df_funil["pct_do_inicial"] = (df_funil["restantes"] / TOTAL_INICIAL * 100).round(1)
print(df_funil.to_string(index=False))
df_funil.to_csv(os.path.join(DIR_DESC, "funil_pipeline.csv"),
                index=False, encoding="utf-8-sig")

print(f"\nTotal descartado ao longo do pipeline: {len(df_todos_desc)}")
print(f"Total retido: {len(df_limpo)}")
print(f"Soma: {len(df_todos_desc) + len(df_limpo)} (esperado: {TOTAL_INICIAL})")

print("\nDescartados por motivo:")
print(df_todos_desc["motivo_descarte"].value_counts().to_string())

prop = df_todos_desc["etapa_descarte"].value_counts(normalize=True)
cotas = (prop * N_AMOSTRA_FN).round().astype(int)
while cotas.sum() != N_AMOSTRA_FN:
    if cotas.sum() < N_AMOSTRA_FN:
        cotas[cotas.idxmax()] += 1
    else:
        cotas[cotas.idxmax()] -= 1

amostras = []
for etapa, q in cotas.items():
    sub = df_todos_desc[df_todos_desc["etapa_descarte"] == etapa]
    amostras.append(sub.sample(min(q, len(sub)), random_state=SEED_AMOSTRA_FN))

df_amostra_fn = pd.concat(amostras).reset_index(drop=True)
df_amostra_fn["FN_ID"] = ["FN-%03d" % (i + 1) for i in range(len(df_amostra_fn))]

# colunas em branco para a anotacao manual dos dois anotadores
for col in ["anotacao_Luck", "anotacao_Joao", "consenso", "observacoes"]:
    df_amostra_fn[col] = ""

df_amostra_fn.to_csv(os.path.join(DIR_DESC, "amostra_falsos_negativos.csv"),
                     index=False, encoding="utf-8-sig")

print(f"\n[SALVO] Amostra de {len(df_amostra_fn)} posts para anotacao manual")
print("Cotas por etapa:")
print(cotas.to_string())
print("\nCategorias de anotacao: bug_software | nao_bug | ambiguo")

# ── Split 70/10/20 por cluster ────────────────────────────────────────────────
train_list, val_list, test_list = [], [], []

for cluster_id in sorted(df_limpo["hdbscan_cluster"].unique()):
    df_cluster = df_limpo[df_limpo["hdbscan_cluster"] == cluster_id].copy()

    #70% treino, 30% restante
    tr, temp = train_test_split(df_cluster, test_size=0.30, random_state=42)

    #10% validacao (0.333 do temp), 20% teste (0.666 do temp)
    va, te = train_test_split(temp, test_size=0.666, random_state=42)

    train_list.append(tr)
    val_list.append(va)
    test_list.append(te)

train_df = pd.concat(train_list).reset_index(drop=True)
val_df   = pd.concat(val_list).reset_index(drop=True)
test_df  = pd.concat(test_list).reset_index(drop=True)

print(f"\nSplit final:")
print(f"  Treino    : {len(train_df)} posts (70%)")
print(f"  Validacao : {len(val_df)} posts (10%)")
print(f"  Teste     : {len(test_df)} posts (20%)")

print(f"\nDistribuicao por cluster no treino:")
print(train_df["hdbscan_cluster"].value_counts().sort_index())
print(f"\nDistribuicao por cluster no teste:")
print(test_df["hdbscan_cluster"].value_counts().sort_index())

# ── Salvar ────────────────────────────────────────────────────────────────────
os.makedirs(os.path.join(BASE, "CSVs"), exist_ok=True)

df_limpo.to_csv(caminho_limpo,  index=False, encoding="utf-8-sig")
train_df.to_csv(caminho_treino, index=False, encoding="utf-8-sig")
val_df.to_csv(caminho_val,      index=False, encoding="utf-8-sig")
test_df.to_csv(caminho_teste,   index=False, encoding="utf-8-sig")

print("\nArquivos salvos:")
print(f"  {caminho_limpo}")
print(f"  {caminho_treino}")
print(f"  {caminho_val}")
print(f"  {caminho_teste}")
print(f"\nDescartados em: {DIR_DESC}/")