import os
import pypandoc 
import subprocess
from typing import Set
from pathlib import Path
import fnmatch

def check_location_file(file_name: str, black_list: Set[str], white_list: Set[str]) -> bool:
    """
    This function takes the file name and two sets: black list and white list. It checks if the file name must be included
    based on the black and white lists. The function returns True if the file should be included. 
    """
    if not black_list and not white_list:
        return True
    elif white_list and not black_list:  # only white list provided
        return file_name in white_list
    elif black_list and not white_list:  # black list only
        return file_name not in black_list
    else:  # both black and white list
        return file_name not in black_list or file_name in white_list

def convert_mdfile_to_html(input_file_path: str) -> str:
    """
    This function takes an input file path which represents the path of the markdown file. It converts
    the markdown file to HTML using pypandoc library. The function returns the path to the generated 
    HTML file as a string if the conversion is successful. 
    """
    markdownfile_path = Path(input_file_path)
    if not markdownfile_path.exists() or not markdownfile_path.is_file() or not markdownfile_path.suffix == ' .md':
        return None
    
    html_file_path = markdownfile_path.with_suffix(' .html')
    with markdownfile_path.open('r') as markdown_file, html_file_path.open('w') as html_file:
        md_content = markdown_file.read()
        html_content = pypandoc.convert_text(md_content, 'html', format='md')
        html_file.write(html_content)

    return str(html_file_path)

def get_md_files(input_repository_path: str):
    """
    This function takes the input repository path that represents the path to a Git repository.
    It reads the black and white lists from files and retrieves a list of markdown files from the
    Git repository which is then converted to HTML. If this conversion is successful, the 
    function adds and commints the HTML files to the Git repository.
    """
    white_list = read_list_folder_to_set('white_list_folder')
    black_list = read_list_folder_to_set('black_list_folder')
    git_files = get_git_files_from_the_repo(input_repository_path)

    for file in git_files:
        if file.endswith(" .md") and check_location_file(file, black_list, white_list):
            filepath = os.path.join(input_repository_path, file)
            html_file_path = convert_mdfile_to_html(filepath)
            if html_file_path:
                add_the_html_file_to_git(html_file_path)
                commit_htmlfile(html_file_path)

def read_list_folder_to_set(foldername: str) -> Set[str]:
    """
    This function takes a folder name and reads the content of the files in the specified
    folder. It returns the contents of the files as a set of strings. 
    """
    fileset = set()
    path_of_folder = Path(foldername)
    if path_of_folder.is_dir():
        for filename in path_of_folder.iterdir():
            if filename.is_file():
                with open(filename, 'r') as file:
                    file_lines = file.read().splitlines()
                    for line in file_lines:
                        if '*' in line or '?' in line:
                            matched_files = [str(path) for path in path_of_folder.glob(line)]
                            fileset.update(matched_files)
                        else:
                            fileset.add(line)
    return fileset


    # if path_of_folder.is_file():
    #    with open(path_of_folder, 'r') as file:
    #     fileset.update(file.read().splitlines())
    # return fileset

def get_git_files_from_the_repo(repository_path: str):
    """
    This function takes a repository path which represents the path to a Git repository. It uses
    Git commands and returns a list of file paths in the repository. 
    """
    git_cmd = ['git', 'rev-parse', '--show-toplevel']
    output = subprocess.run(git_cmd, cwd=repository_path, stdout=subprocess.PIPE, text=True)
    if output.returncode == 0:
        git_root = output.stdout.strip()
        git_files_cmd = ['git', 'ls-files']
        output = subprocess.run(git_files_cmd, cwd=git_root, stdout=subprocess.PIPE, text=True)
        git_file = output.stdout.splitlines()
        return git_file
    else:
        return None

def add_the_html_file_to_git(html_file_path: str):
    """
    This function takes an HTML file path and uses Git to add this HTML file to the staging 
    area for the next commit. 
    """
    git_add_cmd = ['git', 'add', html_file_path]
    subprocess.run(git_add_cmd)

def commit_htmlfile(html_file_path: str):
    """
    This function takes an HTML file payj and commits it to the Git repository with a commit
    message that indicates whether it is an addition or an update of the HTML file. 
    """
    git_commit_cmd = ['git', 'commit', '-m', f'Add/Update the HTML file: {html_file_path}']
    subprocess.run(git_commit_cmd)

