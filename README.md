🔥 Agente de IA com LangChain + Gemini 2.5 Flash

Primeira versão de um agente ReAct em Python, utilizando:

Google Gemini 2.5 Flash (via langchain-google-genai)

LangChain 0.2.14

Ferramenta de busca DuckDuckGoSearchResults

Pipeline de raciocínio ReAct (Thought → Action → Observation → Answer)

Este projeto faz parte da minha evolução prática em IA aplicada e será expandido para versões mais poderosas nos próximos repositórios.

🚀 Objetivo do Projeto

Criar um agente de IA capaz de:

receber perguntas do usuário,

decidir quando deve pesquisar na web,

raciocinar em múltiplos passos,

e entregar uma resposta final estruturada.

Este é o primeiro protótipo e serve como base para versões futuras mais completas.

🧠 Tecnologias Utilizadas

Python 3.11

LangChain 0.2.14

langchain-google-genai 1.0.5

DuckDuckGo Search Tool

Gemini 2.5 Flash

## 📂 Estrutura do Projeto

```bash
.
└── 01-Agente-Final/
    ├── agente_final.py
    ├── agente_interativo.py
    ├── teste_env.py
    ├── .env
    └── README.md

```
🔑 Como Executar

1️⃣ Ative seu ambiente virtual
```
source venv/bin/activate
```

2️⃣ Instale as dependências
```
pip install -r requirements.txt
```

3️⃣ Crie um arquivo .env
```
GOOGLE_API_KEY="sua_chave_aqui"
```

4️⃣ Rode o agente
```
python3 agente_final.py
```
🛠️ Como Funciona o Agente

O agente implementa o padrão ReAct, realizando:

Thought → Action → Observation → Thought → Final Answer


Ele usa o DuckDuckGo para buscar informações externas e o modelo Gemini para raciocinar sobre elas.

📌 Exemplo de Uso

Pergunta:

Qual é o principal benefício da inteligência artificial generativa na área da saúde?

Resposta (resumida):

O principal benefício é acelerar a inovação, personalizar diagnósticos e desenvolver medicamentos utilizando geração de dados sintéticos e análise avançada.

📌 Próximas Versões (Roadmap)

🔧 Versão interativa em loop

🔧 Agentes com Memória

🔧 Agente com múltiplas ferramentas (tradução, RAG, scraping)

🔧 Interface web com Gradio ou Streamlit

🔧 Agente para análise de empresas (CNPJ, dados abertos, etc.)

🧑‍💻 Autor

Mário Junior
Construindo portfólio na área de IA e se tornando referência em TI com projetos reais.
