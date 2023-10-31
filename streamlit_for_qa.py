import os
import langchain
import streamlit as st
from langchain.graphs import Neo4jGraph
from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from langchain.memory import ConversationBufferMemory

os.environ["OPENAI_API_KEY"] = "" ##INTRODUCE YOUR KEY HERE

def main():
    #Get the qeustion from the user
    st.title("Ask questions about the History of Portugal")
    prompt = st.text_input("Ask a question:") #This is where the user will write their question

    #Get the graph already saved in neo4j
    url = "neo4j+s://4bbe0240.databases.neo4j.io"
    username ="neo4j"
    password = "DC7rTr-Pnqa_u7idmZavGqsKUZGSb3akeEJ2BsJCk5w"

    graph = Neo4jGraph(
        url=url,
        username=username,
        password=password)

    graph.refresh_schema()

    #Define chain
    memory = ConversationBufferMemory()#memory_key="chat_history")

    chain = GraphCypherQAChain.from_llm(
        graph=graph,
        cypher_llm=ChatOpenAI(temperature=0.9, model="gpt-4"),
        qa_llm=ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo"),
        validate_cypher=True, # Validate relationship directions
        verbose=True,
        memory=memory, #conversation with memory
    )

    #Answer the question
    response = chain.run(prompt)
    st.write(response)


if __name__ == "__main__":
    main()