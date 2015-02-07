__author__ = 'Dhiraj Patil, SDSU'
import os, sys, glob, subprocess, time
reload(sys)
sys.setdefaultencoding("utf-8")
from os.path import dirname
from lxml import etree
from collections import OrderedDict
#from __future__ import print_function

def make_file_names_list():
    print "function to make file names list to feed it to CoreNLP"
    os.chdir(dirname(__file__))
    with open("file_list.txt", "wb") as fp_op: #overwrite all records every time to maintain atomicity
        for i in range(1, 375):#int(ind.group())):
            dir_name = dirname(__file__)+"/"+str(i)
            if os.path.exists(dir_name):
                os.chdir(dir_name)
                for file in glob.glob("*.txt"):
                    print file
                    fp_op.write(os.path.abspath(file)+'\n')
    print "make_file_names_list exiting"

def make_xml():
    #COMMAND = """
    #exec {JAVA} -Xmx{XMX_AMOUNT} -cp {CLASSPATH}
    #corenlp.PipeCommandRunner {mode} {startup_tmp}"""
    dir_name = "C:/stanford-corenlp-full-2014-10-31"
    os.chdir(dir_name)
    # Make sure to set appropriate parameter for outputDirectory = D:\Task_1\sd_city_data_xml in annotator.properties
    COMMAND = """java -cp stanford-corenlp-3.5.0.jar;stanford-corenlp-3.5.0-models.jar;xom.jar;joda-time.jar;jollyday.jar;ejml-0.23.jar -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -props annotator.properties -filelist D:\\Task_1\\file_list.txt"""
    #COMMAND = "dir
    #    """
    #subprocess.call(COMMAND, shell=True)
    global proc
    proc = subprocess.Popen(COMMAND, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)#, shell=True, stdin=subprocess.PIPE, 
    
    while proc.poll() is None:
        print "Still working"
        time.sleep(5)
    print proc.poll()
    stdout,stderr = proc.communicate()
    print ('This was "' + stdout + '"')
    print "make_xml exiting"
    
def parse_xml(file_name):
    word_dict = OrderedDict()
    #file_name = 'D:/sd_city_data/40/584727-living-downtown-vs-other-nearby-options.txt.xml'
    try:
        doc = etree.parse(file_name)
    except IOError:
        print "Error"
        sys.exit()
    #href_xpath = "//a/@href"
    flag = False
    prev_token_id = ""
    prev_sentence_id = ""
    for token in doc.xpath('//token'):
        #print token.xpath("./NER/text()")
        if token.xpath("./NER/text()")[0] == 'LOCATION':
            sentence_id = token.xpath('ancestor::sentence/@id')[0]
            #print sentence_id
            token_id = token.xpath("./@id")[0]
            #print prev_token_id+"*"+str(int(token_id)-1)
            word = token.xpath("./word/text()")[0]
            ###########################################################################
            #Remove tags from word like <br>, <a>, <b> or eve nspecial chars like '&'
            word = etree.strip_elements(word, *['<br>', '<a>', '<b>'])
            word = etree.tostring(word)
            ###########################################################################
            if flag and prev_sentence_id == sentence_id and prev_token_id == str(int(token_id)-1) and next(reversed(word_dict)) <> word:
                #print prev_token_id, "*", str(int(token_id)-1)
                word = next(reversed(word_dict))+" "+word
                word_dict.popitem(last=True)
            if word not in word_dict:
                word_dict[word] = 1
            else:
                word_dict[word] += 1 
            prev_token_id = token_id
            prev_sentence_id = sentence_id
            flag = True    
            #print token_id, '\t', word
            
    print word_dict
    #print file_name
    #names_file = file_name.replace(file_name[:-3], 'names') 
    names_file = file_name[:-3]+'names'
    print names_file
    with open(names_file, "wb") as fp_op:
        for key, value in word_dict.items():
            #fp_op.write(key+" "+str(value)+"\n")
            fp_op.write(u'\t'.join((key, str(value), "\n")).encode('utf-8'))
    #return word_dict.items()
    print "parse_xml exiting"
    
def make_names_files(xml_loc):
    os.chdir(xml_loc)
    for file in glob.glob("*.xml"):
        new_path = os.path.abspath(file).replace("\\", "/")
        #print new_path
        parse_xml(new_path)
    print "make_xml exiting"
    
def make_global_word_list(xml_loc, final_file_name):
    global_dict = {}
    os.chdir(xml_loc)

    for file in glob.glob("*.names"):
        file_name = os.path.abspath(file).replace("\\", "/")
        with open(file_name, "rb") as fp_op:
            for line in fp_op:
                key, value = line.split('\t')[:2]
                #print key, value
                #if (key.lower() in global_dict or key.upper() in global_dict):
                if (key in global_dict):
                    global_dict[key] = global_dict[key] + int(value)
                else:
                    global_dict[key] = int(value)
                    
    # Sort words we have got according to keys i.e. t[0]
    sorted_dict = OrderedDict(sorted(global_dict.items(), key=lambda t: t[0]))            
    with open(final_file_name, "wb") as fp_op:
        for key, value in sorted_dict.items():
            #fp_op.write(key+" "+str(value)+"\n")
            fp_op.write(u'\t'.join((key, str(value), "\n")).encode('utf-8'))
    
if __name__ == '__main__':
    # Properties file like structure to use in Python OR
    #http://stackoverflow.com/questions/3595363/properties-file-in-python-similar-to-java-properties
    global props
    props = {}
    try:
        with open('config.properties', 'rb') as f:
            for line in f:
                line = line.rstrip() #removes trailing whitespace and '\n' chars
                if ("=" in line and not line.startswith("#")):
                    k, v = line.split("=", 1)
                    props[k] = v
    except IOError:
        print "Properties file load error, program will exit!"
        sys.exit()
    
    print props
    
    make_file_names_list()
    make_xml()
    make_names_files(props["xml_loc"])
    
    #Sample usuage of properties below
    #props[xml_loc] #= "D:/sd_city_data_xml"
    #props[final_loc] #= "D:/sd_city_data_final/"
    #props[global_word_list_file_name] #= "final.txt"
    final_file_name = props["xml_loc"] + props["global_word_list_file_name"]
    print final_file_name
    make_global_word_list(props["xml_loc"], final_file_name)
    print "main exiting"
    
    