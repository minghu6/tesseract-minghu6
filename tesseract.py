# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from PIL import Image
import requests

from utils import *

class NotValidPathStr(BaseException):pass

def get_image(s:str, outdir=None, captcha_name='captcha', session:requests.Session=None):

    from urllib.request import urlretrieve

    import re
    url_net = "(https?|ftp)://[a-zA-Z0-9+&@#/%?=~_|$!:,.;]*[a-zA-Z0-9+&@#/%=~_|$]"
    pattern_url_net = url_net
    if re.match(pattern_url_net, s) is not None:
        if outdir is not None:
            filepath = os.path.join(outdir, captcha_name)
        else:
            filepath = captcha_name

        if session is None:
            if os.path.exists(captcha_name):
                os.remove(captcha_name)
            urlretrieve(s, filename=filepath)
        else:
            r=session.get(s)
            with open(captcha_name, 'wb') as imgFile:
                imgFile.write(r.content)

        with Image.open(filepath) as imgObj:
            newfilepath = filepath + '.'+imgObj.format.lower()

        if os.path.exists(newfilepath):
            os.remove(newfilepath)

        os.rename(filepath, newfilepath)
        with Image.open(newfilepath) as img:
            imgObj = img.copy()

        #imgObj.show()
        return imgObj, newfilepath
    elif os.path.isfile(s):
        with Image.open(s) as img:
            imgObj = img.copy()

        return imgObj, s
    else:
        raise NotValidPathStr(s)

def tesseract(path, limit_config=None, args=None, session:requests=None):
    if not has_proper_tesseract():
        raise DoNotHaveProperVersion

    imgObj, image_path=get_image(path, session=session)

    if args is None:
        cmd_str = 'tesseract -psm 8 {0} stdout '.format(image_path)
    else:
        cmd_str = ' '.join(['tesseract', args, image_path, 'stdout'])
        print(cmd_str)

    if limit_config is not None: #like digits
        cmd_str  += ' {0}'.format(limit_config)

    info_lines, err_lines = exec_cmd(cmd_str, shell=True)

    try:
        captchaResponse = info_lines[0].strip()
    except IndexError:
        raise Exception(''.join(err_lines))
    else:
        return captchaResponse