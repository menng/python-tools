# -*- coding: utf-8 -*-

from qiniu import Auth, put_file
import time, os, sys

access_key = "xxxxxxxxxx"
secret_key = "xxxxxxxxxx"
bucket_url = "xxxxxxxxxx"
bucket_name = "xxxxxxxxxx"
key = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))

def upload_file(filename):
    my_path = os.path.abspath(os.path.dirname(__file__))

    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, key, expires=3600)

    localfile = os.path.join(my_path, filename)
    ret, info = put_file(token, key, localfile)
    return

def get_img_url(bucket_url, file_name):
    img_url = 'http://%s/%s' % (bucket_url, file_name)
    md_url = "![](%s)" % img_url
    return md_url

def addToClipBoard(text):
	command = 'echo ' + text.strip() + '| clip'
	os.system(command)

if __name__ == '__main__':
    imgs = sys.argv[1:]
    for img in imgs:
        upload_file(img)
        addToClipBoard(get_img_url(bucket_url, key))
