
1) Install python 3.0.1 (32-bit) then follow the instructions below to install the pre-requisites depending on whether you are windows or Linux/Mac user


2) Following steps are to install the pre-requisites 


***************************************************************************************

Install the following frameworks from the url given along with it / google for it

------------------------------------------------
framework Name : lxml 2.2.2 (32-bit)
url : http://pypi.python.org/pypi/lxml/2.2.2

-------------------------------------------------

framework Name : sqllite (32-bit)
url : http://www.sqlite.org/download.html

-----------------------------------------------


****************************************************************************************



3) To launch the crawler:
   3.1) Open the command prompt/shell and navigate to the path where you have extracted the zip file and type the following command
   3.2) python Launcher.py <url> <maxlinks> [max-links is optional]
        Eg 1: python Launcher.py http://python.org 50
	Eg 1: python Launcher.py http://python.org
   A file with list of links fetched will pop up once the specified number of links have been fecthed or when the user terminates the execution or when all the links has been exhausted
    


###########NOTE : MULTIPROCESSING IS NOT SUPPORTED######################

(i.e) if you execute Launcher.py from two command prompt/shell at the same time you won't get expected behaviour