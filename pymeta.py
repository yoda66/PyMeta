import os
import re
import argparse
import zipfile
import PyPDF2
from lxml import etree as ET


class PyMetaExtractor():

    ext = ['docx', 'xlsx', 'pptx', 'pdf']
    rexp = re.compile(r'.+\.({})$'.format('|'.join(ext)))
    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        print("[*] Starting to search from: [{}]".format(self.directory))
        return

    def run(self):
        for cwd, lod, lof in os.walk(self.directory):
            for f in lof:
                m = self.rexp.match(f)
                if m:
                    fullpath = os.path.join(cwd, f)
                    try:
                        print('[*] {}'.format(fullpath))
                        if m.group(1) == 'pdf':
                            self.pdf(fullpath)
                        else:
                            self.openxml(fullpath)
                        print('')
                    except:
                        continue

    def openxml(self, pathname):
        zf = zipfile.ZipFile(pathname, 'r')
        docprops = ET.fromstring(zf.read('docProps/core.xml'))
        for meta in docprops.findall('*'):
            if meta.tag[0] == '{':
                tag = meta.tag.split('}')[1].title()
            else:
                tag = meta.tag.title()
            value = meta.text
            print('    [+] {:15s} => {}'.format(tag, value))

    def pdf(self, pathname):
        reader = PyPDF2.PdfFileReader(pathname)
        meta = reader.getDocumentInfo()
        for key in meta:
            tag = key.lstrip('/')
            value =  meta[key]
            print('    [+] {:15s} => {}'.format(tag, value))

if __name__ == '__main__':
    print('''
_______________________________________

    PyMeta version 1.0
    Author: Joff Thyer (c) 2020
    Black Hills Information Security
_______________________________________
''')
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='starting directory')
    args = parser.parse_args()
    pm = PyMetaExtractor(args.directory)
    pm.run()