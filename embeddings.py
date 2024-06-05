from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Path al PDF
PATH_PDF = 'docs/Enciclopedia.pdf'

# Inicializar la función de embeddings
embedding_function = OpenAIEmbeddings()

# Cargar el PDF
loader = PyPDFLoader(PATH_PDF)
documents = loader.load_and_split()

# Usar un text splitter que sea más respetuoso con los límites lógicos del texto
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=256,  # Aumentar el tamaño de chunk para mantener más contexto
    chunk_overlap=10,  # Un pequeño solapamiento para asegurar continuidad de contexto
    length_function=len
)

#Dividir el documento en chunks más coherentes
chunks = text_splitter.split_documents(documents)

# Realizar embeddings y subirlos a una base de datos Chroma
Chroma.from_documents(
    documents=documents,
    embedding=embedding_function,
    persist_directory='docs/Chroma'
)

####################################### embedding para el segundo PDF #########################################






# # Path al PDF
# PATH_PDF = 'docs/Dietas.pdf'

# # Inicializar la función de embeddings
# embedding_function = OpenAIEmbeddings()

# # Cargar el PDF
# loader = PyPDFLoader(PATH_PDF)

# # aca lo voy a splitear porque quiero pasarle solo la info importante
# pages = loader.load_and_split()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 64,
#     chunk_overlap  = 0,
#     length_function = len,
# )


# chunks = text_splitter.split_documents(pages)
# print(f"Cantidad de chunks: {len(chunks)}")
# print()
# print(chunks[1].page_content)
# print()
# print(chunks[2].page_content)
# print()
# print(chunks[3].page_content)


# En este punto podrían elegirse reglas para definiar el criterio de los "chunks"

# Realizar embeddings y subirlos a una bd Chroma
# Chroma.from_documents(
#     documents=documents,
#     embedding=embedding_function,
#     persist_directory='docs/Chroma'
# )

