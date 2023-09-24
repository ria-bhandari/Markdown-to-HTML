from setuptools import setup, find_packages

setup(
    name = 'md2html_package',
    version = '0.1',
    package = find_packages(),
    install_requires = [
        'pypandoc',
        'matplotlib',
    ],
    entry_points = {
        'console_scripts': [
            'md2html_script = md2html_package.md2html_script: get_md_files',
        ],
    },
)