# defino las liberías que voy a utilizar
from openai import OpenAI 
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories import ChatMessageHistory
import inventario
import prompt_template
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory, ChatMessageHistory
import servicioserver
import requests
from langchain_community.tools import YouTubeSearchTool
# Cargo variables de entorno
load_dotenv()
dotenv_path = "./BotEntrenadorPersonal_v1/.env"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  


embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# Creo el modelo
llm = ChatOpenAI(
    model='gpt-3.5-turbo',
    temperature=0.2,
    api_key=OPENAI_API_KEY
)

# Configuración de la base de datos Chroma
db = Chroma(
    persist_directory='docs/Chroma',
    embedding_function=embedding_function
)
retriever = db.as_retriever()

# Configuración de memoria para el chat
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=4,
    return_messages=True,
    chat_memory=ChatMessageHistory()
)


# creo mis tools
normas_tool = create_retriever_tool(
    retriever=retriever,
    name="normas",
    description="Busca y devuelve las normas del gimnasio."
)

ejercicios_tool = create_retriever_tool(
    retriever=retriever,
    name="Ejercicios",
    description="Busca y analiza y devuelve ejercicios puntuales con una explicacion de como hacerlos y que maquina usar dependiendo del inventario del GYM y basados en Enciclopedia.pdf ."
)

nutricion_tool = create_retriever_tool(
    retriever=retriever,
    name="Nutricion",
    description="Busca y devuelve la dieta correcta en base a su tipo de nutricion."
)
youtube_tool  = YouTubeSearchTool()

tools = [normas_tool, ejercicios_tool,nutricion_tool,youtube_tool]



# aca defino la funcion para obtener el response de la API
def get_user_data():
    
    url = 'http://localhost:5000/verificar'  
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  
    else:
        raise Exception("No se pudo obtener la data")

#aca lo parseo para quedarme con las variables que necesito
def setup_user_profile():

    user_data = get_user_data() 
    
    nombre = user_data.get('nombre', 'desconocido')  
    estatura = user_data.get('altura', 'desconocido')  
    peso = user_data.get('peso', 'desconocido')  
    genero = user_data.get('genero', 'desconocido') 
    nutricion = user_data.get('tipoDieta', 'desconocido')  
    return nutricion,genero,peso,estatura,nombre

#aca invoco la funcion

nutricion,genero,peso,estatura,nombre=setup_user_profile()


# nombre = "Ligimat"
# estatura = "159"  # en cm
# peso = "63"  # en kg
# genero = "Femenino"
# nutricion = "celiaco"
lista_inventario =   inventario.inventario_df



# Invocar la función run_bot con los datos de ejemplo
#prompt = promptTemplateTest.create_prompt(nombre, estatura, peso, genero, lista_inventario,nutricion)

prompt=prompt_template.CrearTemplate(nombre, estatura, peso, genero, lista_inventario,nutricion)



agent = create_openai_tools_agent(
    llm=llm, 
    tools=tools, 
    prompt=prompt
)



agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools,
    verbose=True,
    memory=memory
)

# Función para utilizar el agente
def bot(query: str, chat_history):
    # Obtiene el input del usuario junto con el historial del chat
    response = agent_executor.invoke({'input': query, "chat_history": chat_history})['output']
    return response

