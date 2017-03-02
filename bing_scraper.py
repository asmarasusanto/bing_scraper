"""Scrapes images from Bing images using a search term"""
import argparse
import requests
import json
import shutil
import os

class Image():
    """ Image class for storing image metadata from Bing API call """
    def __init__(self, result):
        self.content_url = result.get('contentUrl')
        self.name = result.get('name')
        self.content_size = result.get('contentSize')
        self.thumbnail_url = result.get('thumbnailUrl')
        self.thumbnail_height = result.get('thumbnail').get('height')
        self.thumbnail_width = result.get('thumbnail').get('width')
        self.image_height = result.get('height')
        self.image_width = result.get('width')
        self.encoding_format = result.get('encodingFormat')
    def __str__(self):
        return self.name + ' ' + self.content_url

def get_imgs(term, offset, key):
    """Returns a list of image objects"""
    base = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'
    payload = {
        'q' : term,
        'count' : 50, # max
        'offset' : offset, # use this for multipass
    }
    header = {'Ocp-Apim-Subscription-Key' : key}
    req = requests.get(base, params=payload, headers=header)

    req_json = req.json()
    return [Image(i) for i in req_json["value"]]

def write_imgs(imgs, dest):
    """Downloads images to disk"""
    if not os.path.exists(dest):
        os.mkdir(dest)

    for i, img in enumerate(imgs):
        try:
            r = requests.get(img.thumbnail_url, stream=True)
            path = dest + str(i) + '.' + img.encoding_format
            if r.status_code == 200:
                # Copy to file in chunks
                with open(path, 'wb') as f:
                   shutil.copyfileobj(r.raw, f)
                f.close()

        except Exception as err:
            print("Could not write " + str(err))



def main():
    """ Get images using search term and write to directory"""
    parser = argparse.ArgumentParser(description='Scrape images from Bing Image Search.')
    parser.add_argument('keyfile', help='File containing Azure API key.', type=argparse.FileType('r'))
    parser.add_argument('term', help='Search term for parsing Bing images')
    parser.add_argument('n', help='Number of images to pull.', type=int)
    parser.add_argument('--d', help='Destination dir for writing images.')

    args = parser.parse_args()

    key = args.keyfile.readline().strip()
    args.keyfile.close()

    imgs = []
    # Get n images
    for offset in range(0,args.n,50):
        imgs += get_imgs(args.term, offset, key)

    write_imgs(imgs, args.d)

if __name__ == "__main__":
    main()
