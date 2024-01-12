from setuptools import setup

setup(
    name="btlib",
    author='Paweł Knioła',
    author_email='pawel.kn@gmail.com',
    description='Backtest library focused on portfolio testing',
    long_description=open('README.md', encoding='utf-8').read(),
    license='MIT',
    keywords='quantitative analysis backtesting parallel algorithmic trading',
    url='https://github.com/pawelkn/backtester',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',

    version="0.0.1",
    packages=['btlib'],
)
