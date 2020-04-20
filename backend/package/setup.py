from setuptools import setup

setup(
    name='giftr',
    packages=[('.')],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-login',
        'flask-sqlalchemy'
    ],
)