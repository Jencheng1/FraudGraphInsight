import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.llms import Bedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import Tool

# Load environment variables
load_dotenv()

class FraudGraphInsight:
    def __init__(self):
        # Initialize Bedrock LLM
        self.llm = Bedrock(
            model_id="anthropic.claude-v2",
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        
        # Initialize Bedrock Embeddings
        self.embeddings = BedrockEmbeddings(
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        
        # Initialize OpenSearch Vector Store
        self.vector_store = OpenSearchVectorSearch(
            opensearch_url=os.getenv("OPENSEARCH_URL"),
            index_name="fraud_embeddings",
            embedding_function=self.embeddings,
            http_auth=(os.getenv("OPENSEARCH_USER"), os.getenv("OPENSEARCH_PASSWORD"))
        )
        
        # Initialize Neo4j Graph
        self.graph = Neo4jGraph(
            url=os.getenv("NEO4J_URI"),
            username=os.getenv("NEO4J_USER"),
            password=os.getenv("NEO4J_PASSWORD")
        )
        
        # Create retriever
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )
        
        # Create tools for the agent
        self.tools = [
            Tool(
                name="vector_search",
                func=self.retriever.get_relevant_documents,
                description="Search for relevant fraud patterns in vector database"
            ),
            Tool(
                name="graph_query",
                func=self.graph.query,
                description="Query the fraud relationship graph"
            )
        ]
        
        # Create agent
        self.agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            system_message="You are a fraud detection expert. Use the available tools to analyze fraud patterns and relationships."
        )
        
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a user query about fraud patterns"""
        try:
            response = self.agent_executor.invoke({"input": question})
            return {
                "answer": response["output"],
                "sources": response.get("intermediate_steps", [])
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    insight = FraudGraphInsight()
    result = insight.query("Find suspicious transaction patterns related to account 12345")
    print(result) 