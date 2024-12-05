from setuptools import setup, find_packages

setup(
    name='monte_carlo',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    author='Robert Clay Harris',
    author_email='jbm2rt@virginia.edu',
    description='A Monte Carlo Simulator',
    url='https://github.com/robertclayh/monte_carlo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)