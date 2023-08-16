import pypandoc

def convert_file(input_file):
    output_file = pypandoc.convert_file(input_file, 'html')