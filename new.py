import os
import pypandoc
import subprocess

def convert_mdfile_to_html(input):
    with open(input, 'r') as file:
        md_content = file.read()
    html_content = pypandoc.convert_text(md_content, 'html', format = 'md')
    return html_content

def get_md_files(white_list, black_list, input_repository_path):
    git_files = get_git_files_from_repository(input_repository_path)

    for file in git_files:
        if file.endswith(".md"):
            if (not white_list and not black_list) or (black_list and file not in black_list) or (white_list and file in white_list):
                path_of_file = os.path.join(input_repository_path, file)
                html_content = convert_mdfile_to_html(path_of_file)
                with open(path_of_file.replace(".md", ".html"), 'w'):
                    file.write(html_content)

def get_git_files_from_repository(repo_path):
    git_cmd = ['git', 'ls-files']
    output = subprocess.run(git_cmd, cwd = repo_path, stdout = subprocess.PIPE, text = True)
    git_files = output.stdout.splitlines()
    return git_files

if __name__ == "__main__":
    white_list = [...]
    black_list = [...]
    input_repository_path = "..." # add repo path

    convert_mdfile_to_html(white_list, black_list, input_repository_path)