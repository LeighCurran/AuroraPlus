from setuptools import setup
from distutils.core import setup
from os import path

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='auroraplus',
    packages=['auroraplus'],
    version='1.1.6',
    license='MIT',
    description='Python library to access the Aurora+ API: https://api.auroraenergy.com.au/api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Leigh Curran',
    author_email='AuroraPlusPy@outlook.com',
    url='https://github.com/leighcurran/AuroraPlus',
    keywords=['Aurora+', 'AuroraPlus', 'Aurora', 'Tasmania', 'API'],
    install_requires=[
        'requests',
        'requests_oauthlib',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
