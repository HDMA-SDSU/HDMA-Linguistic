__author__ = 'Dhiraj Patil, SDSU'
import logging
from mpl_toolkits.basemap import Basemap, shapefile #need to install the matplotlib basemap toolkit. It doesn't come with matplotlib by default or any of the scientific Python distributions
import sys, os.path
from string import digits
from os.path import dirname
from datetime import datetime

def extract_locations_from_shapefile():
    logger.info('Start of extract_locations_from_shapefile()')
    shapefile_path = './../shapefiles'
    try:
        if os.path.exists(shapefile_path):
            os.chdir(shapefile_path)
        else:
            logger.error('Cannot find dir=%s', shapefile_path)
            print "NO dir: "+shapefile_path
            sys.exit("Exit")
    except OSError, e:
        sys.exit("Error")
        logger.error('Failed to open dir', exc_info=True)
        
        
    list_dir = [direct for direct in os.listdir('./../shapefiles') if not direct.endswith('.zip') and not os.path.isfile(direct)] 
    #print list_dir
    logger.debug(list_dir)
    
    for i, shape_file_dir in enumerate(list_dir):
        op_file_name = shape_file_dir+".txt"
        if not os.path.isfile("./../place_names/"+op_file_name):
            shape_file = os.path.join(shape_file_dir, shape_file_dir)
            logger.debug('%s iteration %s',i,shape_file)
            
            r = shapefile.Reader(shape_file)
            shapes = r.shapes()
            #logger.info(shapes)
            records = r.records()
            place_set = set()
            def_dir_name = dirname(__file__)
            #os.chdir(def_dir_name+"/../place_names")
                    
            with open("./../place_names/"+op_file_name, "wb") as fp_op:
                for idx, record in enumerate(records):
                    #print record
                    str1 = '\t'.join(str(v) for v in record)
                    #print str1
                    fp_op.write(str(idx+1)+ "\t" +str1)
                    fp_op.write("\n")
                    #print record[2].translate(None, digits)#,"\t", record[7] 
                    #place_set.add(record[7].strip())
            #print place_set
        
    logger.info('End of extract_locations_from_shapefile()')
        
if __name__ == '__main__':
    #print dir(mpl_toolkits)
    #print sys.path
    
    logging.basicConfig(level=logging.INFO) #logging.DEBUG
    logger = logging.getLogger(__name__)
    #change level
    logger.setLevel(logging.DEBUG)    
    
    #handler = logging.FileHandler("./../logs/"+str(datetime.now()).replace(":","-")+"-"+os.path.basename(__file__)+".log")
    ## create a logging format
    #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')#- %(name)s
    #handler.setFormatter(formatter)
    ## add the handlers to the logger
    #logger.addHandler(handler)

    logger.info('Start main')
    extract_locations_from_shapefile()
    logger.info('End of main')
    #handler.close()