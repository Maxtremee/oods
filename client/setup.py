from setuptools import setup

setup(
    name="oodsclient",
    version="0.0.2",
    author="Maksymilian Zadka",
    author_email="maksymilian.j.zadka@gmail.com",
    description='OODS client package',
    install_requires=['oodstools'],
    packages=['oodsclient'],
    package_dir={'oodsclient': 'src'},
)
