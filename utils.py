# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from subprocess import Popen, PIPE
import os
import re
from distutils.version import LooseVersion
import platform

def iswin():
    return platform.platform().upper().startswith('WIN')

def islinux():
    return platform.platform().upper().startswith('LINUX')
def get_locale_codec():
    """
    Is Very Very Useful
    :return:
    """
    import locale
    import codecs
    return codecs.lookup(locale.getpreferredencoding()).name

def exec_cmd(cmd, shell=True):
    """
    only can be used in shell
    :param cmd:" " or []
    :param shell: default True
    :return: [str1,str2,...]
    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell)

    stdout_data, stderr_data=p.communicate()
    p.wait()

    codec=get_locale_codec()

    try:
        stdout_data = stdout_data.decode(codec, errors='ignore')
        stderr_data = stderr_data.decode(codec, errors='ignore')
    except UnicodeDecodeError:
        codec='utf-8'
        stdout_data = stdout_data.decode(codec, errors='ignore')
        stderr_data = stderr_data.decode(codec, errors='ignore')

    finally:
        return stdout_data.split(os.linesep), stderr_data.split(os.linesep)

class DoNotHaveProperVersion(BaseException):pass

def has_proper_tesseract(min_version=None):
    min_version=None
    if iswin():
        tesseract_name = 'tesseract.exe'
    else:
        tesseract_name = 'tesseract'

    info_lines, err_lines=exec_cmd('%s -v'%tesseract_name)

    # java output stream is stderr !!!
    if len(info_lines) == 1 and info_lines[0]=='':
        return False

    if min_version is not None:
        v1 = LooseVersion(min_version)

        pattern = r"(\d+.){2}\d+"
        result=re.search(pattern, info_lines[0]).group(0)
        v2 = LooseVersion(result)

        return v1 <= v2

    return True

