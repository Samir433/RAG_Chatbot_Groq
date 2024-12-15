# RAG Chatbot with Groq and Flask

This repository contains a **RAG (Retrieval-Augmented Generation) Chatbot** that leverages **Groq's LLM** and **Google Generative AI Embeddings** to process and analyze data from JSON files. The chatbot is deployed using Flask API.

---

## Table of Contents
1. [Project Setup](#project-setup)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Environment Variables](#environment-variables)
5. [Testing](#testing)
6. [Project Structure](#project-structure)

---

## Project Setup
Follow these steps to set up the project:

### 1. Clone the Repository
```bash
git clone https://github.com/Samir433/RAG_Chatbot_Groq.git
cd RAG_Chatbot_Groq
```

### 2. Create a Virtual Environment
Use the following commands to create and activate a virtual environment:

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Libraries
Install all necessary libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## Usage
1. Run the Flask API server:

```bash
python main.py
```

2. The API will start at:
```
http://127.0.0.1:5000
```

3. Use tools like Postman or cURL to interact with the API.

---

## API Endpoints

### 1. Embed Documents
**Endpoint:** `POST /embed`  
**Description:** Embeds data from a JSON file into the vector database.

**Request Body:**
```json
{
  "file_path": "path_to_your_json_file.json"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:5000/embed -H "Content-Type: application/json" -d '{"file_path": "data/sample.json"}'
```

### 2. Ask Questions
**Endpoint:** `POST /ask`  
**Description:** Processes a question and returns an answer based on the JSON data.

**Request Body:**
```json
{
  "question": "Your question here"
}
```

**Example cURL:**
```bash
curl -X POST http://127.0.0.1:5000/ask -H "Content-Type: application/json" -d '{"question": "What is the shipment name for ID 123?"}'
```

---

## Environment Variables
Create a `.env` file in the root directory and add the following variables:

```
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

Replace `your_groq_api_key` and `your_google_api_key` with valid API keys.

---

## Testing
To test the API:

1. Ensure the Flask server is running (`python main.py`).
2. Use Postman, cURL, or similar tools to test the endpoints.

Example JSON for testing:
```json
[
  {"id": "123", "shipmentName": "Alpha", "owner": "John Doe"},
  {"id": "456", "shipmentName": "Beta", "owner": "Jane Doe"}
]
```

---

## Project Structure
```
RAG_Chatbot_Groq/
│
├── main.py                # Flask API entry point
├── requirements.txt       # List of required libraries
├── .env                   # API keys and environment variables
└── data/                  # Sample JSON files
```

---

## Dependencies
- Flask
- LangChain
- FAISS
- Google Generative AI
- Groq
- dotenv

---

## Notes
- Ensure you have valid API keys for Groq and Google.
- JSON files must contain a list of records for embedding.
- Use tools like Postman for easier testing of endpoints.

---

## License
This project is licensed under the MIT License.

---

## Author
Developed by **[Samir433](https://github.com/Samir433)**.
