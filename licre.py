#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#

# LiCre - LIcense CREator
#   command-line based license creation tool in Python3 (executable)
#
#   github.com/ferhatgec/licre
#

from json import loads
from datetime import datetime
from requests import get
from sys import argv
from getpass import getuser
from os import remove, path

license_api = 'https://api.github.com/licenses/{license}'

class LiCre:
    def __init__(self):
        self.license_name = ''
        self.license_data = ''
        self.author = ''
        self.year = 0

        self.found = False

    def get_data(self):
        data = get(license_api.format(license=self.license_name)).text

        if len(data) == 0:
            print('Seems license not found!')
            exit(1)

        if not 'body' in data:
            print('Oops!')
            exit(1)

        __json = loads(data)

        self.license_data = __json["body"]

    def replace(self):
        """
        if '<year>' in self.license_data:
            self.license_data = self.license_data.replace('<year>', str(self.year))
        el
        """
        if '[year]' in self.license_data:
            self.license_data = self.license_data.replace('[year]', str(self.year))

        """if '<name of author>' in self.license_data:
            self.license_data = self.license_data.replace('[fullname]', self.author)
        el
        """
        if '[fullname]' in self.license_data:
            self.license_data = self.license_data.replace('[fullname]', self.author)

    def initialize(self, license, name, year):
        self.license_name = license
        self.author = name
        self.year = year

        self.get_data()
        self.replace()

        if not (path.isdir('.git') or path.isdir('.hg')):
            print('Here has not any VCS initializer (git init)')

        if path.isfile('LICENSE'):
            remove('LICENSE')

        with open('LICENSE', 'w') as license_file:
            license_file.write(self.license_data)

        if path.isfile('LICENSE'):
            print(f'{self.license_name.upper()} license created with \'{self.author}\' | {self.year} infos.')

    def check(self):
        current_dir = path.dirname(path.realpath(__file__)).split('/')[-1]

        if len(current_dir) < 1:
            exit(1)

        if get(f'http://github.com/{getuser()}/{current_dir}/blob/master/LICENSE').status_code < 400:
            print('Hahaha. You have already a LICENSE file')

if len(argv) < 2:
    print('LiCre (License Creator)\n'
          '----\n' +
          argv[0] + ' {license_name} {author} {year}')

    exit(1)

if len(argv) > 2:
    author = argv[2]
else:
    author = getuser()

    if len(author) < 1:
        author = '[fullname]'

for i in argv:
    print(i)

if len(argv) > 3:
    year = int(argv[3])
else:
    year = datetime.now().year

init = LiCre()
init.initialize(argv[1], author, year)

init.check()