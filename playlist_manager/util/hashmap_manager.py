# playlist_manager/util/hashmap_manager.py

class HashMap:
    def __init__(self, size=1000):
        self.size = size
        self.count = 0
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def _resize(self):
        new_size = self.size * 2
        new_table = [[] for _ in range(new_size)]
        for bucket in self.table:
            for k, v in bucket:
                new_hash = hash(k) % new_size
                new_table[new_hash].append((k, v))
        self.size = new_size
        self.table = new_table

    def insert(self, key, value):
        if self.count / self.size > 0.7:
            self._resize()
        hash_key = self._hash(key)
        bucket = self.table[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1

    def get(self, key):
        hash_key = self._hash(key)
        bucket = self.table[hash_key]
        for k, v in bucket:
            if key == k:
                return v
        return None

    def delete(self, key):
        hash_key = self._hash(key)
        bucket = self.table[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                del bucket[i]
                self.count -= 1
                return

    def get_all_keys(self):
        keys = []
        for bucket in self.table:
            for k, v in bucket:
                keys.append(k)
        return keys
