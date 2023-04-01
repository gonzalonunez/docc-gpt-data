import argparse
import openai

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--key', help='Your OpenAI secret API key')
parser.add_argument('--model', default='ada:ft-personal-2023-04-01-02-01-39', help='The name of the model to use')

args = parser.parse_args()
openai.api_key = args.key

with open("prompt.txt", 'r') as prompt_file:
    prompt = prompt_file.read() + "\n\n###\n\n"

    response = openai.Completion.create(
        echo=True,
        max_tokens=2048-len(prompt),
        model=args.model,
        prompt=prompt,
        stop=[" <END>"],
        temperature=0)

    print(response.choices[0].text)

    print('\n---\n')
    print(response.usage)