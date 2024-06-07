#from langchain.chains.sql_database.query import create_sql_query_chain
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import sqlalchemy

# Set up your database credentials
db_user = "root"
db_password = "pass123"
db_host = "localhost"
db_name = "demonstrator"

# Function to create a database URI for MySQL
def create_db_uri(user, password, host, db_name):
    return f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"

# Create an instance of SQLDatabase
try:
    db_uri = create_db_uri(db_user, db_password, db_host, db_name)
    db = SQLDatabase.from_uri(db_uri)
    print("Database connection established.")
except sqlalchemy.exc.SQLAlchemyError as e:
    print(f"Error connecting to the database: {e}")
    raise

# Create an instance of OllamaClient with your desired model
try:
    llm = ChatOpenAI(model="mistral", temperature=0,
    base_url = 'http://localhost:11434/v1',
    api_key='ollama')
#    print("Ollama client initialized.")
except Exception as e:
    print(f"Error initializing Ollama client: {e}")
    raise

# Create the SQL query chain
try:
    execute_query = QuerySQLDataBaseTool(db=db)
    chain = create_sql_query_chain(llm, db)
    chain.get_prompts()[0].pretty_print()
  #  context = db.get_context()
  #  print(context["table_info"])
  #  print("SQL query chain created.")
except Exception as e:
    print(f"Error creating SQL query chain: {e}")
    raise

# Invoke the chain with a question
try:
    #response = chain.invoke("who has the highst salary")
    response = chain.invoke({"question": "Who are the highest-paid employees in each department?"})
    print(f"Response: {response}")
except Exception as e:
    print(f"Error invoking chain: {e}")
    raise
