# Geração Automatizada de Casos de Teste a partir de Relatos de Usuários

Pacote de artefatos do artigo *Test Case Generation Based on User Complaints*,publicado no XXV Simpósio Brasileiro de Qualidade de Software (SBQS 2026), Maringá, PR, 10 a 13 de novembro de 2026.

**Artigo (versão dos autores):** https://doi.org/10.5281/zenodo.23352112

**Badge solicitado:** Available

## Descrição geral

O artigo propõe uma abordagem automatizada para geração de casos de testemanuais a partir de relatos informais de usuários publicados em um fórumpúblico de suporte técnico, voltada a aplicações móveis Android. O pipeline combina processamento de linguagem natural, modelagem de tópicos com LDA,clusterização com HDBSCAN e geração por modelos de linguagem de grande porte,com avaliação da qualidade estrutural por meio da abordagem LLM-as-a-Judge.

Este pacote contém o código dos quatro módulos do pipeline, os resultadosagregados reportados no artigo e o material sintético produzido pelos autores para o experimento de ablação.

## Organização do repositório

```
Normalizacao/
  normalizacao_luck.py           coleta e normalizacao textual (Modulo 1)
  stopwordsC.py                  lista de stopwords customizadas
  Tfidf.py                       relatorio TF-IDF por topico (Modulo 2)
  Gerar_topicos_lda_.py          modelagem de topicos com LDA (Modulo 2)
Cluster/
  Cluster.py                     clusterizacao e encadeamento de filtros (Modulo 3)
  CSVs/descartados/
    funil_pipeline.csv            fluxo quantitativo das sete etapas de filtragem(Tabela 2 do artigo)
LLM/
  gerar_tc.py                     geracao dos casos de teste (Modulo 4)
  gpt.py, deepseek.py, llhama.py  clientes dos tres modelos avaliados
Ablacao/
    posts_corner_cases.csv         30 relatos sinteticos em 7 categorias (Secao 5.1)
    corner_cases_com_tcs.csv       casos de teste gerados para os relatos sinteticos
LICENSE                            licenca MIT
```

## Requisitos de sistema

- Python 3
- Acesso às APIs da OpenAI e da DeepSeek (chaves próprias)
- Ollama instalado localmente, para o LLaMA 3.1 8B

Os scripts foram desenvolvidos e executados em Windows. Não foram testados em outros sistemas operacionais.

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

As chaves de API são lidas de variáveis de ambiente. Nenhuma chave está
incluída neste pacote.

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

Os CSVs intermediários são gravados em `Normalizacao/CSVs/`, `pfv_funciona/`,
`Cluster/CSVs/` e `LLM/CSVs/`. Esses diretórios acompanham o repositório vazios,
com um `.gitkeep`, porque os caminhos estão fixos nos scripts.

## O que não está incluído, e por quê

A base de relatos e todos os artefatos dela derivados não podem ser compartilhados publicamente devido a restrições contratuais e deconfidencialidade associadas ao projeto de pesquisa em parceria com a indústria, conforme declarado na seção DISPONIBILIDADE DE ARTEFATO do artigo.

Embora os dados brutos sejam provenientes de um fórum publicamente acessível, as etapas de processamento e enriquecimento vinculam os artefatos a informações que poderiam identificar a empresa parceira e expor padrões de falhas de produtos específicos.

Não acompanham este pacote:

- a base coletada e suas versões intermediárias;
- os relatos descartados em cada etapa de filtragem;
- os casos de teste gerados a partir dos relatos reais e suas avaliações;
- o script de coleta, que expõe o endereço do fórum.

Três conjuntos de termos também foram removidos do código, e a remoção está anotada no próprio arquivo em cada caso:

1. **Termos de marca e identificadores de modelo**, nas listas
   `TERMOS_DOMINIO` de `Normalizacao/stopwordsC.py` e `Cluster/Cluster.py`, e na lista `PADROES_DOMINIO` de `LLM/gerar_tc.py`. As listas foram mantidas vazias.

2. **Trechos literais de relatos** que compunham a heurística de filtragem em `LLM/gerar_tc.py`. Os padrões genéricos foram preservados.

3. **Nomes próprios de usuários do fórum** incorporados à lista de stopwords durante o refinamento iterativo. Removidos sem substituição.

Nos relatos sintéticos, escritos pelos próprios autores, as menções a fabricantes e modelos foram substituídas por identificadores da forma `[FABRICANTE]` e `[MODELO-N]`, preservando a categoria de dificuldade de cada caso.

**Consequência para a reprodução:** executar o pipeline com as listas de domínio vazias produz um vocabulário diferente do reportado no artigo. Para aplicar a abordagem a outro domínio, preencha as três listas com os termos equivalentes.

## Considerações éticas

Os relatos que compõem a base original são públicos, publicados por usuários em um fórum de suporte técnico aberto a qualquer pessoa registrada. Nenhum dado pessoal identificável é redistribuído neste pacote: os identificadores de autor nunca saíram do ambiente de processamento, e os nomes próprios que haviam sido incorporados à lista de stopwords durante o refinamento foram removidos antes da publicação.

Os relatos sintéticos incluídos no pacote foram redigidos pelos autores para o experimento de ablação e não correspondem a nenhum usuário real.

## Licença

MIT. Ver `LICENSE`.

## Contato

Pesquisadores interessados em reproduzir a abordagem podem entrar em contato com os autores para discutir possibilidades de compartilhamento parcial dos demais artefatos.
