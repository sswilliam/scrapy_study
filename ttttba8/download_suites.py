
#! /usr/bin/env python3
# -*- coding: utf-8 -*- 

import os
import json
import subprocess
import time
import sys
cnt = 0
import URL as urlconfig
#donwload all images for the suite that doesnt contains the finish.txt
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
            for img in detailed_info['imgs']:
                file_name = img.split("/")[-1]
                if not os.path.exists("cache/"+dirname+"/"+file_name):
                    print("cache/"+dirname)
                    print(img)
                    if img.find(urlconfig.image_former_url) != -1:
                        print(img)
                        img = img.replace(urlconfig.image_former_url,urlconfig.image_base_url,1)
                    print(img)
                    p = subprocess.Popen(["wget", img], cwd="cache/"+dirname)
                    p.wait()
            print(str(cnt)+"  finished")
           
