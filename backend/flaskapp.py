from flask import Flask, render_template, request, json, url_for, send_file
# import ecks
import subprocess
import happybase
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret'


def to_string(data):
    return ''.join(chr(x) for x in bytearray(data))


def to_list(data):
    return data.strip('()').split(',')


@app.route('/')
def index():
    return render_template('table.html')


@app.route('api/v1/snmp', methods={'GET'})
def get_snmp():
    try:
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('snmp')
        row_key = str(datetime.now())[:16]
        conn.open()

        data = [data for (key, data) in table.scan(row_start=row_key)]
        conn.close()

        response = {}

        for x in data[-1]:
            key = to_string(x)
            value = to_string(data[-1][x])
            ip_addr = key.split(':')[0]
            if(ip_addr not in response.keys()):
                response[ip_addr] = []

            if(key.split(':')[1] == 'cpu'):
                tmp = to_list(value)
                response[ip_addr].append(tmp[0])
            elif(key.split(':')[1] == 'disk'):
                tmp = value.strip('[]').split('), ')
                tmp = to_list(tmp[0])
                # used physical space / total physical space *100
                perc = (float(tmp[3])/float(tmp[2]))*100
                response[ip_addr].append(perc)
            elif(key.split(':')[1] == 'memory'):
                tmp = to_list(value)
                # used swap space / total swap space *100
                perc = (float(tmp[1]) / float(tmp[0]))*100
                response[ip_addr].append(perc)
            elif(key.split(':')[1] == 'os'):
                tmp = value.split()[0]
                response[ip_addr].append(tmp)
            elif(key.split(':')[1] == 'upt'):
                response[ip_addr].append(value)

            # print(x, data[-1][x])
            # print('\n\n\n')
        '''
            Response format {ip_addr1: [cpu_data, dsk_data, mem_data, os, upt], ...}
        '''
        return json.dumps(response), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({}), 400, {'ContentType': 'application/json'}


@app.route('api/v1/ping', methods={'GET'})
def get_ping():
    try:
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('ping')
        row_key = str(datetime.now())[:16]
        conn.open()

        data = [data for (key, data) in table.scan(row_start=row_key)]
        conn.close()

        response = {}

        for x in data[-1]:
            key = to_string(x)
            value = to_string(data[-1][x])
            ip_addr = key.split(':')[0]
            if(ip_addr not in response.keys()):
                response[ip_addr] = ""

            if(key.split(':')[1] == 'ping'):
                response[ip_addr] = value

        '''
            Response format {<ip_addr>: "True" <or> "False", ...}
        '''
        return json.dumps(response), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({}), 400, {'ContentType': 'application/json'}


@app.route('api/v1/ssh', methods={'GET'})
def get_ssh():
    try:
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('ssh')
        row_key = str(datetime.now())[:16]
        conn.open()

        data = [data for (key, data) in table.scan(row_start=row_key)]
        conn.close()

        response = {}

        for x in data[-1]:
            key = to_string(x)
            value = to_string(data[-1][x])
            ip_addr = key.split(':')[0]
            if(ip_addr not in response.keys()):
                response[ip_addr] = []

            if(key.split(':')[1] == 'ssh'):
                response[ip_addr].append(value)
            # elif(key.split(':')[1] == 'last'):
                #todo

        '''
            Response format {<ip_addr>: ["True" <or> "False"], ...}
        '''
        return json.dumps(response), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({}), 400, {'ContentType': 'application/json'}


@app.route('/download')
def download():
    path = 'diskdata.txt'
    return send_file(path)


if __name__ == '__main__':
    app.run(debug=True)
