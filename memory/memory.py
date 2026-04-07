memory_store = []

def save_memory(data):
    memory_store.append(data)

def get_recent_context(n=3):
    return memory_store[-n:]
