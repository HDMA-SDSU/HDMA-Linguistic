Task 2 Help & Explanation
----------------------------------
Author: Dhiraj Patil, SDSU.
Document created on: 1/25/2015.
----------------------------------
**********************************
Note to all users:
------------------
This is an initial (beta) version of this utility.
Please note that this code is not yet ready for final release.
For more usage information, please read the license document.
**********************************
Overview of problem:
--------------------
In task 2, we make use of data from San Diego city related website (http://www.sangis.org/). A bunch of shape files are downloaded from this site which are processed furthermore to extract locations and compare them with standard list to find variants. 

Pre-requisites:
---------------
1. Make sure you have installed Python compiler 2.7 or above and added python installation directory in your system path (varies according to operating system).
2. Make sure you have all below mentioned files in same directory. (Assumption for my program)
I have developed and tested this code using Python 2.7 and tested on Windows command line.

Instructions to execute:
------------------------
Step1:
Download required zip files containing geographical data from URL http://www.sangis.org/ and keep it in directory ‘/shapefiles’. 
Note: 1 sample directory 'Parks_SD' containing shape-file and other related data and it's related output files have been committed to demonstrate working.
Step2:
On any command line such as Unix terminal, Windows command line, Mac terminal, Power Shell; 
Execute command / Run python script as below:
% python extract_locations_from_shapefile.py.py
This script processes the .shp files and makes dictionary containing place names with relevant geographical information in it. This dictionary is stored as filename.txt. 
Step3:
Execute command / Run python script as below:
% python find_name_variants.py
For each location file in directory ‘/place_names’, locations are compared with standard location data i.e. final.txt (output of Task 1), and output is a text file containing matching words. 

Directory structure:
--------------------
Task 2 project directory is as follows:
Task_2
  |_
	logs
		All program execution logs are stored here.
	scripts
		All python script files are stored here.
	shapefiles
		This directory contains all downloaded zip files and respective shp files in each 				subdirectory.
	place_names
		This directory contains text files which containing location names with relevant 				geographical data extracted rfom shape files.		
	name_vairants
		This directory contains text files i.e. final output of Task 2.

Solution files (Scripts):
-------------------------
extract_locations_from_shapefile.py,
find_name_variants.py,
helper.py

Data files:
-----------
final.txt (Output of Task 1),
.shp files in shapefiles directory,
location names files in place_names directory,
matching locations files containing list of matched locations in name_variants directory.

Please, contact me at: dhirajpatil22@gmail.com for any doubts or queries.

END OF FILE

