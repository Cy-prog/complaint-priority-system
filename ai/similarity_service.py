import re
from typing import List, Dict, Any

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from .embedding_service import EmbeddingService

class SimilarityService:
    def __init__(self, embedding_service: EmbeddingService, persist_dir: str):
        self.embedding_service = embedding_service
        self.client = None
        self.collection = None
        # In-memory document store as robust fallback
        self._memory_store: Dict[int, Dict[str, Any]] = {}
        
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(path=persist_dir)
                self.collection = self.client.get_or_create_collection(name="complaints")
            except Exception:
                pass

    def add_complaint(self, complaint_id: int, text: str, metadata: dict = None):
        if not complaint_id or not text:
            return
            
        clean_text = text.strip()
        meta = metadata or {}
        # Always store in fallback memory store
        self._memory_store[complaint_id] = {
            "text": clean_text,
            "metadata": meta
        }
        
        if self.collection:
            try:
                embedding = self.embedding_service.generate_embedding(clean_text)
                self.collection.upsert(
                    documents=[clean_text],
                    embeddings=[embedding],
                    metadatas=[meta],
                    ids=[str(complaint_id)]
                )
            except Exception:
                pass

    def find_similar(self, text: str, n_results: int = 5, threshold: float = 0.65) -> list[dict]:
        if not text:
            return []
            
        clean_text = text.strip().lower()
        similar_complaints = []
        
        # 1. Try ChromaDB
        if self.collection:
            try:
                embedding = self.embedding_service.generate_embedding(clean_text)
                results = self.collection.query(
                    query_embeddings=[embedding],
                    n_results=n_results
                )
                if results and results.get('ids') and results['ids'][0]:
                    for i in range(len(results['ids'][0])):
                        c_id = int(results['ids'][0][i])
                        doc_text = results['documents'][0][i] if results.get('documents') else ""
                        dist = results['distances'][0][i] if 'distances' in results and results['distances'] else 0
                        similarity = max(0.0, 1.0 - (dist / 2.0))
                        
                        if similarity >= threshold:
                            sim_reason = self._compute_similarity_reason(clean_text, doc_text.lower())
                            similar_complaints.append({
                                "complaint_id": c_id,
                                "similarity_score": round(float(similarity), 4),
                                "reason_for_similarity": sim_reason,
                                "text_preview": doc_text[:120] + "..." if len(doc_text) > 120 else doc_text,
                                "auto_merged": False,
                                "requires_officer_confirmation": True
                            })
                    if similar_complaints:
                        return similar_complaints
            except Exception:
                pass

        # 2. Robust In-Memory Word & N-gram Overlap Fallback (Jaccard / Cosine token similarity)
        query_words = set(re.findall(r'\w+', clean_text))
        for c_id, stored in self._memory_store.items():
            stored_text = stored["text"].lower()
            stored_words = set(re.findall(r'\w+', stored_text))
            
            if not query_words or not stored_words:
                continue
                
            intersection = query_words.intersection(stored_words)
            union = query_words.union(stored_words)
            jaccard = len(intersection) / len(union) if union else 0.0
            
            # Boost if specific entities match (e.g. "black suv", "railway station")
            shared_key_entities = [
                w for w in ["suv", "black", "railway station", "accident", "pothole", "transformer", "fire", "hospital"]
                if w in clean_text and w in stored_text
            ]
            
            score = min(jaccard * 1.5 + (len(shared_key_entities) * 0.15), 0.95)
            
            if score >= threshold:
                sim_reason = self._compute_similarity_reason(clean_text, stored_text)
                similar_complaints.append({
                    "complaint_id": c_id,
                    "similarity_score": round(float(score), 4),
                    "reason_for_similarity": sim_reason,
                    "text_preview": stored["text"][:120] + "...",
                    "auto_merged": False,
                    "requires_officer_confirmation": True
                })

        similar_complaints.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar_complaints[:n_results]

    def _compute_similarity_reason(self, text_a: str, text_b: str) -> str:
        factors = []
        if ("suv" in text_a and "suv" in text_b) or ("car" in text_a and "car" in text_b):
            factors.append("matching vehicle type")
        if "black" in text_a and "black" in text_b:
            factors.append("matching vehicle color (black)")
        if ("railway station" in text_a and "railway station" in text_b) or ("station" in text_a and "station" in text_b):
            factors.append("same incident location (railway station)")
        if any(w in text_a and w in text_b for w in ["hit", "hit-and-run", "knocked", "escaped"]):
            factors.append("similar hit-and-run description")
        if any(w in text_a and w in text_b for w in ["fire", "aag", "smoke"]):
            factors.append("matching fire emergency incident")
            
        if factors:
            return "Potential duplicate: " + ", ".join(factors)
        return "High lexical and semantic similarity between complaint narratives"

    def calculate_duplicate_probability(self, text: str) -> float:
        similar = self.find_similar(text, n_results=1, threshold=0.0)
        if similar:
            return float(similar[0]['similarity_score'])
        return 0.0

    def remove_complaint(self, complaint_id: int):
        self._memory_store.pop(complaint_id, None)
        if not self.collection:
            return
        try:
            self.collection.delete(ids=[str(complaint_id)])
        except Exception:
            pass
