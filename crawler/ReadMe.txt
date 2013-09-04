Description : 
=============

       This crawler will fetch all the links/url from the url given as input and again will fetch the urls from the list of urls fetched from the previous link (BFS traversal) and thus continues 

until the specified number of urls have been fetched or the user terminates the execution.


Installation procedure :
=========================


1) Install python 3.0.1 (32-bit)


2) Install the following frameworks


***************************************************************************************


------------------------------------------------
framework Name : lxml 2.2.2 (32-bit)
url : http://pypi.python.org/pypi/lxml/2.2.2

-------------------------------------------------

framework Name : sqllite (32-bit)
url : http://www.sqlite.org/download.html

-----------------------------------------------


****************************************************************************************


procedure to run the crawler :
==============================


1) To launch the crawler:
   1.1) Open the command prompt/shell and navigate to the crawler folder and type the following command
   1.2) python Launcher.py <url> <maxlinks> [max-links is optional]
        Eg 1: python Launcher.py http://python.org 50
	Eg 1: python Launcher.py http://python.org
   A file with list of links fetched will pop up once the specified number of links have been fecthed or when the user terminates the execution or when all the links has been exhausted
    


###########NOTE : MULTIPROCESSING IS NOT SUPPORTED######################

(i.e) if you execute Launcher.py from two command prompt/shell at the same time you won't get expected behaviour


ISSUES TO FIX FOR LATER COMMITS:

The logic for removing the mutiprocessing is not proper, it will be fixed in later commits 
