# Chat-with-doc
A RAG application to interact with your docs 

## Architecture Summary: Retrieval-Augmented Generation (RAG) System

The system is designed to handle user queries via a RESTful API and generate contextually relevant responses using a combination of retrieval and generation techniques. Below is a breakdown of the components:

### 1. FastAPI
- Acts as the entry point for the system.
- Handles `POST /query` requests from users.

### 2. LangChain Framework
- Manages the orchestration of the RAG pipeline.
- Includes:
  - **Prompt Template**: Defines how the query and retrieved context are formatted before being sent to the model.
  - **Retriever Logic**: Interfaces with the vector store to fetch relevant documents based on the query.

### 3. ChromaDB (Vector Store)
- Stores document embeddings.
- Performs similarity search to retrieve top-k relevant chunks for a given query.

### 4. HuggingFace Model
- Uses `distilgpt2`, a lightweight transformer-based language model.
- Generates the final response based on the prompt and retrieved context.

**Code breakdown is not included in this readme as proper commenting has been used while writing code**
