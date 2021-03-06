import sys
import os
import glob
import shutil
import urllib
import zipfile
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.build_py import build_py as _build

CLASSIFIERS = ["Development Status :: 5 - Production/Stable",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: BSD License",
               "Operating System :: MacOS",
               "Operating System :: POSIX :: Linux",
               "Operating System :: Microsoft :: Windows :: Windows 7",
               "Programming Language :: C++",
               "Programming Language :: Python :: 2 :: Only",
               "Topic :: Scientific/Engineering"]

# Description
description = "vmtk - The Vascular Modeling Toolkit"
fid = file('README', 'r')
long_description = fid.read()
fid.close()
idx = max(0, long_description.find("vmtk - The Vascular Modeling Toolkit"))
long_description = long_description[idx:]

NAME                = 'vmtk'
MAINTAINER          = "Simone Manini"
MAINTAINER_EMAIL    = "simone.manini@orobix.com"
DESCRIPTION         = description
LONG_DESCRIPTION    = long_description
URL                 = "https://github.com/vmtk/vmtk"
DOWNLOAD_URL        = "http://pypi.python.org/pypi/vmtk"
LICENSE             = "BSD"
CLASSIFIERS         = CLASSIFIERS
AUTHOR              = "Luca Antiga"
AUTHOR_EMAIL        = "luca.antiga@orobix.com"
PLATFORMS           = "Linux/MacOSX/Windows"
ISRELEASED          = True
VERSION             = '1.3'

def list_files(directory):
    '''A specialized version of os.walk() that list files only in the current directory
       and ignores files whose start with a leading period and cmake files.'''
    for root, dirs, files in os.walk(directory):
        if root == directory:
            return [x for x in files if not (x.startswith('.')) and not (x.endswith('cmake'))]

class vmtk_build_win_i386(_build):
    '''Build vmtk libraries'''

    def run(self):
        #finding absolute path
        VMTKPATH = "../../../vmtk-build-i386/Install"
        vmtk_path = os.path.abspath(VMTKPATH)

        shutil.copytree(os.path.join(vmtk_path,'lib','python2.7','site-packages','vmtk'), 'vmtk')
        shutil.copytree(os.path.join(vmtk_path,'lib','python2.7','site-packages','vtk'), os.path.join('vmtk','vtk'))
        shutil.copytree(os.path.join(vmtk_path,'lib'), os.path.join('vmtk','lib'), symlinks=True, ignore=shutil.ignore_patterns('cmake','python2.7'))
        shutil.copytree(os.path.join(vmtk_path,'bin'), os.path.join('vmtk','bin'))

        if sys.platform == "win32":
            #copy favicon
            shutil.copy(os.path.join(os.getcwd(),'vmtk-icon.ico'),os.path.join('vmtk','bin','vmtk-icon.ico'))
            #copy c++ dll files
            windows_architecture = 'i386'
            dll_zip = urllib.urlretrieve('https://s3.amazonaws.com/vmtk-installers/1.3/i386.zip','i386.zip')
            fh = open(dll_zip[0],'rb')
            z = zipfile.ZipFile(fh)
            z.extractall(os.path.join('vmtk','bin'))
            fh.close()
            os.remove(dll_zip[0])

class vmtk_build(_build):
    '''Build vmtk libraries'''

    def run(self):
        #finding absolute path
        VMTKPATH = "../../../vmtk-build/Install"
        vmtk_path = os.path.abspath(VMTKPATH)

        shutil.copytree(os.path.join(vmtk_path,'lib','python2.7','site-packages','vmtk'), 'vmtk')
        shutil.copytree(os.path.join(vmtk_path,'lib','python2.7','site-packages','vtk'), os.path.join('vmtk','vtk'))
        shutil.copytree(os.path.join(vmtk_path,'lib'), os.path.join('vmtk','lib'), symlinks=True, ignore=shutil.ignore_patterns('cmake','python2.7'))
        shutil.copytree(os.path.join(vmtk_path,'bin'), os.path.join('vmtk','bin'))

        if sys.platform == "win32":
            #copy favicon
            shutil.copy(os.path.join(os.getcwd(),'vmtk-icon.ico'),os.path.join('vmtk','bin','vmtk-icon.ico'))
            #copy c++ dll files
            dll_zip = urllib.urlretrieve('https://s3.amazonaws.com/vmtk-installers/1.3/x8664.zip','x8664.zip')
            fh = open(dll_zip[0],'rb')
            z = zipfile.ZipFile(fh)
            z.extractall(os.path.join('vmtk','bin'))
            fh.close()
            os.remove(dll_zip[0])

setup(name=NAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      classifiers=CLASSIFIERS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      platforms=PLATFORMS,
      version=VERSION,
      cmdclass={'vmtk_build':vmtk_build,'vmtk_build_win_i386':vmtk_build_win_i386},
      packages = find_packages(),
      zip_safe=False,
      package_data = {
         'vmtk': ["lib/*.so*","lib/*.*lib*","lib/*.pyd*","bin/*","*.pyd","*.so","vtk/*.pyd","vtk/*.so"],
         'vtk': ["lib/*.so*","lib/*.pyd*","*.pyd","*.so"],
        },
      scripts = ['vmtk_post_install.py']
    )
