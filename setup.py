from setuptools import setup

setup(
    name='Riki',
    packages=['wiki', 'personalize', 'web'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
