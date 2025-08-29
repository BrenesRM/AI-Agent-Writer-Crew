#!/usr/bin/env python3
from llama_cpp import Llama

# Use relative path since model is in the same folder as this script
model = Llama(model_path="./llama-3.2-1b-instruct-q8_0.gguf")

output = model("Hello, I am a local LLaMA model!", max_tokens=50)
print(output['choices'][0]['text'])
