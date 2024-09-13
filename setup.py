from setuptools import setup, find_packages

setup(
    name='ElectionsAPE',
    version='0.1.0',
    description='Aplicação de terminal que visa mostrar ao usuário informações sobre seu(s) candidadato(s).',
    authors=['Arthur Araújo', 'Davi César', 'Davi Leite', 'Clara Alcântara'],
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'elect-ape=elections.menu:main',
        ],
    },
    python_requires='>=3.10',
)