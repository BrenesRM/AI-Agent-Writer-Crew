#!/usr/bin/env python3

from llama_cpp import Llama

# Load your local model (adjust path if needed)
MODEL_PATH = "./llama-3.2-1b-instruct-q8_0.gguf"
llm = Llama(model_path=MODEL_PATH, n_threads=4)  # Adjust threads as needed

def agente_query(prompt: str, max_tokens: int = 150) -> str:
    """
    Sends a prompt to the LLaMA model and returns the response text.
    """
    result = llm(prompt, max_tokens=max_tokens)
    return result['choices'][0]['text'].strip()

def main():
    print("=== Agente Local LLaMA ===")
    user_prompt = input("Enter your prompt for the agent: ")
    response = agente_query(user_prompt)
    print("\n[Agent Response]:")
    print(response)

if __name__ == "__main__":
    main()
