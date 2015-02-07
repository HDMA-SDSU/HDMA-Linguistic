__author__ = 'Dhiraj Patil, SDSU'

import logging
import os
import sys, time, re, ntpath, lxml
from os.path import dirname
from datetime import datetime

from lxml import etree
from urllib2 import urlopen, URLError
from bs4 import BeautifulSoup

from helper import load_thread_ids
  
def fetch_links_from_html(url):
    logger.info('Start of fetch_links_from_html')
    #Fetch url using HTTP
    logger.info(url)
    try:
        page = urlopen(url)
    except URLError as e:
        if hasattr(e, 'reason'):
            logger.info('We failed to reach a server.')
            logger.info('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            logger.info('The server couldn\'t fulfill the request.')
            logger.info('Error code: ', e.code)
        sys.exit()    
            
    soup = BeautifulSoup(page)
    linklist = soup('a')
    #print linklist
    logger.info('End of fetch_links_from_html')
    return linklist

def filter_links(linklist):
    logger.info('Start of filter_links')
   #Take out thread links
    good_links  =   []
    url_to_visit_list = []
    for l in linklist:
        try:
            if l['id'].startswith('thread_title') and thread_id_dict.get(l['id'].split('_')[-1]) == None:#Check if link is already present or not
                thread_id_dict[l['id'].split('_')[-1]] = 1
                good_links.append(l)
                #Add actual urls to visit
                url_to_visit_list.append(l['href'])
        except KeyError:
            continue
    logger.info('End of filter_links')
    return url_to_visit_list
                 
def process_links(linklist,i=1):
    logger.info('Start of process_links')
    url_to_visit_list = filter_links(linklist)
    #print url_to_visit_list
    
    thread_download_counter = 0
    for url in url_to_visit_list:
        logger.info(url)
        dir_name = dirname(__file__) + "/../sd_city_data/"+str(i)+"/"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name = dir_name + url.split('/')[-1]
        #print file_name
        write_out_html(url, file_name)
        thread_id_dict[url.split('/')[-1].split("-")[0]] = 1
        logger.info("Id: "+ url.split('/')[-1].split("-")[0] + " added to thread links dict")
        time.sleep(2)    
        thread_download_counter += 1
        write_out_txt(file_name)
        logger.info("Download count is: "+str(thread_download_counter))
    logger.info('End of process_links')        
        
def write_out_html(url, file_name):
    logger.info('Start of write_out_html')
    #Download and save files
    #import urllib
    #urllib.urlretrieve (url) #OR
    #split_list = url.split('/')
    #print split_list
            
    try:
        u = urlopen(url)
    except URLError as e:
        if hasattr(e, 'reason'):
            logger.info('We failed to reach a server.')
            logger.info('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            logger.info('The server couldn\'t fulfill the request.')
            logger.info('Error code: ', e.code)
        sys.exit()
    with open(file_name, 'wb') as fp_op:
        fp_op.write(u.read())
    logger.info('End of write_out_html')    
           
    #meta = u.info()
    #meta doesn't give Content-Length here so commenting all code
    #file_size = 1024#int(meta.getheaders("Content-Length")[0])
    #print "Downloading: %s Bytes: %s" % (file_name, file_size)
    #print u
    #f.write(u)
    #file_size_dl = 0
    #block_sz = 8192
    #while True:
    #    buffer = u.read(block_sz)
    #    print buffer
    #    if not buffer:
    #        break
    #    
    #    file_size_dl += len(buffer)
    #    f.write(buffer)
    #    #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    #    #status = status + chr(8)*(len(status)+1)
    #    #print status,
    #f.close() 
    
def write_out_txt(file_name):
    logger.info('Start of write_out_txt')
    with open(file_name) as fp_op:
        stuff_soup = BeautifulSoup(fp_op)
        
    candidates = stuff_soup('div')
    hits = []
    for c in candidates:
        try:
            id = c['id']
        except KeyError:
            continue
        if id.startswith("post_message"):
            hits.append(c)
    # file_name[-4:] are the last 4 characters of string
    # returns a copy of string with replacement(file_name) made
    txt_file_name = file_name.replace(file_name[-4:], 'txt') 
    with open(txt_file_name, "wb") as txt_fp_op:
        txt_fp_op.write('\n'.join(str(e) for e in hits))
    logger.info('End of write_out_txt')
        
# Main function, automatically called
if __name__ == '__main__':
    LOG_FILENAME = "./../logs/"+str(datetime.now()).replace(":","-")+"-"+os.path.basename(__file__)+".log"
    logging.basicConfig(level=logging.INFO) #logging.DEBUG filename=LOG_FILENAME, filemode='w',
    logger = logging.getLogger(__name__)
    #change level
    logger.setLevel(logging.DEBUG)    
    handler = logging.FileHandler("./../logs/"+str(datetime.now()).replace(":","-")+"-"+os.path.basename(__file__)+".log")
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Start of main')
    logger.info('Load dictionary of downloaded thread ids for further use') 
    global thread_id_dict
    thread_id_dict = load_thread_ids()
    #print thread_id_dict
        
    city_url = 'http://www.city-data.com/forum/san-diego/'
    logger.info('main url to fetch the data: ', city_url)
    logger.info("Fetch links from html (a tags)")
    
    linklist = fetch_links_from_html(city_url)
    process_links(linklist)
    
    last_page = []
    for l in linklist:
        try:
            if l['title'].startswith('Last Page'):
                last_page.append(l['href'])
        except KeyError:
            continue
    last_page_url_parts = last_page[0].split('/')
    #print last_page_url_parts[-1]
    logger.info("Last page url: "+ last_page_url_parts[-1])
    ind = re.search(r"(\d+)",last_page_url_parts[-1])
    logger.info("Last page index: ", ind.group())

    for i in range(1, int(ind.group())):
        all_links = fetch_links_from_html(city_url+"index" + str(i) +".html")
        if all_links:
            process_links(all_links, i)
            
    with open("thread_ids.txt", "wb") as fp_op:
        fp_op.write('\n'.join(e for e in thread_id_dict.keys()))
    logger.info('End of main')
    handler.close()    