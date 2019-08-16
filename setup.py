''' Setup for g2p
'''
from os import path
import datetime as dt
from setuptools import setup, find_packages

build_no = dt.datetime.today().strftime('%Y%m%d')

# Ugly hack to read the current version number without importing g2p:
# (works by )
with open("g2p/__version__.py", "r", encoding="UTF-8") as version_file:
    namespace = {}
    exec(version_file.read(), namespace)
    VERSION = namespace['VERSION'] + "." + build_no

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='g2p',
    python_requires='>=3.7',
    version=VERSION,
    description='Module for creating context-aware, rule-based G2P mappings that preserve indices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['openpyxl',
                      'coloredlogs',
                      'Flask',
                      'flask_socketio',
                      'flask-talisman',
                      'pyyaml',
                      'regex'],
    zip_safe=False
)
