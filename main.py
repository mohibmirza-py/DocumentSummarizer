import os
from typing import List, Dict, Literal
from dotenv import load_dotenv
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Literal
from PyPDF2 import PdfReader
from docx import Document
import zipfile
import tempfile
load_dotenv()


class DocumentAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = None
        self.qa_chain = None

    def extract_text_from_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            return "\n".join(page.extract_text() for page in pdf.pages)

    def extract_text_from_docx(self, file_path):
        try:
            doc = Document(file_path)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        except:
            # If python-docx fails, try a more basic approach
            with zipfile.ZipFile(file_path) as zf:
                content = zf.read('word/document.xml').decode('utf-8')
                return content

    def ingest_document(self, file_path: str, file_type: Literal["pdf", "docx"]):
        # Extract text based on file type
        if file_type == "pdf":
            text = self.extract_text_from_pdf(file_path)
        else:
            text = self.extract_text_from_docx(file_path)

        # Split the text
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(text)

        # Create vector store
        self.vector_store = FAISS.from_texts(texts, self.embeddings)
        print("Doc ingested")

        # Initialize QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4o"),
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )

    def summarize(self, query: str) -> str:
        if not self.qa_chain:
            raise ValueError("No document has been ingested yet.")
        return self.qa_chain.invoke({"query": query})

    def take_notes(self, topics: List[str]) -> Dict[str, str]:
        if not self.qa_chain:
            raise ValueError("No document has been ingested yet.")
        notes = {}
        for topic in topics:
            notes[topic] = self.qa_chain.invoke({"query": f"Provide key points about {topic} from the document."})
        return notes

# Streamlit app
def main():
    st.title("Zahra's Document Analysis App")


    st.markdown("""
    - 📤 **Upload** a PDF or Word document
    - 🔑 Enter **key topics** you want to explore
    - 🔍 Click "**Analyze Document**" to process
    - 📚 Get a **summary**, **key points**, and **topic notes**
    - 🧠 Use for **quick study** and **research aid**
    - 🤖 Powered by AI for **smart analysis**
    - 🎓 Perfect for **students** to grasp main ideas quickly
    """)

    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=["docx", "pdf"])

    if uploaded_file is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # Initialize DocumentAgent
            agent = DocumentAgent()
            file_type = "pdf" if uploaded_file.type == "application/pdf" else "docx"
            agent.ingest_document(file_path=tmp_file_path, file_type=file_type)

            # Get topics from user
            topics_input = st.text_area("Enter topics for key notes (one per line):")
            topics = [topic.strip() for topic in topics_input.split("\n") if topic.strip()]

            if st.button("Analyze Document", type="primary", use_container_width=True):
                # Summarize
                with st.spinner("Generating summary..."):
                    summary = agent.summarize("Summarize the main points of the document. Also give a list of key points. Explain it in a way that a 5 year old can understand.")
                st.subheader("Summary")
                st.write(summary["result"])

                # Take notes on topics
                if topics:
                    with st.spinner("Generating notes on topics..."):
                        notes = agent.take_notes(topics)
                    st.subheader("Notes on Topics")
                    for topic, note in notes.items():
                        st.write(f"**{topic}:**")
                        st.write(note["result"])
                        st.write("---")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)

if __name__ == "__main__":
    main()
