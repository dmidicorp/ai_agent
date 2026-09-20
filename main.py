import os
import sys
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions, call_function

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
    result = ""

    for _ in range(20):

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},        
        ]
    for _ in range(20):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages= messages,
            tools = available_functions,
            )
        
        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls != None:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
            
                result_message = call_function(tool_call, function_args)
                messages.append(result_message)

                if not result_message['content']:
                    raise Exception("Error: call_function failed to return content: None")
        
        if response.usage:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
                print(f"-> {result_message['content']}")
        else:
            raise RuntimeError
        
        if message.content and not message.tool_calls:
            result = response.choices[0].message.content
            break
    if result:
        print(result)
    else:
        print("Error: Agent execution aborted due to no response within established limit")
        sys.exit(1)

if __name__ == "__main__":
    main()
