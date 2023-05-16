#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sys
import os
import requests
import shutil

RECUR = 0


# Getting every links on the page
def getlinks(addr):
    global RECUR
    loop = RECUR
    current_len = len(addr)
    while loop < current_len:
        try:
            html_page = requests.get(addr[loop])
        except Exception:
            loop += 1
            continue
        soup = BeautifulSoup(html_page.text, 'html.parser')
        for link in soup.find_all('a'):
            try:
                if link.get('href').startswith("http://") or link.get('href').startswith("https://"):
                    addr.append(link.get('href'))
                else:
                    addr.append(addr[0] + link.get('href'))
                print("\33[2K\rAdding from : " + addr[loop], end="")
            except Exception:
                print("\33[2K\r<a> tag doesn't have a link", end="")
        loop += 1
    RECUR = loop
    return addr


def getimages(addr, folder):
    for link in addr:
        try:
            for img_link in BeautifulSoup(requests.get(link).text, 'html.parser').find_all('img'):
                if (img_link.get('src').startswith("http")):
                    if img_link.get('src').endswith('.png') or img_link.get('src').endswith('.bmp') or img_link.get('src').endswith('.jpg') or img_link.get('src').endswith('.jpeg') or img_link.get('src').endswith('.gif'):
                        r = requests.get(img_link.get('src'), stream=True)
                        print("\33[2K\rSaving : " + img_link.get('src'), end="")
                        with open(folder + img_link.get('src').rsplit('/', 1)[1], 'wb') as out_file:
                            shutil.copyfileobj(r.raw, out_file)
                    else:
                        print("\33[2K\rNot a picture", end="")
        except Exception:
            continue


def main(argv):
    recursive = 0
    path = "./data/"
    if len(argv) < 2:
        print("Manque des arguments bonhomme")
    else:
        argv.pop(0)
        while len(argv) != 1:
            if argv[0] == "-r":
                argv.pop(0)
                if argv[0] == "-l":
                    argv.pop(0)
                    recursive = int(argv[0])
                    continue
                else:
                    recursive = 5
                    continue
            if argv[0] == "-p":
                argv.pop(0)
                path = "./" + argv[0] + "/"
                continue
            else:
                argv.pop(0)
        os.system("rm -rf " + path + " 2> /dev/null")
        os.system("mkdir " + path + " 2> /dev/null")
        addr = []
        addr.append(argv[0])
        if recursive != 0:
            recursive += 1
            while recursive != 0:
                addr = getlinks(addr)
                addr = list(dict.fromkeys(addr))
                recursive = recursive - 1
        getimages(addr, path)


main(sys.argv)
