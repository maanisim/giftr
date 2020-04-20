from setuptools import setup

setup(
    name='backend',
    packages=['backend'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-login',
        'flask-sqlalchemy'
    ],
)