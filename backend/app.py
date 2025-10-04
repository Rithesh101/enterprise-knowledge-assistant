import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, JWTManager
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings # <-- CHANGED
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- APP SETUP ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# --- RAG CHAIN SETUP ---

model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name) # <-- CHANGED

vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
llm = ChatGoogleGenerativeAI(model="gemini-pro-latest") 
system_prompt = (
    "You are an expert assistant for answering questions about company policy. "
    "Use the following retrieved context to answer the question. "
    "If the context does not contain the answer, state that you don't know. "
    "Keep your answers concise and professional."
    "\n\n"
    "{context}"
)
prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# --- AUTHENTICATION ENDPOINTS ---
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    department = data.get('department')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(email=email, department=department)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # The identity is now just the user's email (a string)
        # We put the department in additional_claims
        additional_claims = {"department": user.department}
        access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
        return jsonify(access_token=access_token)

    return jsonify({"message": "Invalid credentials"}), 401

# --- CORE CHATBOT ENDPOINT ---
@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    claims = get_jwt()
    user_department = claims.get("department", "General")
    
    data = request.get_json()
    user_question = data.get('question')

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    # Retriever with role-based filtering
    retriever = vectorstore.as_retriever(
        search_kwargs={'filter': {'department': {'$in': [user_department, 'General']}}}
    )
    
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    response = rag_chain.invoke({"input": user_question})
    return jsonify({"answer": response["answer"]})

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    with app.app_context():
        instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
        db.create_all()
    app.run(debug=True, port=5000, use_reloader=False)