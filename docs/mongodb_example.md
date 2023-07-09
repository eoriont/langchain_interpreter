# MongoDB Vector Store Example

1. Setup MongoDB instance on Atlas (or wherever is convenient)

2. Download [state_of_the_union.txt](https://raw.githubusercontent.com/hwchase17/langchain/master/docs/extras/modules/state_of_the_union.txt)

3. Add the index. On the database cluster page, to to the search tab > create index, paste the following into the JSON editor:

```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "dimensions": 1536,
        "similarity": "cosine",
        "type": "knnVector"
      }
    }
  }
}
```

4. Get your mongo uri, and save the following example langchain template to `mongodbvector_chain.json`.

> Todo: Don't have password straight in the schema

```json
{
  "name": "ChromaDB Chain",
  "description": "An example chain using ChromaDB as a retriever.",
  "template_version": "0.0.7",
  "chain": {
    "type": "RetrievalQA",
    "chain_type": "stuff",
    "llm": {
      "type": "openai",
      "args": {
        "temperature": 0
      }
    },
    "retriever": {
      "type": "vectorstore",
      "vectorstore": {
        "type": "MongoDB",
        "host": "<mongo uri here>",
        "port": ""
      }

    }
  }
}

```

5. Seed your database:

```py
import os
from dotenv import load_dotenv
load_dotenv()

MONGODB_ATLAS_CLUSTER_URI = os.environ["MONGO_URI"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import TextLoader
from langchain.document_loaders import TextLoader

loader = TextLoader("state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
from pymongo import MongoClient

client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

db_name = "langchain_db"
collection_name = "langchain_col"
collection = client[db_name][collection_name]
docsearch = MongoDBAtlasVectorSearch(collection=collection, embedding=OpenAIEmbeddings())

docsearch.add_documents(docs)

```

Make sure similarity search is working with

```py
# perform a similarity search between the embedding of the query and the embeddings of the documents
query = "What did the president say about Ketanji Brown Jackson"
docsearch.similarity_search(query, k=10)
```

6. Run the chain

```py
from langchain_interpreter import chain_from_file

chain = chain_from_file("mongodbvector_chain.json")
chain.run("What did the president say about Ketanji Brown Jackson")
```
