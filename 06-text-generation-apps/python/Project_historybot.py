import os
from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

# Load environment variables from .env
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def get_available_model():
    """Fetch active chat models from Groq API, prioritizing reliable production models."""
    try:
        models_data = client.models.list()
        available_ids = [m.id for m in models_data.data]
        
        # Explicit priority list of standard, reliable chat models on Groq
        preferred_models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
        
        for model in preferred_models:
            if model in available_ids:
                return model
                
        # Fallback to any active non-whisper/non-guard model
        for model in available_ids:
            if not any(x in model for x in ["whisper", "guard", "audio", "oss", "preview"]):
                return model
                
        return available_ids[0] if available_ids else "llama-3.1-8b-instant"
    except Exception as e:
        print(f"Warning: Could not fetch models list dynamically: {e}")
        return "llama-3.1-8b-instant"

def main():
    print("=== Historical Persona Chatbot ===")
    
    persona = input("Which historical character would you like to speak with? ").strip()
    question = input(f"What question would you like to ask {persona}? ").strip()

    if not persona or not question:
        print("Both persona and question are required.")
        return

    # Select working model dynamically
    model_name = get_available_model()
    print(f"\n[Using model: {model_name}]")

    # System instruction persona
    system_prompt = (
        f"You are playing the role of historical figure: {persona}. "
        "Stay completely in character using appropriate historical perspective and tone. "
        "Remember key historical facts, dates, and timeline details accurately. "
        "Do not invent facts or create unverified content. "
        "If you do not know or cannot verify an answer, state clearly that you do not remember."
    )

    messages: list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Greetings {persona}, my question for you is: {question}"}
    ]

    print("Consulting history...\n")
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            max_tokens=600,
            temperature=0.4
        )
        
        output = response.choices[0].message.content
        if output:
            print(f"[{persona}]:")
            print(output)
        else:
            print(f"[{persona}]: (No text returned by the model)")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()