__author__ = 'Dhiraj Patil, SDSU'
import glob, os

def add_thread_ids(pathName):
    #thread_id_dict = load_thread_ids()
    os.chdir(pathName)
    for file in glob.glob("*.html"):
        #print(file.split("-")[0])
        if file.split("-")[0] not in thread_id_dict:
            print file
            thread_id_dict[file.split("-")[0]] = 1
    
    #with open("D:/sd_city_data/thread_ids.txt", "wb") as fp_op:
    #    fp_op.write('\n'.join(e for e in thread_id_dict.keys()))
    #fp_op.close()
        
def load_thread_ids():
    d = {}#defaultdict()
    try:
        fp_word = open("thread_ids.txt", "rb")
    except IOError:
        print "Required files does not exist, program will terminate!"
        return None
        #sys.exit()

    # Read "words.txt" file, extract words and put in a dictionary 
    for words in read_words(fp_word):
        for word in words.split("\n"):
            word = word.strip()
            d[word] = 1
    fp_word.close()
    #print d
    return d
    
# Read file yield for memory efficiency
def read_words(file_object):#, bufsize=1024*1024):
    while True:
        #data = file_object.read(bufsize)
        data = file_object.read()
        if not data:
            break
        yield data

def test_dict():
    #thread_id_dict.get(l[id].split('_')[-1]) <> None
    print d
    #if d.get('2183541') == None:
    if '2183541' in d:
        print "*"
            
if __name__ == '__main__':
    global thread_id_dict
    thread_id_dict = load_thread_ids()
    #add_thread_ids("D:\sd_city_data")
        
    try:
        for i in range(1, 374):
            dir_path = "./../sd_city_data/"+str(i)
            if os.path.exists(dir_path):
                print dir_path
                add_thread_ids(dir_path)
    except IOError:
        print "Error"
    
    with open("thread_ids.txt", "wb") as fp_op:
        fp_op.write('\n'.join(e for e in thread_id_dict.keys()))
    fp_op.close()
    print "program exiting"             