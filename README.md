# bing_scraper
Python module for scraping bing images using Azure API
usage: bing_scraper.py [-h] [--d D] keyfile term n

Scrape images from Bing Image Search.

positional arguments:
  keyfile     File containing Azure API key.
  term        Search term for parsing Bing images
  n           Number of images to pull.

optional arguments:
  -h, --help  show this help message and exit
  --d D       Destination dir for writing images.
  
  
  
  NOTE: Currently only pulls thumbnails. Original intention was small images for training but will add a flag to toggle this feature.
