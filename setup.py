# -*- coding: utf-8 -*-
#
# This file is part of the ptwinrm project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

import os
import sys
from setuptools import setup

def main():
    # make sure we use ptwinrm from the source
    _this_dir = os.path.dirname(__file__)
    sys.path.insert(0, _this_dir)

    import ptwinrm

    requirements = [
        'pywinrm',
        'prompt_toolkit',
        'docopt',
        'requests',
    ]

    with open(os.path.join(_this_dir, 'README.rst')) as f:
        readme = f.read()

    setup(
        name='ptwinrm',
        version=ptwinrm.__version__,
        description="winrm console",
        long_description=readme,
        author="Tiago Coutinho",
        author_email='coutinhotiago@gmail.com',
        url='https://github.com/tiagocoutinho/ptwinrm',
        packages=['ptwinrm'],
        entry_points={
            'console_scripts': [
                'ptwinrm=ptwinrm.ptwinrm:main'
            ]
        },
        install_requires=requirements,
        zip_safe=False,
        keywords='windows winrm console',
        license='MIT',
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )


if __name__ == '__main__':
    main()
