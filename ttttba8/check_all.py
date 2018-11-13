import os
import json
import subprocess
cnt = 0
#download all cover image for not finished suites
for dirname in os.listdir("cache"):
    if dirname != '.' and dirname != '..' and dirname != '.DS_Store':
        detailed_json = "cache/"+dirname+"/detailed.json"
        basic_json = "cache/"+dirname+"/basicinfo.json"

        if not os.path.exists(detailed_json):
            print(dirname+" not  configured")
        else:
            # if os.path.exists()
            if os.path.exist("cache/"+dirname+"/finish.txt"):
                continue
            with open(basic_json) as f:
                basic_info = json.load(f)
                if basic_info['cover']== None:
                    continue
                start_index = basic_info['cover'].index("src=")
                end_index = basic_info['cover'].find("&w=300")
                cover_url = basic_info['cover'][start_index+4:end_index]
                if os.path.exists("cache/"+dirname+"/cover.jpg"):
                    print("cache/"+dirname+"/cover.jpg")
                    cnt = cnt+1
                    # break
                else:
                    p = subprocess.Popen(["wget", cover_url,"-O", "cover.jpg"], cwd="cache/"+dirname)
                    p.wait()
                    print("not exist cover"+dirname)
print(str(cnt))