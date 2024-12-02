NUM_DOCUMENTS = 7
MAX_CONTEXT_DOCS = 2

import sys
sys.stdout.reconfigure(encoding='utf-8')
from openai import OpenAI
openai_client = OpenAI(api_key=open(".key.txt", "r").read())

import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="rag_documents")
collection.upsert(ids = [f"doc{i}" for i in range(NUM_DOCUMENTS)], 
               documents = [open(f"data/{i}.txt", "r", encoding = "utf-8").read() for i in range(NUM_DOCUMENTS)])

def matchDocuments(question):
    response = collection.query(query_texts=[question], n_results=MAX_CONTEXT_DOCS)["documents"][0]
    # print([str(doc.encode("utf-8"), "utf-8")[:128] for doc in response])
    return response
def getPrompt(docs, question, withContext = True):
    if withContext:
        prompt = [{"role":"system", "content": "Given the following documents, you will answer users' questions as accurately as possible.\n\n" + '\n\n\n'.join(docs)},
              {"role":"user", "content": question}]
    elif not withContext:
        prompt = [{"role":"user", "content":question}]
    print(prompt)
    return prompt

def askQuestion(question, withContext = True):
    context = matchDocuments(question)
    prompt = getPrompt(context, question, withContext)
    response = openai_client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = prompt
    )
    print("\n\nAnswer: " + response.choices[0].message.content)

question = "Who is Weather Report?"
askQuestion(question)
print("\n\nUninformed:")
askQuestion(question, withContext=False)
