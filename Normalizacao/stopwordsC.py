# ─────────────────────────────────────────────────────────────────────────────
# Lista de stopwords customizadas do dominio.
#
# NOTA SOBRE ESTA VERSAO PUBLICA
# Dois conjuntos de termos foram removidos desta versao:
#
#   1. Termos de marca, submarca e identificadores de modelo do fabricante
#      parceiro, omitidos por restricao contratual (ver secao
#      DISPONIBILIDADE DE ARTEFATO do artigo). Preencha TERMOS_DOMINIO
#      abaixo com os termos equivalentes do seu dominio.
#
#   2. Nomes proprios que apareciam no corpus, removidos por se tratarem
#      de dados pessoais de usuarios do forum.
#
# A ausencia desses termos altera o vocabulario resultante em relacao a
# execucao original reportada no artigo.
# ─────────────────────────────────────────────────────────────────────────────

# Termos de marca, submarca e modelos do dominio analisado.
# Ex.: ["<fabricante>", "<submarca>", "<linha>", "<modelo_1>", "<modelo_2>"]
TERMOS_DOMINIO = []

STOPWORDS = list(set(TERMOS_DOMINIO + [

    # ── Dominio generico ──────────────────────────────────────────────────────
    "android", "celular", "aparelho", "telefone",
    "dispositivo", "aplicativo", "software", "produto", "atualizacao", "seguranca",
    "5g", "sistema", "opcao", "configuracao", "modo", "dado", "garantia", "suporte",
    "servico", "equipe", "google", "usuario", "recurso", "solucao", "versao",

    # ── Verbos genericos — sem acento ─────────────────────────────────────────
    "comprar", "pagar", "gostar", "recomendar", "tentar", "estar", "ser", "fazer",
    "ter", "haver", "ir", "usar", "resolver", "receber", "saber", "dizer",
    "ficar", "mostrar", "aparecer", "parecer", "poder", "dever", "ver",
    "conseguir", "querer", "precisar", "existir", "possuir", "funcionar",
    "funcionando", "continuar", "parar", "ligar", "atualizar", "acontecer",
    "encontrar", "chegar", "passar", "levar", "tornar", "acabar", "comecar",
    "incluir", "oferecer", "realizar", "utilizar", "tratar", "basear",
    "colocar", "deixar", "obter", "enfrentar", "chamar", "ouvir",
    "dar", "vir", "sera", "sair", "ocorrer", "lancar", "remover",
    "prometer", "vender", "entregar", "enviar", "perguntar", "responder",
    "falar", "descobrir", "autorizar", "trocar", "visitar", "consertar",
    "quebrar", "cair", "pensar", "significar", "informar", "verificar",
    "substituir", "editar", "confirmar", "participar", "inscrever",
    "aguardar", "esperar",

    # ── Verbos conjugados — com acento (texto original) ──────────────────────
    "estou", "esta", "está", "estão", "estamos", "estava", "estavam",
    "tenho", "tem", "têm", "temos", "tinha", "tinham",
    "fiz", "fez", "fizeram", "faço", "fazendo", "feito",
    "vou", "vai", "vão", "fui", "foi", "foram",
    "sei", "sabe", "sabem", "soube",
    "posso", "pode", "podem", "podia",
    "quero", "quer", "querem", "queria",
    "preciso", "precisa", "precisam",
    "consigo", "consegui", "conseguiu",
    "recebi", "recebeu", "receberam",
    "tentei", "tentou", "tentaram",
    "comprei", "comprou", "compraram",
    "usei", "usou", "usaram",
    "vi", "viu", "viram",
    "falar", "falei", "falou",
    "colocou", "colocaram",
    "deixou", "deixaram",
    "aconteceu", "aconteceram",
    "funcionou", "funcionaram",
    "reiniciei", "reiniciou",
    "instalei", "instalou",
    "atualizei", "atualizou",
    "encontrei", "encontrou",
    "resolvi", "resolveu",

    # ── Adverbios / intensificadores ──────────────────────────────────────────
    "claramente", "completamente", "totalmente", "extremamente", "simplesmente",
    "principalmente", "geralmente", "normalmente", "frequentemente", "especialmente",
    "definitivamente", "provavelmente", "bastante", "certeza", "realmente",
    "corretamente", "repente", "rapidamente", "atualmente", "recentemente",
    "também", "tambem", "já", "ja", "ainda", "apenas", "agora", "sempre",
    "nunca", "novamente", "depois", "antes", "durante", "enquanto",
    "então", "entao", "assim", "portanto", "porém", "porem",
    "embora", "contudo", "todavia",

    # ── Palavras genericas ────────────────────────────────────────────────────
    "forma", "parte", "coisa", "tipo", "maneira", "linha", "lado", "lugar",
    "caso", "ponto", "meio", "base", "geral", "total", "grande", "pequeno",
    "alto", "baixo", "cima", "acima", "abaixo", "dentro", "fora", "volta",
    "nivel", "estado", "ideia", "motivo", "razao", "questao", "situacao",
    "assunto", "resultado", "processo", "causa", "fato", "acordo", "relacao",
    "informacao", "detalhe", "resposta", "pessoa", "pessoal", "cliente",
    "empresa", "marca", "mercado", "mundo", "pais", "conta", "inicial",
    "completo", "ativo", "novo", "tempo", "modelo", "normal", "atual",
    "necessario", "disponivel", "seguro", "original", "hora",
    "numero", "semana", "futuro", "longo", "final", "canal", "pedido",
    "dano", "inferior", "antigo", "atraso", "operacional", "vejo",
    "contra", "protecao", "suporta", "mesmo", "muito", "outro", "outros",
    "outra", "outras", "todo", "todos", "toda", "todas", "cada", "qualquer",
    "nenhum", "nenhuma", "algum", "alguma", "alguns", "algumas",
    "esse", "essa", "esses", "essas", "este", "esta", "estes", "estas",
    "aquele", "aquela", "aqueles", "aquelas", "isso", "isto", "aquilo",
    "novo", "nova", "novos", "novas", "bom", "boa", "bons", "boas",
    "ruim", "ruins", "bem", "mal",

    # ── Preposicoes / artigos / conectivos — com e sem acento ─────────────────
    "de", "do", "da", "dos", "das", "no", "na", "nos", "nas",
    "ao", "aos", "à", "às", "pelo", "pela", "pelos", "pelas",
    "em", "para", "por", "com", "sem", "sobre", "entre", "até", "ate",
    "após", "apos", "desde", "sob", "perante", "mediante",
    "um", "uma", "uns", "umas", "o", "a", "os", "as",
    "que", "se", "ou", "mas", "e", "nem", "pois", "logo",
    "quando", "como", "onde", "quem", "qual", "quanto",
    "porque", "pq", "pra", "pro",

    # ── Pronomes ──────────────────────────────────────────────────────────────
    "eu", "me", "mim", "meu", "minha", "meus", "minhas",
    "tu", "te", "ti", "teu", "tua", "teus", "tuas",
    "ele", "ela", "eles", "elas", "lhe", "lhes",
    "nos", "nós", "nosso", "nossa", "nossos", "nossas",
    "vos", "vós", "vosso", "vossa",
    "você", "voce", "vocês", "voces", "seu", "sua", "seus", "suas",
    "se", "si", "lo", "la", "los", "las",

    # ── Cortesia / forum ──────────────────────────────────────────────────────
    "hello", "atenciosamente", "prezado", "prezada", "ajudar", "obrigado",
    "obrigada", "agradecer", "antecipadamente", "gentilmente", "solicitar",
    "fornecer", "avisar", "pedir", "sentir", "apreciado", "saudacoes",
    "ajuda", "site", "oficial", "centro", "programa", "contato",
    "ola", "oi", "sim", "nao", "não", "ok",

    # ── Datas / numeros ───────────────────────────────────────────────────────
    "hoje", "ontem", "janeiro", "fevereiro", "marco", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    "2023", "2024", "2025", "2026",
    "10", "11", "12", "13", "14", "15", "16", "17", "20", "25", "30", "40",
    "50", "60", "70", "80", "90", "100", "120", "01",

    # ── Ingles ────────────────────────────────────────────────────────────────
    "to", "it", "in", "is", "on", "and", "the", "has", "raw", "type", "etc",
    "ok", "have", "with", "phone", "forum", "store", "update", "feedback",
    "enter", "will", "like", "even", "good", "test", "screen", "device",
    "my", "your", "this", "that", "for", "not", "are", "was", "be", "an",
    "at", "by", "from", "or", "but", "if", "do", "did", "can", "could",
    "would", "should", "may", "might", "shall", "get", "got", "go", "went",

    # ── Lemas ruins do spaCy ──────────────────────────────────────────────────
    "alguir", "tamber", "rapir", "naoer", "facar", "serar", "digar",
    "playr", "corriger", "trar", "compr", "patche", "aler", "pecar",
    "obrigar", "alguer", "raper", "resolr", "recebir", "verifiqueir",
    "onlinar", "realizeir", "resolvar", "areo", "telo", "forun", "junteser",
    "indir", "canado", "atrave", "instagr", "fc", "ulti", "atra", "roso",
    "ruer", "configur", "mudanco", "atualizacoe", "funcoe", "condicoe",
    "opcoe", "informacoe", "disponivei", "paise", "deixeir", "desligo",
    "usalo", "ligalo", "faco", "vario", "haverar",

    # ── Hardware ──────────────────────────────────────────────────────────────
    "bateria", "carregar", "carregador", "carregamento", "carga", "descarregar",
    "usb", "usbc", "turbo", "energia", "porcentagem", "autonomia",
    "camera", "câmera", "foto", "video", "imagem", "lente", "zoom",
    "frontal", "traseiro", "tirar", "gravar", "captura", "gravacao", "resolucao",
    "tela", "display", "brilho", "exibicao", "toque", "sensivel",
    "stylus", "caneta", "dobravel", "flip", "fold", "dobradica",
    "ram", "processador", "chip", "hardware", "placa", "placamae",
    "armazenamento", "memoria", "espaco", "gb", "slot", "cartao",
    "impressao", "digital", "impressao digital", "esim", "botao",
    "volume", "externo", "desbloquear", "capa", "power",
    "cabo", "sensor", "sensor proximidade", "proximidade", "vibracao", "pelicula",
    "hdr", "fone",

    # ── Beta / roadmap / comunidade ───────────────────────────────────────────
    "beta", "inscrevi", "cronograma", "reino", "oportunidade", "estavel",
    "bimestral", "data lancamento", "atualizacoes atualizacoes",
    "regra", "violacao", "violacao regra", "diretriz", "diretriz comunidade",
    "politica", "postar", "perfil", "idioma", "visite", "registro",
    "bootloader", "recebera", "comunidade", "lancamento", "previsao", "prazo",
    "android 16", "android 17", "teste beta",

    # ── Suporte / reparo fisico ───────────────────────────────────────────────
    "substituicao", "reparo", "email", "verde", "preto",
    "loja", "tecnico", "atendimento", "custo", "peca",
    "canto", "gratuito", "india", "índia", "europa", "brasil",
    "compra", "decepcionante", "consumidor", "promessa", "indiano",
    "agente", "papel", "parede", "papel parede",

    # ── Idiomas e localidades que poluem ──────────────────────────────────────
    "araber", "testalo", "timeline", "italiano",
    "previsto", "distribuer", "saudita", "araber saudita", "razoes",
    "desconheco", "receberao", "variante", "notar",
    "canada", "italia", "ingles", "resto", "that", "note",

    # ── Genericos que ainda poluem ────────────────────────────────────────────
    "favor", "ha", "mais", "dias", "meses", "vezes", "vez",
    "disso", "alem", "cerca", "comecou", "tudo", "nada",
    "alguem", "parece", "algo", "gostaria", "possivel",
    "espero", "estao", "aqui", "tiver", "manter",

    # ── Lixo tecnico ──────────────────────────────────────────────────────────
    "https", "link", "mfn",

    # ── Tempo / conversa generica ─────────────────────────────────────────────
    "dia", "dias", "ano", "anos", "mes", "meses", "havia",
    "era", "disse", "disseram", "devo", "poderia", "tao",
    "sinal", "menos", "persiste",

    # ── Roadmap ───────────────────────────────────────────────────────────────
    "esperando", "bimestrais", "regioes", "junte", "rom",
    "atrasos", "seguir", "ajude", "perguntas",

    # ── Lixo ──────────────────────────────────────────────────────────────────
    "serie", "marcas", "modelos",
    "telefones", "usuarios", "dispositivos",
    "fi", "wi", "wi fi",

    # ── Verbos subjuntivo/condicional que escaparam ───────────────────────────
    "seria", "deveria", "seja", "tenha", "fosse", "tivesse",
    "pudesse", "houvesse", "estivesse",

    # ── Moderacao / edicao ────────────────────────────────────────────────────
    "editado", "editado devido", "removido", "visitei", "diagnostico",

    # ── Roadmap ainda sobrando ────────────────────────────────────────────────
    "futuras", "futuras atualizacoes", "quaisquer", "fique",
    "oportunidades", "paises", "suave", "vindo", "primeira",

    # ── Genericos ─────────────────────────────────────────────────────────────
    "tendo", "linhas", "protetor", "presente", "mae",
    "pessoas", "mesma", "diretamente", "superior", "fix",
    "smartphone", "tenha", "seja", "so", "sao",
    "unido", "australia", "version", "of", "formulario",
    "experimentar", "proteger", "unidos",
    "assistencia", "danos", "traseira", "capturas",
    "resolvido", "defeito",
    "ai", "ia", "musica", "fotos", "midia",
    "pc", "via", "auto", "fio",
    "sou", "forneca", "deve", "muitos",
    "clientes", "ultima", "due",
    "photos", "vontade", "maximo", "dicas", "conecte",
    "olho", "veja", "vulnerabilidades", "requisitos",
    "regras", "devido regras", "pessoais", "acho", "tentando",
    "possa", "vem", "maximo", "passos",
    "tarde", "ligado", "desligado", "mostra",
    "perfeitamente", "recebendo", "entrar", "anuncios", "empresas",
    "frances", "cronogramas",
    "trabalho", "unico", "neste", "relacionado", "acontecendo",
    "lancado", "util", "sendo", "disponiveis",
    "importantes", "quadro", "instalados", "grandes",
    "ambos", "pouco", "faz", "acabei", "noite", "segura",
    "contatos", "varios",
]))
