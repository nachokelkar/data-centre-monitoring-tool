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
    return ''.join( chr(x) for x in bytearray(data) )

def to_list(data):
    return data.strip('()').split(',')


@app.route('/')
def index():
    return render_template('table.html')

# @app.route('/scan')
# def pingscan():
#     ip_out = subprocess.check_output('ifconfig')
#     ip = ip_out.find('inet')
#     return render_template('scan.html')


# @app.route('/check', methods=['POST'])
# def check():
#     if request.method == 'POST':
#         result = request.get_json(force=True)
#         ip = str(result[0])

#         e = ecks.Ecks()
#         toflash = ''
#         tab = '&nbsp;&nbsp;&nbsp;&nbsp;'

#         ecksdiskdefs = {1: 'Other', 2: 'RAM', 3: 'Virtual Memory', 4: 'Fixed Disk', 5: 'Removable Disk',
#                         6: 'Floppy Disk', 7: 'Compact Disk', 8: 'RAM Disk', 9: 'Flash Memory', 10: 'Network Disk'}

#         uptime = str(e.get_data(ip, 'public', 'uptime'))
#         disk_data = e.get_data(ip, 'public', 'disk')
#         cpu_data = e.get_data(ip, 'public', 'cpu')

#         toflash += 'Uptime : ' + uptime + '<br>'
#         toflash += 'CPU Usage: <br>' + tab + 'User : ' + str(cpu_data[0]) + '%<br>' + tab + 'System : ' + str(
#             cpu_data[1]) + '%<br>' + tab + 'Idle : ' + str(cpu_data[2]) + '%<br>'
#         toflash += 'Disk : <br>' + tab
#         for i in disk_data:
#             toflash += ecksdiskdefs[i[0]] + '&nbsp;&nbsp;' + i[1] + ' : ' + str(
#                 i[2]/2**20) + 'MB TOTAL, ' + str(i[3]/2**20) + 'MB USED <br>' + tab

#         return json.dumps({'success': 'True', 'message': toflash}), 200, {'ContentType': 'application/json'}


@app.route('/test', methods={'GET'})
def test():
    try:
        conn = happybase.Connection('localhost', port=9090)
        table = conn.table('snmp')
        row_key = str(datetime.now())[:16]
        conn.open()

        # row = table.row(b'2020-04-08 18:03:13.832322')
        # print(row[b'127.0.0.1:upt'])
        # for (key, data) in table.scan(row_start=row_key):
        #     print(key, data)
        #     print()

        data = [data for (key, data) in table.scan(row_start=row_key)]
        conn.close()

        response = {}

        for x in data[-1]:
            key = to_string(x)
            value = to_string(data[-1][x])
            ip_addr = key.split(':')[0]
            if(ip_addr not in response.keys()):
                response[ip_addr] = []

        
            if(key.split(':')[1]== 'cpu'):
                tmp = to_list(value)
                response[ip_addr].append(tmp[0])
            elif(key.split(':')[1]== 'disk'):
                tmp = value.strip('[]').split('), ')
                tmp = to_list(tmp[0])
                #used physical space / total physical space *100
                perc = (float(tmp[3])/float(tmp[2]))*100
                response[ip_addr].append(perc)
            elif(key.split(':')[1]== 'memory'):
                tmp = to_list(value)
                #used swap space / total swap space *100
                perc = (float(tmp[1])/ float(tmp[0]))*100
                response[ip_addr].append(perc)
            elif(key.split(':')[1]== 'os'):
                tmp = value.split()[0]
                response[ip_addr].append(tmp)  
            elif(key.split(':')[1]== 'upt'):
                response[ip_addr].append(value)           


            # print(x, data[-1][x])
            # print('\n\n\n')
        '''
            Response format {ip_addr1: [cpu_data, dsk_data, mem_data, os, upt], ...}
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
