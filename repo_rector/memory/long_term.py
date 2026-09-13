import os
import sqlite3
import json
try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

class LongTermMemory:
    """Persistent knowledge store using SQLite (structured) and ChromaDB (vector)."""
    
    def __init__(self, db_path: str = "memory.db", chroma_path: str = "./chroma_db"):
        self.db_path = db_path
        self._init_sqlite()
        
        if CHROMA_AVAILABLE:
            self.chroma_client = chromadb.PersistentClient(path=chroma_path)
            self.collection = self.chroma_client.get_or_create_collection(name="codebase_knowledge")
        else:
            self.chroma_client = None
            self.collection = None
            
    def _init_sqlite(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def set_preference(self, key: str, value: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
        
    def get_preference(self, key: str, default: str = "") -> str:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else default
        
    def add_knowledge(self, document_id: str, text: str, metadata: dict = None):
        if not self.collection:
            return
            
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[document_id]
        )
        
    def search_knowledge(self, query: str, n_results: int = 3) -> list:
        if not self.collection:
            return []
            
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results.get('documents', [[]])[0]
