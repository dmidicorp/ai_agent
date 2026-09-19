import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

def main():


    load_dotenv()
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("API Key not found, check your API key in .env")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},        
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages,
        temperature=0,
        )

    if response.usage:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError
    print(f"{response.choices[0].message.content}")

if __name__ == "__main__":
    main()
