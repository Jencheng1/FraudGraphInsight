import streamlit as st
import os
from dotenv import load_dotenv
import boto3
from app import FraudGraphRAG
import json

# Load environment variables
load_dotenv()

# Initialize Bedrock client for Guardrails
bedrock_client = boto3.client(
    'bedrock',
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Initialize RAG system
@st.cache_resource
def get_rag_system():
    return FraudGraphRAG()

# Function to check content with Bedrock Guardrails
def check_content_with_guardrails(content):
    try:
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                "prompt": f"Analyze this content for harmful, unethical, or sensitive information: {content}",
                "max_tokens_to_sample": 100,
                "temperature": 0.1,
                "top_p": 0.9,
            })
        )
        return json.loads(response.get('body').read())
    except Exception as e:
        st.error(f"Error checking content with Guardrails: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(
    page_title="FraudGraphInsight",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 FraudGraphInsight")
st.markdown("""
    This AI-powered system helps analyze fraud patterns using RAG (Retrieval-Augmented Generation) with AWS Bedrock.
    It combines vector search and graph analysis to provide comprehensive fraud detection insights.
""")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    max_results = st.slider(
        "Maximum Results",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about fraud patterns..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get RAG system
    rag = get_rag_system()

    # Process query
    with st.chat_message("assistant"):
        with st.spinner("Analyzing fraud patterns..."):
            try:
                # Get response from RAG system
                response = rag.query(prompt)
                
                # Check response with Guardrails
                guardrail_check = check_content_with_guardrails(response["answer"])
                
                if guardrail_check and "flagged" in guardrail_check and guardrail_check["flagged"]:
                    st.warning("⚠️ Content flagged by Guardrails. Response may be modified.")
                    # Modify response based on Guardrails feedback
                    response["answer"] = "I apologize, but I cannot provide that information as it may contain sensitive or harmful content."
                
                # Display response
                st.markdown(response["answer"])
                
                # Display sources if available
                if "sources" in response and response["sources"]:
                    with st.expander("View Sources"):
                        for source in response["sources"]:
                            st.markdown(f"- {source}")
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"]
                })
                
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")

# Add footer with Guardrails information
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Powered by AWS Bedrock with Guardrails for responsible AI</p>
        <small>This system uses content filtering to prevent harmful or unethical responses</small>
    </div>
""", unsafe_allow_html=True) 