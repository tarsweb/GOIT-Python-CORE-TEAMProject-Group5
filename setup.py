from setuptools import setup, find_namespace_packages

setup(
    name='assistant',
    version='0.1.0',
    description='Team project groupe 5 GOIT python 20 core',
    url='https://github.com/tarsweb/GOIT-Python-CORE-TEAMProject-Group5',
    author='Group 5',
    license='MIT',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=['prettytable', 'prompt-toolkit', 'wcwidth'],
    entry_points={'console_scripts': ['assistant = assistant.assistant:main']}
)
