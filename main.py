from flask import Flask, request, jsonify
import os
import json
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load the GROQ and Google API Keys
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Define Prompt Template
prompt = ChatPromptTemplate.from_template("""
You are a highly skilled mathematical analyst. You are tasked to perform detailed calculations and analysis based on the provided context.
Use advanced reasoning and precise computation techniques to derive the most accurate answers. Be concise and clear.

<context>
{context}
<context>
Question: {input}
Answer:
""")

# Global state for storing embeddings and vector database
embeddings = None
vectors = None

# Function to embed JSON data
def vector_embedding(json_file):
    global embeddings, vectors
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Load JSON file and prepare records as chunks
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file format.")

    if not isinstance(data, list):
        raise ValueError("JSON data must be a list of records.")

    # Each JSON record is treated as a chunk
    records = []
    for record in data:
        chunk = " | ".join([f"{key}: {value}" for key, value in record.items()])
        records.append({"content": chunk, "metadata": record})

    # Split the data into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.create_documents([r['content'] for r in records])

    # Embed and save into FAISS vector database
    vectors = FAISS.from_documents(final_documents, embeddings)
    return "Vector store DB is ready."

@app.route('/embed', methods=['POST'])
def embed_documents():
    """
    API endpoint to initialize and embed JSON data.
    Expects 'file_path' in the request JSON.
    """
    try:
        data = request.get_json()
        json_file = data.get("file_path")

        if not json_file or not os.path.exists(json_file):
            return jsonify({"status": "error", "message": "Invalid or missing file path."}), 400

        message = vector_embedding(json_file)
        return jsonify({"status": "success", "message": message}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    """
    API endpoint to answer questions based on the embedded JSON data.
    """
    global vectors
    if not vectors:
        return jsonify({"status": "error", "message": "Documents not embedded yet. Run /embed first."}), 400

    try:
        # Parse input JSON
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"status": "error", "message": "No question provided."}), 400

        # Set up the chain for retrieval and response
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # Process the question and time response
        start = time.time()
        response = retrieval_chain.invoke({'input': question})
        response_time = round(time.time() - start, 2)

        # Prepare response
        answer = response.get("answer", "No answer found.")
        context_chunks = [doc.page_content for doc in response["context"]]

        return jsonify({
            "status": "success",
            "answer": answer,
            "response_time": f"{response_time} seconds",
            "similar_documents": context_chunks
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)