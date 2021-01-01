#!/usr/bin/env python3
import os
import zipfile
import glob
import os.path as path
import logging

files_to_exclude  = ['.chalice', 'app.py', '.DS_Store', 'package', '.git', '.gitignore', 'venv', 'env', 'vendor', 'requirements.txt','__pycache__',os.path.basename(__file__)]
cwd = os.getcwd()
package_folder = os.getenv('pacakge_folder', 'package')
deployment_zip = os.getenv('deployment_zip', 'deployment.zip')
package_location = path.join(cwd, package_folder, deployment_zip)
files = set(glob.glob('**')) - set(glob.glob('**__pycache__/**')) - set("vendor/**")
s = set(files_to_exclude)
files_to_add = list((x for x in files if x not in s))

with zipfile.ZipFile(package_location, 'a') as zipf:
    for _file in files_to_add:
        if(path.isfile(_file) and not path.islink(_file) and not path.splitext(_file)[1] == '.pyc'):
            zipf.write(path.join(cwd, _file), _file)
        elif (path.isdir(_file) and not path.islink(_file)):
            for folder, subfolders, file_names in os.walk(path.join(cwd, _file)):
                for file_name in file_names:
                    if (not path.splitext(file_name)[1] == '.pyc'):
                        file_path = path.join(folder, file_name)
                        files_to_add.append(path.join(_file, file_name))
                        print("Adding {} to following path {}".format(file_path, path.join(_file, file_name)))
                        zipf.write(file_path, path.join(_file, file_name) )


#with zipfile.ZipFile(package_location, 'a') as zipf:
    print ("Adding Files to Zip")
    #[zipf.write(path.join(cwd, f), f, zipfile.ZIP_DEFLATED) for f in files_to_add]

print("Added following files to zip {}".format(files_to_add))
