import ec2_deploy as app
from distutils.core import setup
from setuptools import find_packages


setup(
    name='ec2_deploy',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    version=app.__version__,
    description='Convenient Python Fabric Scrips to Facilitate Code Deployment to AWS EC2',
    author='Glyn Jackson',
    author_email='me@glynjackson.org',
    url='https://github.com/glynjackson/ec2-deploy',  # use the URL to the github repo
    keywords=['ec2', 'deployment', 'aws', 'fabric'],  # arbitrary keywords
    classifiers=[],
    install_requires=[
        'fabric==1.10.1',
        'boto==2.36.0',
        'python-dotenv==0.1.2'
    ],
)