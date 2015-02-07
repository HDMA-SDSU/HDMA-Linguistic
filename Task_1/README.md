Task 1 Help & Explanation
----------------------------------
Author: Dhiraj Patil, SDSU.
Document created on: 1/23/2015.
----------------------------------
Overview of problem:
--------------------
In task 1, we take input data from San Diego city-data website (www.city-data.com/forum/san-diego). Basically, we do web crawling for this site and extract the list of place names from this website. In addition, we find all the variants of places present on this website.

Pre-requisites:
------------------------
1. Make sure you have installed Python compiler 2.7 or above and added python installation directory in your system path (varies according to operating system).
2. Another requirement for this utility to work is, you should have 'Stanford CoreNLP' installed and ready to run on your machine.
Stanford CoreNLP integrates many NLP tools, including the
part-of-speech (POS) tagger, the named entity recognizer (NER), the
parser, the coreference resolution system, the sentiment analysis, and
bootstrapped pattern learning tools.
You can download the Stanford CoreNLP from
http://nlp.stanford.edu/software/corenlp.shtml
This is a big suite of java programs.  You will need to have runtime
Java running on your machine.
Download the tools.  And follow the directions for installing them.
Minimally, you will need to add the location of the stanford_ner
source to your java CLASSPATH. 
3. Make sure you have all below mentioned files in same directory. (Assumption for my program)
I have developed and tested this code using Python 2.7 and tested on Windows command line.

Instructions to execute:
------------------------
On any command line such as Unix terminal, Windows command line, Mac terminal, Power Shell; 
% python step1.py
This script does web crawling for website city-data.com with San Diego city forum and downloads HTML files.
Then, we extract data from these HTML files and make text files.
Make sure you have Stanford CoreNLP utility installed and running.

% python step2.py
Output is xml, names and final output file final.txt

Directory structure:
--------------------
Task 1 project directory is as follows:
Task_1
  |_
	logs
		All program execution logs are stored here.
	scripts
		All python script files are stored here.
	sd_city_data
		This directory contains all downloaded html files and respective txt files which contain 			the filtered div tags.
	sd_city_data_final
		This directory contains final.txt file which is final output of Task 1.		
	sd_city_data_xml
		This directory contains xml files i.e. output of CoreNLP which is a location extraction 			utility and names files which are output of processing of these xml files.

Solution files (Scripts):
-------------------------
step1.py
step2.py
helper.py

Data files (Not present initially):
-----------------------------------
	thread_ids.txt
	file_list.txt
	HTML and text files in sd_city_data directory
	XML and names files in sd_city_xml directory
	final.txt file containing list of locations

Please, contact me at: dhirajpatil22@gmail.com for any doubts or queries.

END OF FILE