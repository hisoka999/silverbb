'''
Created on 07.01.2012

@author: stefan
'''
import subprocess
import os
def revision():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    svn_list = subprocess.Popen('svn info',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=repo_dir, universal_newlines=True)
    try:
        lst = svn_list.communicate()
        erg = lst[0].split('\n')[5].split(': ')[1]
    except Exception,e:
        print e
        print lst
        erg = ""
    return erg
revision()
sbb_version = '0.1'
sv_date = '$LastChangedDate: 2012-11-25 21:58:27 +0100 (So, 25. Nov 2012) $'