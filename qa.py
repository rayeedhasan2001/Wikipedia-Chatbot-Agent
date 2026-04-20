from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.schema.messages import AIMessage
from langchain.schema.runnable import RunnableLambda
from langgraph.graph import StateGraph, END
from backend.models import QuestionRequest, AnswerResponse
from backend.services.vector_store import get_vectorstore
from backend.services.llm import get_llm
from backend.services.wikipedia import get_wikipedia_tool
from backend.scripts.load_documents import load_and_process_documents  # Import the load function

router = APIRouter()

class GraphState(TypedDict):
    question: str
    documents: List[Document]
    answer: str
    next_step: str

# Load documents when the application starts
load_and_process_documents()

def retrieve(state: GraphState) -> GraphState:
    print("Retrieve:")
    vector_store = get_vectorstore()
    documents = vector_store.as_retriever().get_relevant_documents(state['question'])
    return {**state, "documents": documents, "next_step": "generate_answer"}

def wiki_search(state: GraphState) -> GraphState:
    print("Wiki Search:")
    wiki_tool = get_wikipedia_tool()
    results = wiki_tool.run(state['question'])
    results = Document(page_content=results)
    return {**state, "documents": [results], "next_step": "generate_answer"}

def route_question(state: GraphState) -> GraphState:
    print("Route Question")
    llm = get_llm()
    
    system = """
    You are an expert at routing a user question to a vectorstore or wikipedia.
    The vectorstore contains documents related to agents, prompts engineering, and adversarial attacks.
    Use the vectorstore for questions on these topics otherwise perform wikipedia search.
    """
    
    route_prompt = ChatPromptTemplate.from_messages([
        ('system', system),
        ('human', "{question}"),
    ])
    
    class RouteQuery(BaseModel):
        datasource: Literal['vectorstore', 'wikisearch']
    
    structured_llm_router = llm.with_structured_output(RouteQuery)
    ques_router = route_prompt | structured_llm_router
    
    source = ques_router.invoke({"question": state['question']})

    if source.datasource == "wikisearch":
        print("Route question to Wiki Search")
        return {**state, "next_step": "wiki_search"}
    elif source.datasource == "vectorstore":
        print("Route question to RAG SYSTEM")
        return {**state, "next_step": "retrieve"}
    else:
        raise ValueError("Unknown datasource returned from router.")

def generate_answer(state: GraphState) -> GraphState:
    llm = get_llm()
    
    context = "\n".join([doc.page_content for doc in state['documents']])
    prompt = f"""
    Based on the following context, answer the question. If the context doesn't contain relevant information, say so.
    
    Context:
    {context}
    
    Question: {state['question']}
    
    Answer:
    """
    
    response = llm.invoke(prompt)
    
    if isinstance(response, AIMessage):
        answer = response.content
    else:
        answer = str(response)
    
    return {**state, "answer": answer, "next_step": "end"}

def decide_next(state: GraphState) -> Literal["retrieve", "wiki_search", "generate_answer", "end"]:
    return state["next_step"]

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    question = request.question
    
    workflow = StateGraph(GraphState)
    
    workflow.add_node("route", RunnableLambda(route_question))
    workflow.add_node("wiki_search", RunnableLambda(wiki_search))
    workflow.add_node("retrieve", RunnableLambda(retrieve))
    workflow.add_node("generate_answer", RunnableLambda(generate_answer))
    
    workflow.add_conditional_edges(
        "route",
        RunnableLambda(decide_next),
        {
            "wiki_search": "wiki_search",
            "retrieve": "retrieve"
        }
    )
    workflow.add_conditional_edges(
        "wiki_search",
        RunnableLambda(decide_next),
        {
            "generate_answer": "generate_answer"
        }
    )
    workflow.add_conditional_edges(
        "retrieve",
        RunnableLambda(decide_next),
        {
            "generate_answer": "generate_answer"
        }
    )
    workflow.add_conditional_edges(
        "generate_answer",
        RunnableLambda(decide_next),
        {
            "end": END
        }
    )
    
    workflow.set_entry_point("route")
    
    app = workflow.compile()
    
    initial_state = {
        "question": question,
        "documents": [],
        "answer": "",
        "next_step": "route"
    }
    
    result = app.invoke(initial_state)
    
    answer = result['answer']
    sources = [doc.metadata.get("source", "Unknown") for doc in result['documents']]
    
    return AnswerResponse(answer=answer, sources=sources)