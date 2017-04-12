from setuptools import setup

setup(
    name='ctrp_rest_client',
    packages=['ctrp_rest_client'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-Bootstrap',
        'Flask-WTF',
        'Flask-Bower',
        'Flask-WTF',
        'requests',
        'ruamel.yaml',
    ],
)
