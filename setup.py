from setuptools import setup

setup(
    name="btester",
    author='Paweł Knioła',
    author_email='pawel.kn@gmail.com',
    description='Python framework optimized for running backtests on multiple assets',
    long_description=open('README.md', encoding='utf-8').read(),
    license='MIT',
    keywords='python python3 quantitative analysis backtesting portfolio parallel algorithmic trading',
    url='https://github.com/pawelkn/btester',
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires='>=3.7',
    version="0.0.1",
    packages=['btester'],
)
