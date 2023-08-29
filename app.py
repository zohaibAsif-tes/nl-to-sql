from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

API_KEY = 'OPENAI_API_KEY'

# setup database

db = SQLDatabase.from_uri(
    f"postgresql://postgres:postgres@localhost:5432/reachlm?sslmode=disable"
)

# setup llm
# TODO: Replace this llm with manually finetuned falcon-7b-instruct
llm = OpenAI(temperature=0, openai_api_key=API_KEY)

# create db chain
# TODO: Tweek this prompt according to the requirements 
QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""

# setup the database chain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

# TODO: Tweek this method to work with gradio 
def get_prompt():
    print("Type 'exit' to quit")
    
    while True:
        prompt = input("Enter a prompt: ")
        
        if prompt.islower() == 'exit':
            print("Exiting...")
            break
        else:
            try:
                question = QUERY.format(question=prompt)
                print(db_chain.run(question))
            except Exception as e:
                print(e)
                
                
get_prompt()

# -----------------------------------------------------------------------------------------------------------------------------

# TODO: Read these articles
# 1. https://medium.com/vectrix-ai/gpt-4-chatbot-guide-mastering-embeddings-and-personalized-knowledge-bases-f58290e81cf4
# 2. https://medium.com/vectrix-ai/creating-your-own-ai-powered-database-interface-1456b72eb36e
# extra-article: https://www.mlexpert.io/prompt-engineering/chatbot-with-local-llm-using-langchain