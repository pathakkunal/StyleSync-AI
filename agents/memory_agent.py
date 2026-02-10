import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai

load_dotenv()

class MemoryAgent:
    def __init__(self):
        # 1. Configure Gemini (for Embeddings)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            print("⚠️ GEMINI_API_KEY missing. Memory Agent will fail.")
            return
        genai.configure(api_key=self.gemini_api_key)
        
        # 2. Configure Pinecone (Vector DB)
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        if not self.pinecone_api_key:
            print("⚠️ PINECONE_API_KEY missing. Memory Agent will fail.")
            return
            
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index_name = "stylesync-index-v2" # Rebranded Index Name
        
        # 3. Create Index if not exists
        existing_indexes = [i.name for i in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            print(f"🧠 Creating new memory index: {self.index_name}...")
            try:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=3072, # Dimension for 'models/gemini-embedding-001'
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
                while not self.pc.describe_index(self.index_name).status['ready']:
                    time.sleep(1)
                print("✅ Index created successfully.")
            except Exception as e:
                print(f"❌ Failed to create index: {e}")
        
        self.index = self.pc.Index(self.index_name)

    def _get_embedding(self, text):
        """Generates vector embeddings using Gemini"""
        try:
            result = genai.embed_content(
                model="models/gemini-embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"❌ Embedding Error: {e}")
            return [0.0] * 3072 # Return empty vector on failure

    def retrieve_keywords(self, query_text: str, top_k=5):
        """Searches memory for relevant keywords"""
        if not hasattr(self, 'index'): return []
        
        print(f"🧠 Searching memory for: '{query_text}'...")
        embedding = self._get_embedding(query_text)
        
        try:
            results = self.index.query(
                vector=embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Extract unique keywords
            keywords = []
            for match in results.matches:
                if match.score > 0.5: # Relevance threshold
                    kw_str = match.metadata.get('keywords', '')
                    keywords.extend([k.strip() for k in kw_str.split(',')])
            
            return list(set(keywords))[:10] # Return top 10 unique
        except Exception as e:
            print(f"❌ Search Error: {e}")
            return []
