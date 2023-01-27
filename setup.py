from setuptools import setup, find_packages

setup(
    name='Fetch_data_TGE_PSE',
    packages=find_packages(),
    email='kaczmarek.rafal98@gmail.com',
    author='Rafal Kaczmarek',
    install_requires=[
        'click',
        'bs4',
        'pandas',
        'datetime',
        'requests',
        'lxml'
    ],
    version='0.9.0',
    entry_points='''
    [console_scripts]
    Fetch_data_TGE_PSE=fetch_data:download_data
    '''
)
