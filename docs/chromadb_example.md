# ChromaDB Vector Store Example

1. Run ChromaDB docker image

```bash
git clone git@github.com:chroma-core/chroma.git
cd chroma
```

> Important: If using chroma with clickhouse, which you probably are unless it's after 7/10/23, make sure to do this: [Github Issue](https://github.com/chroma-core/chroma/issues/687#issuecomment-1620506878)

Run the container

```bash
docker-compose up --build -d
```



3. Get your mongo uri, and save the following example langchain template to `chromadbvector_chain.json`.

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
        "type": "ChromaDB",
        "host": "localhost",
        "port": "8000"
      }

    }
  }
}

```

4. Seed your database:

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

client_settings = chromadb.Settings(chroma_api_impl="rest", chroma_server_host="localhost", chroma_server_http_port="8000")
embeddings = OpenAIEmbeddings()
db = Chroma(client_settings=client_settings, embedding_function=embeddings)

docsearch.add_documents(docs)

```

Make sure similarity search is working with

```py
# perform a similarity search between the embedding of the query and the embeddings of the documents
query = "What did the president say about Ketanji Brown Jackson"
docsearch.similarity_search(query, k=10)
```

5. Run the chain

```py
from langchain_interpreter import chain_from_file

chain = chain_from_file("chromadb_chain.json")
chain.run("What did the president say about Ketanji Brown Jackson")
```
