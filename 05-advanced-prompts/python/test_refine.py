import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])
model_name = "qwen/qwen3.8-27b"

# 1. Get exact folder path of this script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "aoai-assignment.py")

# 2. Read assignment code
with open(file_path, "r") as f:
    assignment_code = f.read()

# 3. Construct prompt safely without triple quotes
prompt = (
    "I have the following basic Flask app:\n\n"
    "```python\n" + assignment_code + "\n```\n\n"
    "Apply the Self-Refine technique:\n"
    "1. Provide 3 security and code quality improvements.\n"
    "2. Rewrite the code into a secure, production-ready Flask application incorporating those improvements."
)

response = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model=model_name,
)

print(response.choices[0].message.content)