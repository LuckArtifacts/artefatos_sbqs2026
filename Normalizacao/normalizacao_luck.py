import unicodedata, re, pandas as pd
import spacy

nlp = spacy.load("pt_core_news_sm")

correcoes = {
    "nao": "nao", "tb": "tambem", "vc": "voce", "pq": "porque",
    "qdo": "quando", "kd": "onde", "oq": "oque", "mto": "muito",
}

def remover_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )

def normalizar_e_lematizar(texto):
    if not isinstance(texto, str):
        return ""
    
    texto = texto.lower()
    texto = remover_acentos(texto)
    texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    texto = re.sub(r'http\S+', '', texto)
    
    texto = re.sub(r'\b\d+\b', '', texto)
    texto = re.sub(r'[^a-z\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # lematização
    tokens_brutos = texto.split()
    tokens_corrigidos = [correcoes.get(t, t) for t in tokens_brutos]
    texto = " ".join(tokens_corrigidos)

    doc = nlp(texto)
    tokens = [
        token.lemma_ for token in doc
        if not token.is_punct
        and not token.is_space
        and len(token.lemma_) > 3        
        and token.is_alpha
        and token.lemma_.isascii() 
    ]
    return " ".join(tokens)

def normalizar_sem_lematizar(texto):
    if not isinstance(texto, str):
        return ""
    
    texto = texto.lower()
    texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def extrarir_modelo(url):
    if not isinstance(url, str):
        return ""
    
    modelo_bruto = re.search(r'/t5/([^/]+)/', url)
    if modelo_bruto:
        modelo = modelo_bruto.group(1)
        modelo = modelo.replace("-", " ")
        return modelo
    return ""

df = pd.read_csv("Testes/CSVs/funciona.csv", encoding="utf-8-sig")

print(f"Dados originais: {len(df)} linhas.")
    
#df = df.drop_duplicates(subset=['Autor', 'Conteudo'])

df['Conteudo_Original'] = df['Conteudo'].apply(normalizar_sem_lematizar)
df['Titulo_Original']   = df['Titulo_Topico'].apply(normalizar_sem_lematizar)

df['Titulo_Topico'] = df['Titulo_Topico'].apply(normalizar_e_lematizar)
df['Conteudo'] = df['Conteudo'].apply(normalizar_e_lematizar)
df["Modelo"] = df["URL_Topico"].apply(extrarir_modelo)

df = df[['Titulo_Topico', 'Titulo_Original', 'Modelo', 'Autor', 'Conteudo', 'Conteudo_Original', 'URL_Topico']] 

print(f"Dados após limpeza: {len(df)} linhas.")

df.to_csv("Normalizacao/CSVs/dataset_que_talvez_ta_certo.csv", index=False, encoding="utf-8-sig")