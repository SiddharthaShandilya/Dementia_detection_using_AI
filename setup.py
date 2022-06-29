from tkinter.ttk import Notebook
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="src",
    version="0.0.1",
    author="siddhartha",
    description="A small package for dvc ml pipeline demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SiddharthaShandilya/air_quality_index_prediction",
    author_email="siddharthashandilya104gmail.com",
    packages=["src"],
    python_requires=">=3.7",
    install_requires=[
        'dvc',
        'pandas',
        'seaborn',
        'scikit-learn',
        'matplotlib',
        'flask',
        'xgboost',
        'bs4',
        'numpy'
        
    ]
)