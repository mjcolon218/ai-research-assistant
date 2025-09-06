import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # or use os.getenv("OPENAI_API_KEY")
print(openai.api_key)
models = openai.models.list()
for m in models.data:
    print(m.id)
