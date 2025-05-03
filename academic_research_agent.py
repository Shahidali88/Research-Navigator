import os
import tempfile
import requests
import arxiv
import streamlit as st
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
  
# Load environment variables
load_dotenv()
  
  # --- Streamlit Configuration ---
st.set_page_config(
      page_title="🔬 Research Navigator",
      layout="wide",
  )
  
  # --- Sidebar Configuration ---
st.sidebar.header("⚙️ Configuration")
  
topic = st.sidebar.text_input(
      "Research Topic",
      placeholder="e.g., agentic AI",
      help="Enter keywords to search on arXiv"
  )
  
max_papers = st.sidebar.slider(
      "Max # of Papers", 1, 20, 5,
      help="Maximum number of papers to retrieve"
  )
  
days_back = st.sidebar.slider(
      "Published in Last (Days)", 1, 365, 180,
      help="Include only papers published within this timeframe"
  )
  
st.sidebar.markdown("---")
  
  # Optional PDF toggle is removed as per update
  # Please deploy on Streamlit Cloud; QA functionality omitted for simplicity
  
    # --- Header ---
st.title("🔬 Research Navigator")
st.write(
      "Use this tool to quickly discover and preview recent arXiv papers on your chosen topic."
  )
st.markdown("---")
  
  # --- Search Button ---
if st.sidebar.button("🔍 Fetch Papers"):
      if not topic.strip():
          st.sidebar.warning("Please enter a research topic.")
      else:
          cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
          with st.spinner("Searching arXiv..."):
              search = arxiv.Search(
                  query=topic,
                  max_results=max_papers,
                  sort_by=arxiv.SortCriterion.Relevance
              )
              papers = []
              for result in search.results():
                  pub = result.published.replace(tzinfo=timezone.utc)
                  if pub < cutoff:
                      continue
                  papers.append({
                      "title": result.title,
                      "authors": ", ".join(a.name for a in result.authors),
                      "published": pub.strftime("%Y-%m-%d"),
                      "categories": ", ".join(result.categories),
                      "summary": result.summary,
                      "pdf_url": result.pdf_url
                  })
          st.session_state["papers"] = papers
  
  # --- Display Results ---
if "papers" in st.session_state and st.session_state["papers"]:
      papers = st.session_state["papers"]
      st.subheader(f"📄 Found {len(papers)} Papers for '{topic}'")
      cols = st.columns(2)
      for idx, paper in enumerate(papers):
          with cols[idx % 2]:
              st.markdown(f"**{idx+1}. {paper['title']}**")
              st.caption(
                  f"Authors: {paper['authors']}  |  Published: {paper['published']}  |  Categories: {paper['categories']}"
              )
              st.markdown(f"[📄 Download PDF]({paper['pdf_url']})")
              st.write(paper['summary'][:200] + "...")
              st.markdown("---")
  
  # --- Footer ---
st.markdown("---")
st.markdown(
      "<div style='text-align:center; color:gray;'>Developed with LangChain & Streamlit</div>",
      unsafe_allow_html=True
  )
