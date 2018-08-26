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
import html

def main(url, out_folder="./_images/", archive_path = "./_archive/"):
    """Downloads all the images at 'url' to ./_images/"""
    isLocal = False

    if url.lower().startswith("http"):
        # remote file
        soup = bs(urlopen(url), "html5lib")
    else:
        # local file
        try:
            local_file = open(url)
        except FileNotFoundError:
            # doesn't exist
            print("Source file does not exist.")
            sys.exit()
        else:
            # exists
            soup = bs(local_file, "html5lib")
            isLocal = True

    # make sure html entities are unescaped
    soup = bs(html.unescape(soup.prettify(formatter="html5")), "html5lib");

    # create out_folder if not exists
    if not os.path.exists(out_folder):
        print("Directory %s doesn't exist. Creating it now." % out_folder)
        os.makedirs(out_folder)

    _extractImages(soup)

    if isLocal:
        _archiveParsed(url, archive_path)

    print("Complete.")

def _usage():
    print("usage: python dumpimages.py http://example.com [outpath]")

def _archiveParsed(file, archive_path):
    print("archiving source file")
    # create out_folder if not exists
    if not os.path.exists(archive_path):
        print("Archive directory does not exist. Creating it now. (%s)" % archive_path)
        os.makedirs(archive_path)
    filename = os.path.basename(file)
    # print("%s%s" % (archive_path, filename))
    os.rename(url, archive_path + filename)

def _extractImages(soup):
    print("There are %s images" % len(soup.findAll("img")))
    for image in soup.findAll("img"):
        print("Image: %(src)s" % image)
        image_url = urljoin(url, image['src'])
        filename = image["src"].split("/")[-1]
        outpath = os.path.join(out_folder, filename)
        urlretrieve(image_url, outpath)

if __name__ == "__main__":
    archive_path = "./_archive/"
    if len(sys.argv) < 3:
        url = sys.argv[-1]
        out_folder = "./_images/"
    elif len(sys.argv) == 3:
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
    else:
        archive_path = sys.argv[-1]
        out_folder = sys.argv[-2]
        url = sys.argv[-3]
    main(url, out_folder, archive_path)
