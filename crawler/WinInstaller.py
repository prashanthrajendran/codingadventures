import os
import shutil

if __name__ == '__main__':
    
    sqllitefile = 'packages\sqlite3.txt'
    lxmlfile = 'packages\lxml-2.2.2.win32-py3.0.txt'
    
    sqllitesetup = 'packages\sqlite3.dll'
    lxmlsetup = 'packages\lxml-2.2.2.win32-py3.0.exe'
    
    if os.path.isfile(sqllitefile):
        os.rename(sqllitefile,sqllitesetup)
    if os.path.isfile(lxmlfile):
        os.rename(lxmlfile,lxmlsetup)
    
    sqllitedestiantion = 'C:\Windows\System32\sqlite3.dll'
    
    if not os.path.isfile(sqllitedestiantion):
        if os.path.isfile(sqllitesetup):
            shutil.copy(sqllitesetup, sqllitedestiantion)
        else:
            print('sqllite dll is missing')
    
    if os.path.isfile(lxmlsetup):
        os.system(lxmlsetup)
    else:
        print('lxml installer missing')