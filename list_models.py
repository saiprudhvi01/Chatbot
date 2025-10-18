import os
import google.generativeai as genai

# Set the API key directly for testing
genai.configure(api_key='xxxxx')

models = genai.list_models()
for model in models:
    print(f"{model.name}: {model.supported_generation_methods}")
