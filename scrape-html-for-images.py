"""
dumpimages.py
    Downloads all the images on the supplied URL, and saves them to the
    specified output file ("/test/" by default)

Usage:
    python dumpimages.py http://example.com/ [output]
"""
from bs4 import BeautifulSoup as bs
from urllib.request import (
    urlopen, urlparse, urlunparse, urlretrieve, urljoin)
import os
import sys

def main(url, out_folder="./_images/"):
    """Downloads all the images at 'url' to ./_images/"""

    if url.lower().startswith("http"):
        # remote file
        print("Opening remote file")
        soup = bs(urlopen(url))
    else:
        # local file
        print("Opening local file")
        soup = bs(open(url), "html.parser")

    if not os.path.exists(out_folder):
        print("Directory %s doesn't exist. Creating it now." % out_folder)
        os.makedirs(out_folder)

    parsed = list(urlparse(url))

    print("Checking for images")
    print("There are %s images" % len(soup.findAll("img")))
    for image in soup.findAll("img"):
        print("image")
        # print "Image: %(src)s" % image
        image_url = urljoin(url, image['src'])
        filename = image["src"].split("/")[-1]
        outpath = os.path.join(out_folder, filename)
        urlretrieve(image_url, outpath)

def _usage():
    print("usage: python dumpimages.py http://example.com [outpath]")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        url = sys.argv[-1]
        out_folder = "./_images/"
    else:
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
    main(url, out_folder)
