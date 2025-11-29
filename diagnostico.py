import os
from dotenv import load_dotenv

# --- Teste de Pacotes Essenciais (Gemini + dotenv) ---
try:
    from google import genai
    print("✅ google-genai: OK")
except Exception as e:
    print(f"❌ google-genai: FALHA. Erro: {e}")

try:
    load_dotenv()
    if os.getenv("GEMINI_API_KEY"):
        print("✅ python-dotenv: OK (Chave Carregada)")
    else:
        print("❌ python-dotenv: FALHA (Chave não encontrada no .env)")
except Exception as e:
    print(f"❌ python-dotenv: FALHA. Erro: {e}")


# --- Teste de Pacotes LangChain (O Ponto de Falha Anterior) ---
print("\n--- Testando LangChain (Modularização) ---")

# Teste 1: Importação da Ferramenta de Busca (DuckDuckGo)
try:
    from langchain_community.tools import DuckDuckGoSearchRun
    print("✅ langchain-community.tools: OK")
except Exception as e:
    print(f"❌ langchain-community.tools: FALHA. Erro: {e}")

# Teste 2: Componente Básico (Prompt Template)
try:
    from langchain_core.prompts import ChatPromptTemplate
    print("✅ langchain-core.prompts: OK")
except Exception as e:
    print(f"❌ langchain-core.prompts: FALHA. Erro: {e}")

# Teste 3: O Executor do Agente (O Erro Persistente)
try:
    # Este é o caminho mais comum após a limpeza
    from langchain.agents import AgentExecutor
    from langchain.agents.react.base import create_react_agent 
    print("✅ langchain.agents: OK (AgentExecutor & create_react_agent)")
except Exception as e:
    print(f"❌ langchain.agents: FALHA. O caminho de importação está quebrado. Erro: {e}")


# --- Teste Final de LLM ---
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("✅ langchain-google-genai: OK")
except Exception as e:
    print(f"❌ langchain-google-genai: FALHA. Erro: {e}")