from setuptools import setup, find_packages

setup(
    name="SUAPSslotRegister",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",  # Ajouter vos dépendances ici
        "datetime",
        "json",
    ],
    entry_points={
        "console_scripts": [
            "mon_projet=mon_projet.main:main",  # Point d'entrée pour les scripts en ligne de commande
        ],
    },
)