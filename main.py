import os
import pypandoc

def convert_markdown_files(white_list, black_list, input_directory, output_directory):
    for file in os.listdir(input_directory):
        if file.endswith(".md"):
            path = os.path.join(input_directory, file)

            # 3 conditions to check: 
            # 1. Neither a white list or black list is supplied. In this case 
            # we would match all markdown files within the repository
            # 2. Only a black list is given. We match all markdown files 
            # within the repository that don't match against the black list
            # 3. Only a white list is given. We match all markdown files 
            # within the repository that  match against the white list
            # 4. Both a white and black list are given. We match all 
            # markdown files that don't match against the black list 
            # unless they are on the white list
            
            if (not (white_list) or not(black_list)):
                find_md_files
            
            if (black_list and not(white_list)):
                find_md_files_not_in_black_list

            if (white_list and not(black_list)):
                find_md_files_in_white_list

            if (white_list and black_list):
                find_md_files_bw

def find_md_files(directory):
    md_files = []
    for root, directories, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") or file.endswith(".markdown"):
                md_files.append(os.path.join(root, file))

    return md_files 

def find_md_files_not_in_black_list(directory, black_list):
    md_files_not_black_list = []
    for root, directories, files in os.walk(directory):
        for file in files:
            if (file.endswith(".md") or file.endswith(".markdown")) and not(file in black_list):
                md_files_not_black_list.append(os.path.join(root, file))

    return md_files_not_black_list 

def find_md_files_in_white_list(directory, white_list):
    md_files_in_white_list = []
    for root, directories, files in os.walk(directory):
        for file in files:
            if (file.endswith(".md") or file.endswith(".markdown")) and (file in white_list):
                md_files_in_white_list.append(os.path.join(root, file))

    return md_files_in_white_list 

def find_md_files_bw(directory, black_list, white_list):
    md_files_bw = []
    for root, directories, files in os.walk(directory):
        for file in files:
            if (file.endswith(".md") or file.endswith(".markdown")) and (not(file in black_list) and (file in white_list)):
                md_files_bw.append(os.path.join(root, file))

    return md_files_bw 