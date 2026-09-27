import threading

try:
    from sentence_transformers import SentenceTransformer
    ST_AVAILABLE = True
except ImportError:
    ST_AVAILABLE = False
    SentenceTransformer = None

class EmbeddingService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, model_name: str = 'all-MiniLM-L6-v2'):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EmbeddingService, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        if self._initialized:
            return
        self.model_name = model_name
        self.model = None
        self._initialized = True

    def _load_model(self):
        if self.model is None and ST_AVAILABLE:
            try:
                self.model = SentenceTransformer(self.model_name)
            except Exception:
                pass

    def generate_embedding(self, text: str) -> list[float]:
        if not text:
            return [0.0] * 384
            
        self._load_model()
        
        if self.model:
            try:
                embedding = self.model.encode(text)
                return embedding.tolist()
            except Exception:
                pass
                
        # Fallback if sentence-transformers unavailable or fails
        return self._generate_fallback_embedding(text)

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
            
        self._load_model()
        
        if self.model:
            try:
                embeddings = self.model.encode(texts)
                return embeddings.tolist()
            except Exception:
                pass
                
        return [self._generate_fallback_embedding(t) for t in texts]
        
    def _generate_fallback_embedding(self, text: str) -> list[float]:
        # Pseudo-embedding fallback: hash based trick just to return a 384d vector
        vec = [0.0] * 384
        for i, char in enumerate(text[:384]):
            vec[i % 384] += ord(char) / 255.0
        # Normalize
        norm = sum(v*v for v in vec) ** 0.5
        if norm > 0:
            vec = [v/norm for v in vec]
        return vec
