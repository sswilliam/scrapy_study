
#! /usr/bin/env python3
# -*- coding: utf-8 -*- 

import os
import json
import subprocess
import time
import sys
import URL as urlconfig
cnt = 0
# check all folder that doens't contains the finish.txt
# generate the finish.txt if all images are download
# download mising image and break the program to debug
for dirname in os.listdir("cache"):
    if dirname != '.' and dirname != '..' and dirname != '.DS_Store':
        detailed_json = "cache/"+dirname+"/detailed.json"
        basic_json = "cache/"+dirname+"/basicinfo.json"

        if not os.path.exists(detailed_json):
            print(dirname+" not  configured")
        else:
            # print(dirname)
            cnt = cnt+1
            if os.path.exists("cache/"+dirname+"/finish.txt"):
                continue
            with open(detailed_json) as f:
                detailed_info = json.load(f)
            # print(detailed_info['imgs'])
            for img in detailed_info['imgs']:
                # print(isinstance(img,unicode))
                # print(isinstance("cache",unicode))
                file_name = img.split("/")[-1]
                if not os.path.exists("cache/"+dirname+"/"+file_name):
                    print("cache/"+dirname)
                    print(img)
                    # exit("hello")
                    if img.find(urlconfig.image_former_url) != -1:
                        print(img)
                        img = img.replace(urlconfig.image_former_url,urlconfig.image_base_url,1)
                    print(img)
                    p = subprocess.Popen(["wget", img], cwd="cache/"+dirname)
                    p.wait()
                    exit("hello")
                    #
            print(str(cnt)+"  finished")
            with open("cache/"+dirname+"/finish.txt", 'wb') as f:
                f.write("finish".encode(encoding="utf-8"))
            