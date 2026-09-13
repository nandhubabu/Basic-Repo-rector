from typing import List, Dict, Any

class ShortTermMemory:
    """Manages the short-term conversation/interaction window."""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.history: List[Dict[str, Any]] = []
        
    def add_interaction(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        
        # Keep only the last N items (sliding window)
        if len(self.history) > self.window_size:
            self.history.pop(0)
            
    def get_context_string(self) -> str:
        """Returns the recent history formatted as a context string."""
        context = ""
        for entry in self.history:
            context += f"{entry['role'].upper()}: {entry['content']}\n"
        return context
        
    def clear(self):
        self.history.clear()
