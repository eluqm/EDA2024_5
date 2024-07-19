# playlist_manager/util/memory_manager.py
class MemoryManager:
    def __init__(self, max_cache_size=100):
        self.cache = {}
        self.max_cache_size = max_cache_size

    def add_to_cache(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.max_cache_size:
            # Elimina el primer elemento en la caché (FIFO)
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value

    def get_from_cache(self, key):
        if key in self.cache:
            # Refrescar la posición en la caché
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None

    def clear_cache(self):
        self.cache.clear()