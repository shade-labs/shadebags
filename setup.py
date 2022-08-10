from setuptools import find_packages, setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, './README.md'), encoding='utf-8') as f:
    long_description = f.read()

"""
Build Info:
python3 -m build
twine upload dist/*
"""

setup(
    name='shadebags',  # How you named your package folder (MyLib)
    packages=find_packages(),
    version='v1.0.0-beta',
    license='lgpl-2.1',  # Licenses: https://help.github.com/articles/licensing-a-repository
    description='Quickly compress & share indexed rosbags',  # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    ext_modules=[
    ],
    author='Emerson Dove',
    entry_points={'console_scripts': ['shade = shadebags.cli.cli:main']},
    author_email='emerson@shaderobotics.com',
    url='https://github.com/open-shade/shadebags',  # Could be github or website
    keywords=['Robotics', 'Ros', 'Compression'],  # Keywords
    install_requires=[
        'pillow',
        'tqdm',
        'bsdf'
    ],
    classifiers=[
        # Possible: "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'LICENSE :: OSI APPROVED :: GNU LESSER GENERAL PUBLIC LICENSE V2 OR LATER (LGPLV2+)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
