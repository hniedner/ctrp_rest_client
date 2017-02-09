from setuptools import setup

setup(
    name='ctrp_rest_client',
    packages=['ctrp_rest_client'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-Bootstrap',
        'flask-nav',
        'Flask-WTF',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'requests',
        'visitor',
        'Werkzeug',
        'WTForms',
    ],
)
