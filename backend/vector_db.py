import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

def create_db(subject, storage_path):
    documents = SimpleDirectoryReader(subject).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=storage_path)
    return index

def load_db(storage_path):
    storage_context = StorageContext.from_defaults(persist_dir=storage_path)
    index = load_index_from_storage(storage_context)
    return index

