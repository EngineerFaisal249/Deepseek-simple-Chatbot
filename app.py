from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader

# Load API key
load_dotenv()
api_key = os.getenv("key")

if not api_key:
    raise ValueError("API key not found! Check your .env file.")

# Initialize model
model = "deepseek-r1-distill-llama-70b"
deepseek = ChatGroq(api_key=api_key, model_name=model)
parser = StrOutputParser()
deepseek_chain = deepseek | parser

# Load context file
data_path = "data.txt"
if os.path.exists(data_path):
    loader = TextLoader(data_path, encoding="utf-8")
    data = loader.load()
else:
    data = "No context available."

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    template = f"""
    You are an AI chatbot providing accurate answers based only on the given context.  
    Do not make things up.

    Context: {data}
    Question: {user_input}
    """

    response = deepseek_chain.invoke(template)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
