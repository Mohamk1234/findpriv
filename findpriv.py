#!/usr/bin/env python3
import argparse
import os
import stat
import subprocess

parser = argparse.ArgumentParser(
                    prog = 'findpriv')

parser.add_argument('-p','--path')
parser.add_argument('-c', '--capabilities', action='store_true')
parser.add_argument('-s', '--setuid', action='store_true')

args = parser.parse_args()

pathtoscan = '/'
executables = 0
suid_enabled= []
no_of_file_scanned = 0
capabilities_enabled = []


def find_setuid(file_being_checked):
    if os.stat(file_being_checked).st_mode & stat.S_ISUID:
                suid_enabled.append(file_being_checked)
    
def find_capabilites(file_being_checked):
    out = subprocess.run(['getcap',file_being_checked],capture_output=True, universal_newlines=True).stdout
    if out != '':
        capabilities_enabled.append(out)

def print_setuid():
    print('\nsetuid executables:\n')
    print(*suid_enabled, sep='\n')

def print_capabilities():
    print('\ncapability-aware executables:\n')
    print(*capabilities_enabled, sep='\n')

if args.path != None:
    pathtoscan = args.path

for root, dirs, files in os.walk(pathtoscan):
    for filename in files:
        no_of_file_scanned+=1
        file_being_checked = os.path.join(root, filename)
        if os.access(file_being_checked, os.X_OK):
            executables+=1
            if not(args.setuid ^ args.capabilities):
                find_setuid(file_being_checked)
                find_capabilites(file_being_checked)
            elif args.setuid:
                find_setuid(file_being_checked)
            else:
                find_capabilites(file_being_checked)
        
                


print('Total number of files scanned : ', no_of_file_scanned)
print('Number of executables found : ', executables)
if not(args.setuid ^ args.capabilities):
    print_setuid()
    print_capabilities()
          
elif args.setuid:
    print_setuid()
else:
    print_capabilities()




