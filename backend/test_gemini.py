import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file to get the API key
load_dotenv()

try:
    print("Attempting to configure API key...")
    # Configure the client library with your API key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    print("API key configured.")

    print("Listing available models...")
    # List the models to see what your key has access to
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

    print("\nAttempting to create a model instance...")
    # Create an instance of the gemini-pro model
    model = genai.GenerativeModel('gemini-pro')
    print("Model instance created successfully.")

    print("\nSending a test prompt...")
    # Send a simple prompt
    response = model.generate_content("Tell me a fun fact about the Roman Empire.")
    
    print("\nSUCCESS! Response received:")
    print(response.text)

except Exception as e:
    print("\n--- AN ERROR OCCURRED ---")
    print(e)