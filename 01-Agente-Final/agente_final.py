import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults

from langchain.agents import initialize_agent, AgentType

# Carregar variáveis
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("ERRO: GOOGLE_API_KEY não encontrada.")

# Modelo LLM (Gemini 2.5 Flash)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Ferramentas
tools = [
    DuckDuckGoSearchResults(
        name="Pesquisa_Web",
        source="news",
        backend="api",
        safe="active",
        region="br-pt",   # <---- força resultados do Brasil
    )
]

# Criar agente estilo ReAct
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# Pergunta teste
question = (
    "Qual é o principal benefício da inteligência artificial generativa e "
    "onde ela está sendo mais aplicada no setor de saúde?"
)

print("\n🧠 Perguntando ao agente...\n")

response = agent.invoke({"input": question})

print("\n--- Resposta Final do Agente ---")
print(response["output"])
print("---------------------------------")
