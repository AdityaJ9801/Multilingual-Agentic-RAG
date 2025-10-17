"""
Streamlit Frontend for Multilingual Agentic RAG System
"""
import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional
import time

# Page configuration
st.set_page_config(
    page_title="Multilingual RAG System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1rem;
        padding: 0.5rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"
if "api_key" not in st.session_state:
    st.session_state.api_key = "your-api-key"
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.session_state.api_url = st.text_input(
        "API URL",
        value=st.session_state.api_url,
        help="FastAPI backend URL"
    )
    
    st.session_state.api_key = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        help="API authentication key"
    )
    
    st.divider()
    
    # System status
    st.subheader("📊 System Status")
    if st.button("🔄 Check Health", use_container_width=True):
        try:
            response = requests.get(
                f"{st.session_state.api_url}/api/v1/health",
                timeout=5
            )
            if response.status_code == 200:
                health = response.json()
                st.success("✅ System Healthy")
                st.json(health)
            else:
                st.error("❌ System Unhealthy")
        except Exception as e:
            st.error(f"❌ Connection Error: {str(e)}")
    
    st.divider()
    
    # Query history
    st.subheader("📜 Query History")
    if st.button("Clear History", use_container_width=True):
        st.session_state.query_history = []
        st.rerun()
    
    if st.session_state.query_history:
        for i, query in enumerate(st.session_state.query_history[-5:], 1):
            st.caption(f"{i}. {query[:50]}...")

# Main content
st.title("🌍 Multilingual Agentic RAG System")
st.markdown("*Retrieve, Augment, and Generate responses in multiple languages*")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍 Query", "📤 Document Upload", "📚 Documents", "📊 Analytics"]
)

# ============================================================================
# TAB 1: QUERY
# ============================================================================
with tab1:
    st.header("Query the RAG System")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query_text = st.text_area(
            "Enter your query:",
            placeholder="Ask a question in any language...",
            height=100,
            key="query_input"
        )
    
    with col2:
        st.markdown("**Language**")
        language = st.selectbox(
            "Select language (optional):",
            ["Auto-detect", "English", "Spanish", "French", "Chinese", "Arabic"],
            label_visibility="collapsed"
        )
        
        language_map = {
            "Auto-detect": None,
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "Chinese": "zh",
            "Arabic": "ar"
        }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_k = st.slider("Top K documents:", 1, 20, 5)
    
    with col2:
        include_sources = st.checkbox("Include sources", value=True)
    
    with col3:
        include_reasoning = st.checkbox("Include reasoning", value=False)
    
    if st.button("🚀 Submit Query", use_container_width=True, type="primary"):
        if not query_text.strip():
            st.error("Please enter a query")
        else:
            with st.spinner("Processing query..."):
                try:
                    payload = {
                        "query": query_text,
                        "language": language_map[language],
                        "top_k": top_k,
                        "include_sources": include_sources,
                        "include_reasoning": include_reasoning
                    }
                    
                    response = requests.post(
                        f"{st.session_state.api_url}/api/v1/query",
                        json=payload,
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Add to history
                        st.session_state.query_history.append(query_text)
                        
                        # Display results
                        st.markdown("### 📝 Response")
                        st.markdown(result["response"])
                        
                        # Metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Language", result["language"].upper())
                        with col2:
                            st.metric("Confidence", f"{result['confidence']:.2%}")
                        with col3:
                            st.metric("Processing Time", f"{result['processing_time_ms']:.0f}ms")
                        with col4:
                            st.metric("Sources", len(result.get("sources", [])))
                        
                        # Sources
                        if include_sources and result.get("sources"):
                            st.markdown("### 📚 Sources")
                            for i, source in enumerate(result["sources"], 1):
                                with st.expander(f"Source {i}: {source.get('source', 'Unknown')[:50]}"):
                                    st.write(source)
                        
                        # Reasoning
                        if include_reasoning and result.get("reasoning"):
                            with st.expander("🧠 Agent Reasoning"):
                                st.code(result["reasoning"], language="json")
                        
                        # Agent states
                        if result.get("agent_states"):
                            with st.expander("🤖 Agent States"):
                                st.json(result["agent_states"])
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timeout. The query took too long to process.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============================================================================
# TAB 2: DOCUMENT UPLOAD
# ============================================================================
with tab2:
    st.header("Upload Documents")
    st.markdown("Upload documents to build your knowledge base. Supported formats: PDF, TXT, MD, JSON, CSV")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "md", "json", "csv"],
        help="Select a document to ingest"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"📄 File: {uploaded_file.name}")
            st.info(f"📊 Size: {uploaded_file.size / 1024:.2f} KB")
        
        if st.button("📤 Upload Document", use_container_width=True, type="primary"):
            with st.spinner("Uploading and processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getbuffer())}
                    
                    response = requests.post(
                        f"{st.session_state.api_url}/api/v1/ingest",
                        files=files,
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Document uploaded successfully!")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Document ID", result["document_id"][:8])
                        with col2:
                            st.metric("Chunks Created", result["chunks_created"])
                        with col3:
                            st.metric("Language", result["language"].upper())
                        with col4:
                            st.metric("Status", result["status"])
                        
                        st.info(result["message"])
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============================================================================
# TAB 3: DOCUMENTS
# ============================================================================
with tab3:
    st.header("Ingested Documents")
    
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    try:
        response = requests.get(
            f"{st.session_state.api_url}/api/v1/documents",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            st.metric("Total Documents", data["total_count"])
            
            if data["documents"]:
                st.dataframe(
                    [
                        {
                            "File Name": doc["file_name"],
                            "Type": doc["file_type"],
                            "Language": doc["language"],
                            "Chunks": doc["chunks_count"],
                            "Size (KB)": doc["file_size_bytes"] / 1024,
                            "Ingested": doc["ingestion_date"]
                        }
                        for doc in data["documents"]
                    ],
                    use_container_width=True
                )
            else:
                st.info("No documents ingested yet. Upload documents in the 'Document Upload' tab.")
        else:
            st.error(f"Error: {response.status_code}")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ============================================================================
# TAB 4: ANALYTICS
# ============================================================================
with tab4:
    st.header("System Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Query Statistics")
        if st.session_state.query_history:
            st.metric("Total Queries", len(st.session_state.query_history))
            st.write("Recent queries:")
            for query in st.session_state.query_history[-10:]:
                st.caption(f"• {query[:70]}...")
        else:
            st.info("No queries yet")
    
    with col2:
        st.subheader("🤖 Agent Information")
        if st.button("Get Agent Status", use_container_width=True):
            try:
                response = requests.get(
                    f"{st.session_state.api_url}/api/v1/agents/status",
                    timeout=10
                )
                if response.status_code == 200:
                    agents = response.json()
                    st.json(agents)
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
    🌍 Multilingual Agentic RAG System | Powered by FastAPI, Ollama, and Qdrant
    </div>
""", unsafe_allow_html=True)

