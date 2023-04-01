import json
import os

dir_path = "files"
separator = "\n\n###\n\n"

json_data = []

for subdir in [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]:
    prompt_path = os.path.join(dir_path, subdir, 'Prompt.swift')
    completion_path = os.path.join(dir_path, subdir, 'Completion.swift')

    with open(prompt_path, 'r') as prompt_file:
        with open(completion_path, 'r') as completion_file:
            prompt_contents = prompt_file.read().strip()
            completion_contents = completion_file.read().strip()

            json_data.append({
                "prompt": prompt_contents + separator,
                "completion": " " + completion_contents + " <END>"
            })

            completion_file.close()            
        prompt_file.close()

with open('data.jsonl', 'w') as data_file:
    for pair in json_data:
        json_string = json.dumps(pair)
        data_file.write(json_string)
        data_file.write("\n")
