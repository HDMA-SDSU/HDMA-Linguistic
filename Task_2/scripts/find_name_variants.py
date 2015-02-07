__author__ = 'Dhiraj Patil, SDSU'

import logging
from mpl_toolkits.basemap import Basemap, shapefile #need to install the matplotlib basemap toolkit. It doesn't come with matplotlib by default or any of the scientific Python distributions
import sys, os.path
from string import digits
from os.path import dirname
from datetime import datetime
from logging.handlers import RotatingFileHandler
from collections import OrderedDict

def setup_logging(logdir=None, scrnlog=True, txtlog=True, loglevel=logging.DEBUG):
    logdir = os.path.abspath(logdir)

    if not os.path.exists(logdir):
        os.mkdir(logdir)

    log = logging.getLogger(__file__.split('/')[-1].split('.')[0])
    log.setLevel(loglevel)

    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s :: %(message)s")

    if txtlog:
        txt_handler = RotatingFileHandler(os.path.join(logdir, __file__.split('/')[-1].split('.')[0]+".log"), backupCount=5)
        #txt_handler.doRollover()
        txt_handler.setFormatter(log_formatter)
        log.addHandler(txt_handler)
        log.info("Logger initialised.")

def find_name_variants(fileToProcess, loc_ind1, loc_ind2 = -99):
    corelog.info('Start of '+sys._getframe().f_code.co_name)
    d = {}#defaultdict()

    try:
        with open("final.txt", "rb") as fp_word:
            for line in fp_word:
                word = line.split("\t")[0]
                d[word] = 1
        #print d
        d2 = {}
        op_dict = OrderedDict()
        #raw_dict = OrderedDict()
        #new_dict = {}
        flag = None
        with open(fileToProcess, "rb") as fp_place:
            for line in fp_place:
                #print line
                word2 = line.split("\t")[loc_ind1]
                #print word2
                if loc_ind2 != -99:
                    d2[word2] = line.split("\t")[loc_ind2]
                else:
                    d2[word2] = 1
                word_set = word2.split()
                #make case insensitive search
                theset = set(k.lower() for k in d)
                if word2.lower() in theset:
                    # * indicates exact match for the word in Task_1 output dict
                    op_dict[word2+"\t*"] = 1
                else:
                    for word in word_set:
                        if (word and word[0].isupper() and (word in d  or word.lower() in d or word.upper() in d)):
                            #Logic to concatenate multiple words matching criteria, flag to make sure last word has been added to output before
                            #if flag and  next(reversed(op_dict)) <> word:
                            #    new_word = next(reversed(op_dict))+" "+word
                            #    op_dict[word2] = 1
                            #    #op_dict[new_word] = 1
                            #else:
                            #    op_dict[word] = 1
                            #raw_dict[word2] = word
                            op_dict[word2] = 1
                            flag = True
                        else:
                            flag = False
                            continue
                
                #for k, v in raw_dict.iteritems():
                #    new_dict.setdefault(v, []).append(k)
                
                                
                            

    except IOError:
        corelog.info("Required files does not exist, program will terminate!")
        #print "Required files does not exist, program will terminate!"
        sys.exit("Exit")

    #print new_dict
    # Sort words we have got according to keys i.e. t[0]
    sorted_dict = OrderedDict(sorted(op_dict.items(), key=lambda t: t[0]))

    #print sorted_dict.keys()
    dir_name = './../name_variants/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    #os.chdir(dir_name)
    op_file_name = dir_name + 'matching_words_' + fileToProcess.split('/')[-1].split('.')[0] + '.txt'
    with open(op_file_name, "wb") as fp_op:
        for k in sorted_dict.keys():
            if k in d2 and type(d2[k]) is str:
                fp_op.write(k+"\t"+d2[k]+"\n")
            else:
                fp_op.write(k+"\n")
            #fp_op.write('\n'.join(e for e in sorted_dict.keys()))
    corelog.info('End of '+sys._getframe().f_code.co_name)

def find_name_variants_with_suffix_list(fileToProcess, loc_ind1, loc_ind2 = -99):
    corelog.info('Start of '+sys._getframe().f_code.co_name)
    final_dict = {}#defaultdict()
    places_dict = {}
    op_dict = OrderedDict()
    #raw_dict = OrderedDict()
    #new_dict = {}
    flag = None
    suffix_dict = {}
        
    try:
        with open("final.txt", "rb") as fp_word:
            for line in fp_word:
                word = line.split("\t")[0]
                final_dict[word] = 1
        #print d
        
        with open("subregion_suffixes.txt", "rb") as fp_suffix:
            for line in fp_suffix:
                word = line.strip()
                suffix_dict[word] = 1
        d2 = {}
        with open(fileToProcess, "rb") as fp_place:
            for line in fp_place:
                #print line
                word2 = line.split("\t")[loc_ind1]
                #print word2
                if loc_ind2 != -99:
                    places_dict[word2] = line.split("\t")[loc_ind2]
                else:
                    places_dict[word2] = 1
                word_set = word2.split()
                #make case insensitive search
                theset = set(k.lower() for k in final_dict)
                if word2.lower() in theset:
                    # * indicates exact match for the word in Task_1 output dict
                    op_dict[word2+"\t*"] = 1
                else:
                    for word in word_set:
                        if (word and word[0].isupper() and (word in final_dict  or word.lower() in final_dict or word.upper() in final_dict)):
                            #Logic to concatenate multiple words matching criteria, flag to make sure last word has been added to output before
                            #if flag and  next(reversed(op_dict)) <> word:
                            #    new_word = next(reversed(op_dict))+" "+word
                            #    op_dict[word2] = 1
                            #    #op_dict[new_word] = 1
                            #else:
                            #    op_dict[word] = 1
                            #raw_dict[word2] = word
                            op_dict[word2] = 1
                            flag = True
                        else:
                            flag = False
                            continue
                
                #for k, v in raw_dict.iteritems():
                #    new_dict.setdefault(v, []).append(k)
    except IOError:
        corelog.info("Required files does not exist, program will terminate!")
        #print "Required files does not exist, program will terminate!"
        sys.exit("Exit")

    #print new_dict
    # Sort words we have got according to keys i.e. t[0]
    sorted_dict = OrderedDict(sorted(op_dict.items(), key=lambda t: t[0]))

    #print sorted_dict.keys()
    dir_name = './../name_variants/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    #os.chdir(dir_name)
    op_file_name = dir_name + 'matching_words_' + fileToProcess.split('/')[-1].split('.')[0] + '_with_suffix_list.txt'
    with open(op_file_name, "wb") as fp_op:
        for k in sorted_dict.keys():
            if k in d2 and type(d2[k]) is str:
                fp_op.write(k+"\t"+d2[k]+"\n")
            else:
                fp_op.write(k+"\n")
            #fp_op.write('\n'.join(e for e in sorted_dict.keys()))
    corelog.info('End of '+sys._getframe().f_code.co_name)
        
if __name__ == '__main__':
    setup_logging('./../logs')
#    global corelog
    corelog = logging.getLogger(__file__.split('/')[-1].split('.')[0])
    corelog.info('Start of __main__') 
#           
    find_name_variants("./../place_names/Places.txt", 2 , 3)
    find_name_variants("./../place_names/Parks_SD.txt", 8)
    find_name_variants("./../place_names/Community_Plan_SD.txt", 2)
    #find_name_variants_with_suffix_list("./../place_names/Community_Plan_SD.txt", 2)
    
    # Code to close all logging handlers
    handlers = corelog.handlers[:]
    for handler in handlers:
        handler.close()
        corelog.removeHandler(handler)