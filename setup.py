import subprocess
from setuptools import setup
from setuptools import find_packages
from setuptools import Command
import os

file_path = os.path.dirname(os.path.realpath(__file__))

def version():
    return "0.01.alpha"


def readme():
    filename = os.path.abspath(os.path.join(file_path, 'README.md'))
    with open(filename) as f:
        return f.read()

class Runtests:
    def run(self):
        cmd = ['py.test']
        subprocess.check_call(' '.join(cmd), cwd=file_path, shell=True)


setup(
    name='gangagsoc',
    packages=['gangagsoc'],
    version='1.0',
    license='gpl-3.0',
    description='The Challenge for GSoC 2020 student to particpate in the Ganga project',
    author='Ratin Kumar',
    author_email='ratin.kumar.2k@gmail.com',
    url='https://github.com/dumbmachine/GangaGSoC2020',
    keywords=['GSoC', 'Ganga', 'Challenge'],
    install_requires=[
          'pytest',
          'ganga',
          'PyPDF2',
          'pymongo',
        #   'alchemy'
      ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3.0',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # cmdclass={
    #     # "tests": Runtests,
    # }
)
