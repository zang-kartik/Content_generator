import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index import StorageContext
from llama_index import SimpleDirectoryReader, VectorStoreIndex
import openai
from dotenv import load_dotenv
import os
from chromadb.utils import embedding_functions


def createUserIndex(modalId,openkey):
    """
    Creates Chroma Vector Database Index

    Parameter:
    - modalId (str) : a unique to create collection in Vector DB
    
    Returns:
    - string
    """
    load_dotenv(".env")
    try:
        openai.api_key = openkey#Import your OpenAI key to set Embeddings for storing

        openai_embedding = embedding_functions.OpenAIEmbeddingFunction(model_name = "text-embedding-ada-002")


        chroma_client = chromadb.PersistentClient() #Creating a Persistent Chroma Client
        chroma_collection = chroma_client.create_collection(modalId,embedding_function=openai_embedding) #Naming the Collection 
        vec_store = ChromaVectorStore(chroma_collection=chroma_collection) #Creating Vector object for that collection   
        stcontext = StorageContext.from_defaults(vector_store=vec_store) #Defining Storage context

        path = "/home/ubuntu/package-chatbot/Data"#os.getenv("DOC_PATH") #Path where the document is Stored
        # path = os.path.join(path,modalId)
        document  = SimpleDirectoryReader(path).load_data() #Loading document data

        index = VectorStoreIndex.from_documents(documents=document,storage_context=stcontext) #Creating vector index
        path2 ="/home/ubuntu/package-chatbot/Vector_DB"# os.getenv("VECTOR_DB_PATH") #Path to store index or Persistent DIR
        print("path is ,",os.getenv("VECTOR_DB_PATH"))
        index._storage_context.persist(path2)

        files = os.listdir(path)

        for file in files:
            file_path = os.path.join(path,file)

            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)

            except Exception as e:
                return str(e)
            
    except Exception as e:
        return str(e)
    

    return "success"



