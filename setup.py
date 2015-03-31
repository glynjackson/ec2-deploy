import ec2_deploy as app
from distutils.core import setup
from setuptools import find_packages

setup(
    name='ec2_deploy',
    packages=find_packages(exclude=['tests*', 'demo*', 'server_templates*']),
    include_package_data=True,
    version=app.__version__,
    description='EC2 Deploy is a convenient deployment tool to facilitate code deployment and other tasks to AWS EC2.',
    license='The MIT License',
    author='Glyn Jackson',
    author_email='me@glynjackson.org',
    url='https://github.com/glynjackson/ec2-deploy',
    keywords=['ec2', 'deployment', 'aws', 'fabric', 'environment variables', 'amazon', 'boto'],
    classifiers=[],
    install_requires=[
        'fabric==1.10.1',
        'boto==2.36.0',
        'python-dotenv==0.1.2',
        'gitpython==0.3.6',
    ],
)