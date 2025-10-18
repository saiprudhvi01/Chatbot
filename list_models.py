import os
import google.generativeai as genai

# Set the API key directly for testing
genai.configure(api_key='AIzaSyDThnvak5WKtNoCN3c3PgJWo5E-35MNqis')

models = genai.list_models()
for model in models:
    print(f"{model.name}: {model.supported_generation_methods}")
