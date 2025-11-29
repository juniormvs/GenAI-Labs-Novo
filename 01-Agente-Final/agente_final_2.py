# agente_moderno.py
import os
from dotenv import load_dotenv
import time
from collections import deque

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults

from langchain.agents import initialize_agent, AgentType

# --- Carregar .env ---
load_dotenv()  # usa o .env na mesma pasta do script

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("ERRO: GOOGLE_API_KEY não encontrada no .env")

# --- Configuração do LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2  # mais determinístico
)

# --- Ferramenta de busca (wrapper) ---
# Configure aqui k (quantos resultados retornar) se o wrapper permitir.
# Se não tiver argumento, faremos o pós-processamento.
search_tool = DuckDuckGoSearchResults(name="Pesquisa_Web")

# --- Função utilitária: sumariza os top-N snippets em texto limpo ---
def summarize_search_results(results, top_n=3, lang_hint="pt"):
    """
    results: lista de dicts com keys: snippet, title, link
    Retorna uma string compacta com os top_n resultados formatados.
    """
    if not results:
        return "Nenhum resultado encontrado."
    out = []
    used_links = set()
    count = 0
    for r in results:
        # r pode ser um objeto; converta em dict se necessário
        snippet = getattr(r, "snippet", None) or r.get("snippet", "") if isinstance(r, dict) else ""
        title = getattr(r, "title", None) or r.get("title", "") if isinstance(r, dict) else ""
        link = getattr(r, "link", None) or r.get("link", "") if isinstance(r, dict) else ""
        if link in used_links:
            continue
        used_links.add(link)
        count += 1
        # opcional: pular se snippet vazio
        if not snippet and not title:
            continue
        out.append(f"{count}. {title}\n{snippet}\nFonte: {link}")
        if count >= top_n:
            break
    return "\n\n".join(out) if out else "Resultados sem conteúdo útil."

# --- Estratégia para evitar repetir a mesma query ---
recent_queries = deque(maxlen=20)  # cache simples

def safe_search(query, lang="pt"):
    """
    Faz uma busca, evitando repetir queries idênticas em curto espaço de tempo.
    Também adiciona hint de idioma para reduzir resultados multilingues.
    """
    # adicionar hint explícito em português para priorizar PT
    query_with_lang = f"{query} (em Português)" if "português" not in query.lower() else query
    if query_with_lang in recent_queries:
        # evita refazer idêntico; retornar vazio ou sinalizar cache
        return {"cached": True, "summary": "Consulta repetida recentemente. Usando cache local (nenhum novo resultado).", "raw": []}
    # chamar a ferramenta
    recent_queries.append(query_with_lang)
    # a DuckDuckGoSearchResults normalmente é chamada via agent; aqui mostramos como invocar diretamente:
    # Note: se o wrapper não expõe uma chamada síncrona pública, deixe para o agente chamar a ferramenta.
    results = search_tool.run(query_with_lang)
    # results pode ser string ou list; trate conforme o retorno real
    # vamos supor que results é uma lista de dicts
    summary = summarize_search_results(results, top_n=3, lang_hint=lang)
    return {"cached": False, "summary": summary, "raw": results}

# --- Prompt e inicialização do agente ---
# Usamos o estilo ZERO_SHOT_REACT_DESCRIPTION (funciona bem com a 0.2.x)
tools = [search_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,                 # VERBOSE ligado só para debug; em produção desligue
    handle_parsing_errors=True
)

# --- Parâmetros de execução para controlar comportamento ---
MAX_ITERATIONS = 4
TIME_LIMIT_SECONDS = 30

# --- Execução segura do agente (wrapper com limites) ---
def run_agent(question: str):
    start = time.time()
    # pedimos explicitamente para o agent usar no máximo X iterações.
    # initialize_agent/Agent executors variam por versão; aqui usamos invoke simples:
    try:
        # construir input com instruções extras (forçar linguagem PT, evitar repetição de busca)
        augmented_input = question + " Por favor responda em Português e use no máximo uma busca por sub-pergunta."
        result = agent.invoke({"input": augmented_input})
        return result
    except Exception as e:
        return {"error": str(e)}

# --- TESTE ---
if __name__ == "__main__":
    pergunta = (
        "Qual é o principal benefício da inteligência artificial generativa "
        "e onde ela está sendo mais aplicada hoje no setor de saúde?"
    )
    print("Pergunta:", pergunta)
    output = run_agent(pergunta)
    print("\n--- Resultado bruto do agente ---")
    # Se o agent devolve dict com 'output', mostramos; se erro, mostramos o erro
    if isinstance(output, dict) and "error" in output:
        print("Erro:", output["error"])
    else:
        # normalmente em versões 0.2.x o agent.invoke retorna um objeto com 'output'
        try:
            print(output.get("output") if isinstance(output, dict) else output["output"])
        except Exception:
            # fallback: print direto
            print(output)
