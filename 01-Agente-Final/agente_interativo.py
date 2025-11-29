import os
from dotenv import load_dotenv

# LLM moderno para Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

# Ferramenta de busca
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults

# Prompt ReAct moderno
from langchain_core.prompts import ChatPromptTemplate

# Criador atual de agentes ReAct
from langchain.agents import create_react_agent, AgentExecutor


# ------------------------------
# 1. Carregar variáveis de ambiente
# ------------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("ERRO: GOOGLE_API_KEY não encontrada no .env")


# ------------------------------
# 2. Definir o LLM (Gemini)
# ------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.4,
)


# ------------------------------
# 3. Ferramentas disponíveis
# ------------------------------
tools = [
    DuckDuckGoSearchResults(name="Pesquisa_Web")
]


# ------------------------------
# 4. Criar o Prompt ReAct moderno
# ------------------------------
prompt_template = """
Você é um agente inteligente. Use as ferramentas abaixo quando necessário.

{tools}

Use este formato:

Question: pergunta do usuário
Thought: seu raciocínio passo a passo
Action: ferramenta a usar (somente uma de {tool_names})
Action Input: entrada da ferramenta
Observation: resultado da ferramenta
... repita se necessário ...
Thought: agora sei a resposta final
Final Answer: resposta final

Comece!

Question: {input}
{agent_scratchpad}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)


# ------------------------------
# 5. Criar Agente ReAct moderno
# ------------------------------
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # mostra pensamento e chamadas
)



# ------------------------------
# 6. Loop interativo com você
# ------------------------------
print("\n🤖 Agente Interativo iniciado! (Digite 'sair' para encerrar)\n")

while True:
    pergunta = input("Você: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Agente: Até mais! 👋")
        break

    resposta = agent_executor.invoke({"input": pergunta})
    print("\nAgente:", resposta["output"], "\n")
