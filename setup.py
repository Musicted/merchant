from setuptools import setup

setup(
    name='merchantsguide',
    version='0.1.0',
    packages=['merchantsguide'],
    url='',
    license='MIT',
    author='Gavin Lüdemann',
    author_email='gavin.luedemann@gmail.com',
    description='Merchan\'t Guide to the Galaxy',
    install_requires=[
        'parsimonious~=0.8.1',
        'singleton-decorator~=1.0.0'
    ]
)
