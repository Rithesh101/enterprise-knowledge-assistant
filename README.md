# Enterprise Knowledge Assistant 

An AI-powered internal assistant that uses a Retrieval-Augmented Generation (RAG) architecture to answer complex, policy-aware employee questions based on an internal knowledge base.

---

## Key Features

-   **Intelligent Q&A:** Leverages a Large Language Model (Gemini) to provide natural, conversational answers grounded in source documents.
-   **Retrieval-Augmented Generation (RAG):** Ensures answers are accurate and prevents AI "hallucination" by retrieving relevant context from a vector database before generating a response.
-   **Role-Based Access Control:** A secure Flask backend with JWT authentication ensures that users can only access information from documents relevant to their department.
-   **Local & Free Embeddings:** Uses a local Hugging Face model (`all-MiniLM-L6-v2`) for creating document embeddings, ensuring data privacy and zero cost.
-   **Modern UI:** A clean and responsive chat interface built with React.js.

---

## Tech Stack

-   **Frontend:** React.js, Vite
-   **Backend:** Flask (Python)
-   **Databases:**
    -   **User Management:** SQLite
    -   **Vector Storage:** FAISS
-   **AI & Orchestration:**
    -   **LLM for Generation:** Google Gemini
    -   **Framework:** LangChain
    -   **Embeddings:** Hugging Face Sentence Transformers

---

## Setup and Installation

### Prerequisites

-   Python 3.10+
-   Node.js and npm
-   A Google AI Studio API Key

### 1. Clone the Repository

```bash
git clone https://github.com/Rithesh101/enterprise-knowledge-assistant
cd enterprise-knowledge-assistant
```

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create a .env file and add your API key
touch .env
echo "GOOGLE_API_KEY='Your-Google-API-Key'" >> .env
echo "JWT_SECRET_KEY='your-super-secret-key-for-jwt'" >> .env

# Place your policy PDFs inside the 'documents/' folder
# (Sample PDFs can be created as needed)

# Run the ingestion script once to create the vector database
python ingest.py
```

### 3. Frontend Setup

```bash
# Navigate to the frontend directory from the root
cd frontend

# Install Node.js dependencies
npm install
```

### 4. Running the Application

1.  **Start the Backend Server:** In your backend terminal, run:
    ```bash
    python app.py
    ```
    The server will be running at `http://127.0.0.1:5000`.

2.  **Start the Frontend Server:** Open a **new terminal** and navigate to the `frontend` directory. Run:
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`.

---

## How to Use

1.  Navigate to the application in your browser.
2.  **Register** a new account, selecting a department (e.g., "HR" or "Engineering").
3.  **Login** with your new credentials.
4.  You will be redirected to the chat interface. Ask a question related to the policy documents you provided!
