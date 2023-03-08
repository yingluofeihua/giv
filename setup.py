# @Time : 2023/3/9 0:40
# @Author : Administrator
# @File : setup.py
# @Software: PyCharm

from setuptools import setup

setup(
    name='giv',
    version='0.1',
    py_modules=['giv'],
    entry_points={
        'console_scripts': [
            'giv=giv:generative',
        ],
    },
)