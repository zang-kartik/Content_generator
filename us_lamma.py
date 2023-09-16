from llama_index import load_index_from_storage, StorageContext,VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore,PineconeVectorStore
import openai
import os
from dotenv import load_dotenv
from llama_index import Prompt
import database_utils
import chromadb
from chromadb.utils import embedding_functions

def queryAns(modalId,query):
    """
    Queries GPT model and generates response

    Parameter
    - 
    """
    # modalid INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), contentType VARCHAR(50), samplefile VARCHAR(255), guidelines VARCHAR(255), responeSize VARCHAR(50), paid BOOLEAN,openkey,description

    load_dotenv()
    try:
        openai.api_key = database_utils.getOpenAI(modalId=modalId)
        res = database_utils.getData(modalId=modalId)

        #getting params according to modalId to create prompt
        title = res[1]
        content_type = res[2]
        guidelines = res[4]
        responseSize = res[5]
        description = res[6]

        #creating prompt for the model according params
        template = (
        f"You are an {title} based AI. \n"
        "---------------------\n"
        f"You create this type of content {content_type}"
        "\n---------------------\n"
        f"You need to follow this guidelines {guidelines}\n"
        "\n---------------------\n"
        f"Your response size should be strictly in {responseSize}\n"
        "\n---------------------\n"
        f"Here is some description {description}\n"
        "\n---------------------\n"
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Using both the context information and also using your own knowledge, "
        "answer the question: {query_str}\n"
        "If the context isn't helpful, you can also answer the question on your own.\n"
        )

        openai_embedding = embedding_functions.OpenAIEmbeddingFunction(model_name = "text-embedding-ada-002")
        client = chromadb.PersistentClient()
        collection = client.get_collection(modalId,embedding_function=openai_embedding)
        
        path = "/home/ubuntu/package-chatbot/Vector_DB"#os.getenv("VECTOR_DB_PATH")
        vec_store = ChromaVectorStore(chroma_collection=collection)
        stcontext = StorageContext.from_defaults(vector_store=vec_store,persist_dir=path)
        index = load_index_from_storage(stcontext)
        qa_template = Prompt(template=template)
        query_engine = index.as_query_engine(text_qa_template=qa_template)
        res = query_engine.query(query)
        return res
    
    except Exception as e:
        return str(e)

