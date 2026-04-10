import argparse
import os
import sys
from prompts import system_prompt

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):

    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0,tools=[available_functions]),
        )
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        
        
        list_of_function_results = []
        


        if response.function_calls != None:
            for func in response.function_calls:
                function_call_result = call_function(func, verbose)
                if function_call_result is None:
                    raise Exception("The function called has an empty .parts list.")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("The function response object is none")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("The function response is none.")
                
                
                list_of_function_results.append(function_call_result.parts[0])
                
                print("Final response:")
                if verbose: print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            break

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
            messages.append(types.Content(role="user", parts=list_of_function_results))



    else:
        print("The maximum number of iterations was reached without a final response")
        sys.exit(1)
            
        

if __name__ == "__main__":
    main()
