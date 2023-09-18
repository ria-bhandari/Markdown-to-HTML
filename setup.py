from setuptools import setup, find_packages

setup(
    name='md2html',
    version='0.1',
    packages=find_packages(),
    install_requirements=[
        'pypandoc',
        'subprocess',
        'pathlib',
    ],
)