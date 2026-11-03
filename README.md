# Geração Automatizada de Casos de Teste a partir de Relatos de Usuários

Pacote de artefatos do artigo *Test Case Generation Based on User Complaints*, publicado no XXV Simpósio Brasileiro de Qualidade de Software (SBQS 2026), Maringá, PR, 10 a 13 de novembro de 2026.

**Artigo (versão dos autores):** o PDF acompanha este depósito e está disponível em https://doi.org/10.5281/zenodo.23933219

## Descrição geral

O artigo propõe uma abordagem automatizada para geração de casos de teste manuais a partir de relatos informais de usuários publicados em um fórum público de suporte técnico, voltada a aplicações móveis Android. O pipeline combina processamento de linguagem natural, modelagem de tópicos com LDA, clusterização com HDBSCAN e geração por modelos de linguagem de grande porte, com avaliação da qualidade estrutural por meio da abordagem LLM-as-a-Judge.

Este pacote contém o código dos quatro módulos do pipeline, os resultados agregados reportados no artigo e o material sintético produzido pelos autores para o experimento de ablação.

## Organização do repositório

```
Normalizacao/
  normalizacao_luck.py           coleta e normalizacao textual (Modulo 1)
  stopwordsC.py                  lista de stopwords customizadas
  Gerar_topicos_lda_.py          modelagem de topicos com LDA (Modulo 2)
  Tfidf.py                       relatorio TF-IDF por topico (Modulo 2)
Cluster/
  Cluster.py                     clusterizacao e encadeamento de filtros (Modulo 3)
  CSVs/descartados/
    funil_pipeline.csv           fluxo quantitativo das sete etapas de
                                 filtragem (Tabela 2 do artigo)
LLM/
  gerar_tc.py                     geracao dos casos de teste (Modulo 4)
  gpt.py, deepseek.py, llhama.py  clientes dos tres modelos avaliados
Ablacao/
  posts_corner_cases.csv          30 relatos sinteticos em 7 categorias
                                  (Secao 5.1 do artigo)
  corner_cases_com_tcs.csv        casos de teste gerados para esses relatos
  corner_cases_com_tcs.xlsx       o mesmo conteudo em planilha, para leitura
LICENSE                           licenca MIT
```

## Requisitos de sistema

### Ambiente

Ambiente verificado em novembro de 2026, em **Windows PREENCHER_VERSAO** com **Python 3.14.4**. Os scripts não foram testados em outros sistemas operacionais nem em outras versões do Python.

### Dependências de terceiros

Os scripts importam apenas estes cinco pacotes externos:

| Pacote | Versão | Onde é usado |
|---|---|---|
| `pandas` | 3.0.2 | leitura e escrita de todos os CSVs, em todos os módulos |
| `scikit-learn` | 1.8.0 | `CountVectorizer`, `TfidfVectorizer`, `LatentDirichletAllocation`, `train_test_split` (Módulos 2 e 3) |
| `hdbscan` | 0.8.42 | clusterização por densidade (Módulo 3) |
| `requests` | 2.33.1 | chamadas HTTP às três LLMs (Módulo 4) |
| `spacy` | ver nota abaixo | lematização, com o modelo `pt_core_news_sm` (Módulo 1) |

**Nota sobre o spaCy:** o Módulo 1 depende do spaCy com o modelo `pt_core_news_sm`. A versão utilizada na execução original não foi registrada, e o ambiente foi posteriormente reconstruído, de modo que o spaCy não está presente no Python 3.14.4 verificado acima. Quem for reexecutar o Módulo 1 deve instalar uma versão do spaCy compatível com o seu interpretador e baixar o modelo com `python -m spacy download pt_core_news_sm`.

Os demais módulos importados (`os`, `sys`, `csv`, `re`, `unicodedata`) fazem parte da biblioteca padrão do Python.

### Serviços externos

| Serviço        |                                          Endpoint |          Autenticação |
|----------------|---------------------------------------------------|-----------------------|
| OpenAI         | `https://api.openai.com/v1/chat/completions`| variável `OPENAI_API_KEY` |
| DeepSeek       | `https://api.deepseek.com/chat/completions` | variável `DEEPSEEK_API_KEY` |
| Ollama (local) | `http://localhost:11434/api/generate`       | nenhuma |

## Instalação

```bash
pip install pandas scikit-learn hdbscan spacy requests
python -m spacy download pt_core_news_sm
```

Para o modelo local:

```bash
ollama pull llama3.1
```

## Configuração

As chaves de API são lidas de variáveis de ambiente. Nenhuma chave está incluída neste pacote.

```bash
export OPENAI_API_KEY="sua-chave"
export DEEPSEEK_API_KEY="sua-chave"
```

O cliente do LLaMA espera o Ollama em `http://localhost:11434`.

## Ordem de execução

Os scripts assumem execução a partir da raiz do repositório e dependem dos arquivos de dados descritos na seção seguinte, que não acompanham este pacote.

1. `python Normalizacao/normalizacao_luck.py` — normaliza o corpus bruto e produz o dataset limpo
2. `python Normalizacao/Gerar_topicos_lda_.py` — aplica LDA e atribui tópicos
3. `python Normalizacao/Tfidf.py` — gera o relatório TF-IDF usado para refinar iterativamente a lista de stopwords
4. `python Cluster/Cluster.py` — reaplica o LDA sobre os tópicos retidos, clusteriza com HDBSCAN e aplica o encadeamento de sete filtros; produz o funil quantitativo e os conjuntos de treino, validação e teste
5. `python LLM/gerar_tc.py` — gera os casos de teste com os três modelos

Os CSVs intermediários são gravados em `Normalizacao/CSVs/`, `pfv_funciona/`, `Cluster/CSVs/` e `LLM/CSVs/`. Esses diretórios acompanham o repositório vazios, com um `.gitkeep`, porque os caminhos estão fixos nos scripts.

## O que não está incluído, e por quê

A base de relatos e todos os artefatos dela derivados não podem ser compartilhados publicamente devido a restrições contratuais e de confidencialidade associadas ao projeto de pesquisa em parceria com a indústria, conforme declarado na seção DISPONIBILIDADE DE ARTEFATO do artigo.

Embora os dados brutos sejam provenientes de um fórum publicamente acessível, as etapas de processamento e enriquecimento vinculam os artefatos a informações que poderiam identificar a empresa parceira e expor padrões de falhas de produtos específicos.

Não acompanham este pacote:

- a base coletada e suas versões intermediárias;
- os relatos descartados em cada etapa de filtragem;
- os casos de teste gerados a partir dos relatos reais e suas avaliações;
- o script de coleta, que expõe o endereço do fórum.

Três conjuntos de termos também foram removidos do código, e a remoção está anotada no próprio arquivo em cada caso:

1. **Termos de marca e identificadores de modelo**, nas listas `TERMOS_DOMINIO` de `Normalizacao/stopwordsC.py` e `Cluster/Cluster.py`, e na lista `PADROES_DOMINIO` de `LLM/gerar_tc.py`. As listas foram mantidas vazias.

2. **Trechos literais de relatos** que compunham a heurística de filtragem em `LLM/gerar_tc.py`. Os padrões genéricos foram preservados.

3. **Nomes próprios de usuários do fórum** incorporados à lista de stopwords durante o refinamento iterativo. Removidos sem substituição.

Nos relatos sintéticos, escritos pelos próprios autores, as menções a fabricantes e modelos foram substituídas por identificadores da forma `[FABRICANTE]` e `[MODELO-N]`, preservando a categoria de dificuldade de cada caso.

**Consequência para a reprodução:** executar o pipeline com as listas de domínio vazias produz um vocabulário diferente do reportado no artigo. Para aplicar a abordagem a outro domínio, preencha as três listas com os termos equivalentes.

## Considerações éticas

Os relatos que compõem a base original são públicos, publicados por usuários em um fórum de suporte técnico aberto a qualquer pessoa registrada. Nenhum dado pessoal identificável é redistribuído neste pacote: os identificadores de
autor nunca saíram do ambiente de processamento, e os nomes próprios que haviam sido incorporados à lista de stopwords durante o refinamento foram removidos antes da publicação.

Os relatos sintéticos incluídos no pacote foram redigidos pelos autores para o experimento de ablação e não correspondem a nenhum usuário real.

## Licença

MIT. Ver `LICENSE`.

## Contato

Pesquisadores interessados em reproduzir a abordagem podem entrar em contato com os autores para discutir possibilidades de compartilhamento parcial dos demais artefatos.
