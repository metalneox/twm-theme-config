#!/usr/bin/env python
import requests
import sys
import json
import os
import subprocess

#Function check is json
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def config(json):
    #working

    name = os.popen("whoami").read().strip('\n')
    current_git = json['theme']['git']

    print("Installation of the theme "+json['theme']['title']+"\n")
    print("You want set configuration for user "+name+"?[Y/N]")

    risposta = input() 

    if(risposta == "y" or risposta == "yes" ):
        p1 = subprocess.Popen(["git","clone",current_git,"/tmp/twm-theme-config-tmp"])
        p1.wait()

        package = ' '.join(json['theme']['package'])
        community = ' '.join(json['theme']['community'])

        #installation package and community
        if(json['theme']['distro'] == "Arch"):
            p2  = subprocess.Popen("sudo pacman -S --noconfirm "+package, shell=True)
            p2.wait()
            p3  = subprocess.Popen("yay -S --noconfirm "+community, shell=True)
            p3.wait()

        #NOT TESTING
        #Requirement 3rd package repository
        if(json['theme']['distro'] == "Deb"):
            p2  = subprocess.Popen("sudo apt-get install -y "+package, shell=True)
            p2.wait()
            p3  = subprocess.Popen("sudo apt-get install -y "+community, shell=True)
            p3.wait()

 #        p4  = subprocess.Popen("rm -rf ~/.* ", shell=True)
 #        p4.wait()
 #
 #        p5  = subprocess.Popen("cp -rT /tmp/twm-theme-config-tmp ~/. ", shell=True)
 #        p5.wait()
 #
 #        p6  = subprocess.Popen("rm -rf /tmp/twm-theme-config-tmp", shell=True)
 #        p6.wait()

#List theme from restful api 
def list():
    try:
        r = requests.get('http://127.0.0.1:5000/api/v1.0/list/')
        if(is_json(r.text)):
            data = r.json()
            print("ID NAME")
            for i in range(len(data)):
                print(str(data[i]['id'])+"  "+data[i]['title'])
        else:
            print("I cant parse json")
    except  requests.exceptions.RequestException as e:
        print("Server offline")
        sys.exit(1)

def theme(number):

    #TODO check number is number
    r = requests.get('http://127.0.0.1:5000/api/v1.0/themes/'+number)

    if(is_json(r.text)):
        data = r.json()
        config(data)
    else:
        print("I can't parse json")

def intro():
    print("***********************************************************")
    print("    Script for install themes of twm"                       )
    print("***********************************************************")
    print("\n")

def localjson(filename):
    file = open(filename, "r")
    data_local = file.read()
    if(is_json(data_local)):
        currentjson = json.loads(data_local)
        config(currentjson)
    else:
        print("I can't parse json")

def generate():
    print("Under Construction")

def help():
    print("--help                           Display this help          ")
    print("--localjson                      Load theme from local file ")
    print("--theme                          Set theme                  ")
    print("--list                           List theme available       ")
    print("--generate                       Generate json config       ")


if((len(sys.argv)) < 2):
    intro()
    help()
else:
    intro()

    if(sys.argv[1] == "--localjson"):
        if((len(sys.argv)) < 3): 
            print("Miss argument for setting theme\n")
            print("./twm-theme-config.py --localjson file")
        else:
            localjson(sys.argv[2])
        
    if(sys.argv[1] == "--theme"):
        if((len(sys.argv)) < 3): 
            print("Miss argument for setting theme\n")
            print("./twm-theme-config.py --theme ID_Theme ")
        else:
            theme(sys.argv[2])

    if(sys.argv[1] == "--list"):
        list()
    if(sys.argv[1] == "--generate"):
        generate()
    if(sys.argv[1] == "--help"):
        help()

    
