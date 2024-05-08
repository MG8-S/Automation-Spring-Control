# -*- coding: utf-8 -*-
import os
import sys

from os.path import basename, abspath, join

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)


def __found_before_path__(path_name: str, relative_path: str = None):
    __before_path__ = None
    __path__ = relative_path if relative_path else os.getcwd()

    while True:
        if basename(str(__path__).lower()) == path_name.lower():
            return __path__

        if __path__ in os.getcwd().split('\\')[0] + "\\":
            raise Exception("Modulo não encontrado")

        __before_path__ = abspath(join(__path__, '..'))

        print(__path__)
        __path__ = __before_path__


def __import_sys_path__(path_name: str, relative_path: str = None):
    path = __found_before_path__(path_name, relative_path)
    sys.path.append(path)


__import_sys_path__('Automacao Spring Control')
