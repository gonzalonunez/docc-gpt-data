import os
import shutil
import subprocess

def create_dir_forced(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def walk_sources(prompts_dir, final_dir):
    ignored_files = {
        'Package.swift',
    }

    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if not file.endswith('.swift') or file in ignored_files:
                continue

            rel_root = os.path.relpath(root)
            src_file = os.path.join(rel_root, file)
            if not "Sources/" in src_file:
                continue

            # Create a special folder for the source file
            comp_folder = src_file.replace('/', '-').replace('.swift', '')

            # Copy the source file as Prompt.swift over to the prompts directory
            prompt_dir = os.path.join(prompts_dir, comp_folder)
            create_dir_forced(prompt_dir)
            shutil.copy2(src_file, os.path.join(prompt_dir, 'Prompt.swift'))

            # Copy the source file as Completion.swift over to the final directory
            comp_dir = os.path.join(final_dir, comp_folder)
            create_dir_forced(comp_dir)
            shutil.copy2(src_file, os.path.join(comp_dir, 'Completion.swift'))

prompts_dir = 'prompts'
create_dir_forced(prompts_dir)

destination_dir = 'files'
create_dir_forced(destination_dir)

# Walk the sources, copying files over to the prompts directory and the files directory
walk_sources(prompts_dir, destination_dir)

# Run ross on the prompts directory to remove all comments
subprocess.Popen(['mint', 'run', 'ross', prompts_dir, '--remove-plain', 'false']).wait()

# Copy all of the prompts over to the files directory
for root, dirs, files in os.walk(prompts_dir):
    for file in files:
        src_path = os.path.join(root, file)
        parent_dir = os.path.dirname(src_path)
        parent_folder = os.path.basename(parent_dir)
        dest_path = os.path.join(destination_dir, parent_folder, file)
        shutil.copy2(src_path, dest_path)

# Clean up the prompts directory
shutil.rmtree(prompts_dir)

# Format all of /files
subprocess.Popen(['swift', 'format', '--configuration', '.swift-format.json', '--ignore-unparsable-files', '--in-place', '--recursive', destination_dir], stdout=subprocess.PIPE).wait()

# Print total number of files
num_files = 0
for root, dirs, files in os.walk(destination_dir):
    num_files += len(files)

print("🤖 Generated ", num_files / 2, " example pairs.")