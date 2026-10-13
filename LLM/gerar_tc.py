import os
import pandas as pd
from deepseek import chamar_deepseek
from gpt import chamar_gpt
from llhama import chamar_llama

# ── Configuracao ──────────────────────────────────────────────────────────────
CASOS_BASE_CSV = "LLM/TestCase_List.csv"
TREINO_CSV     = "Cluster/CSVs/dataset_treino_llm.csv"
SAIDA_CSV      = "LLM/CSVs/gerados_treino_deepseek.csv" #troca o tive para oq for usar
N_EXEMPLOS     = 3   #quantos casos de teste usar como exemplo por cluster

os.makedirs("LLM", exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# NOTA SOBRE ESTA VERSAO PUBLICA
# A lista original de padroes continha trechos literais extraidos de relatos
# reais do forum e mencoes ao fabricante parceiro. Esses itens foram omitidos
# por restricao contratual e de privacidade (ver secao DISPONIBILIDADE DE
# ARTEFATO do artigo). Os padroes genericos foram mantidos. Para reproduzir a
# execucao original, preencha PADROES_DOMINIO com os padroes equivalentes do
# seu corpus.
# ─────────────────────────────────────────────────────────────────────────────

# Padroes especificos do dominio analisado (marca, modelos, trechos do corpus).
PADROES_DOMINIO = []

palavras_irrelevantes = PADROES_DOMINIO + [
    "libere uma atualizacao",
    "quando vao lancar",
    "quero o android",
    "quero participar do programa beta",
    "se inscreveu para beta",
    "por favor me avise quando",
    "aguardando atualizacao",
    "lista de precos",
    "quando foi ativado pela primeira vez",
    "voce pode verificar",
    "por que versoes sao lancadas",
    "esta mostrando retornado",
    "o que isso significa",
    "solicito gentilmente que voce forneca",
    "alguem se inscreveu",
    "preciso de substituicao",
    "vou comprar um novo telefone",
    "quando chega o android",
    "quando android",
    "por favor mandem",
    "havera beta",
    "por favor nao quebrem",
    "por favor nao adicionem",
    "voces podem por favor adicionar",
    "podem por favor adicionar",
    "gostaria de saber se ha alguma previsao",
    "estou escrevendo como usuario",
    "adoraria ver esse recurso",
    "solicito que iniciem oficialmente",
    "incluam o registro de alteracoes",
    "quando teremos a nova central",
    "pode adicionar um dicionario",
    "podem incluir um medidor",
    "faca uma boa atualizacao para",
    "quando iremos receber a atualizacao qpr",
    "tem noticias falando que o android",
    "eu gostaria de ver essa cor",
    "na proxima atualizacao adicione",
    "qual adaptador",
    "adicionem o suporte",
    "e possivel ter um medidor",
    "voces vao atualizar",
    "ha alguma chance de",
    "tela rachou",
    "protetor de tela",
    "pelicula de protecao",
    "bolha",
    "gostaria de sugerir",
    "espero que isso possa ser considerado",
    "quero que ele volte",
    "por favor nao nos force",
    "sera suportado no",
    "alguem sabe se vao fazer",
    "verificar a data de ativacao",
    "validade da garantia",
    "alguem enfrentou algum problema apos atualizar",
    "e uma atualizacao sem bugs",
    "alguem pode sugerir",
    "adicione novas fontes",
    "pedindo uma atualizacao de correcao",
    "adicionar medidor de velocidade",
    "adicionar recurso de bloqueio",
    "por favor adicione isso",
    "qual aplicativo do sistema eu devo atualizar",
    "o que ele faz exatamente",
    "review after using",
    "bateria",
    "dados de login",
]

# ── Carrega datasets ──────────────────────────────────────────────────────────
df_posts   = pd.read_csv(TREINO_CSV)
df_base    = pd.read_csv(CASOS_BASE_CSV)

df_posts["Conteudo_Original"] = df_posts["Conteudo_Original"].fillna("").astype(str)

print(f"Posts de treino   : {len(df_posts)}")
print(f"Casos base        : {df_base['test_id'].nunique()} casos")
print(f"Clusters          : {sorted(df_posts['hdbscan_cluster'].unique())}")

def formatar_caso(df_base, test_id):
    linhas = df_base[df_base["test_id"] == test_id]
    if linhas.empty:
        return ""
    summary = linhas.iloc[0]["summary"]
    setup   = linhas.iloc[0]["initial_setup"]
    passos  = []
    for _, row in linhas.iterrows():
        step   = str(row["step"]).strip()
        result = str(row["expected_result"]).strip()
        if step and step != "nan":
            passos.append(f"  - Step: {step}\n    Expected: {result}")
    texto = f"Summary: {summary}\n"
    if setup and str(setup) != "nan":
        texto += f"Initial Setup: {setup}\n"
    texto += "Steps:\n" + "\n".join(passos)
    return texto

def is_relevante(texto):
    texto = texto.lower()
    return any(p in texto for p in palavras_irrelevantes)

#seleciona N_EXEMPLOS casos base para cada cluster
#como nao temos mapeamento direto, usa os mesmos exemplos para todos os clusters
test_ids_disponiveis = df_base["test_id"].unique().tolist()
exemplos_fixos = test_ids_disponiveis[:N_EXEMPLOS]
exemplos_texto = "\n\n---\n\n".join([formatar_caso(df_base, tid) for tid in exemplos_fixos])

def montar_prompt(post_original, exemplos):
    return f"""You are a mobile software test engineer specialized in writing test cases for Android smartphones.

Below are {N_EXEMPLOS} real test cases from the industry partner as format reference:

{exemplos}

---

IMPORTANT RULES:
- Generate ONLY test cases for BUG REPORTS — posts describing unexpected behavior, crashes, or malfunctions.
- DO NOT generate test cases for: feature requests, questions, complaints about update delays, or hardware repair issues.
- The test case must REPRODUCE the bug described in the report, not verify that a feature exists or doesn't exist.
- Focus only on SOFTWARE behavior — do NOT include hardware repair steps.
- Steps must be specific and actionable — a tester should be able to follow them exactly.
- The "Expected" result must always describe the CORRECT behavior of a working device. If the bug is "X does not work", write Expected: "X should work correctly" — never describe the broken behavior as expected.

USER BUG REPORT:
{post_original}

Generate ONE software test case in the EXACT same format as the examples above:
Summary: TC - Verify [brief description of the bug behavior]
Initial Setup: [required preconditions, one per line]
Steps:
  - Step: [specific action to reproduce the bug]
    Expected: [what SHOULD happen if the bug is NOT present]
  - Step: [next action]
    Expected: [expected result]
(add as many steps as needed to reproduce and verify the bug)

Respond ONLY with the test case. No explanations, no preamble."""

# ── Processa posts ────────────────────────────────────────────────────────────
#df_posts = df_posts.head(3)
resultados = []
total = len(df_posts)

for i, row in df_posts.iterrows():
    post_original = row["Conteudo_Original"]
    cluster_id    = row["hdbscan_cluster"]

    if not post_original or len(post_original.strip()) < 20:
        print(f"[{i+1}/{total}] Post muito curto, pulando.")
        continue

    if is_relevante(post_original):
        print(f"[{i+1}/{total}] Conteudo irrelevante detectado, pulando.")
        continue

    prompt   = montar_prompt(post_original, exemplos_texto)
    resposta = chamar_deepseek(prompt)

    resultados.append({
        "post_index"       : i,
        "cluster"          : cluster_id,
        "topico_nome"      : row.get("topico_nome", ""),
        "url"              : row.get("URL_Topico", ""),
        "post_original"    : post_original,
        "caso_gerado"      : resposta,
    })

    print(f"[{i+1}/{total}] Cluster {cluster_id} — OK")

    # salva a cada 50 posts para nao perder progresso
    if (i + 1) % 50 == 0:
        pd.DataFrame(resultados).to_csv(SAIDA_CSV, index=False, encoding="utf-8-sig")
        print(f"  >> Checkpoint salvo: {i+1} posts processados")

# ── Salva resultado final ─────────────────────────────────────────────────────
df_resultado = pd.DataFrame(resultados)
df_resultado.to_csv(SAIDA_CSV, index=False, encoding="utf-8-sig")

print(f"\nConcluido!")
print(f"  Posts processados : {len(df_resultado)}")
print(f"  Salvo em          : {SAIDA_CSV}")
