from flask import Flask, render_template, request, json, url_for, send_file
import ecks
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
    return render_template("table.html")

# @app.route('/scan')
# def pingscan():
#     ip_out = subprocess.check_output("ifconfig")
#     ip = ip_out.find("inet")
#     return render_template("scan.html")

@app.route('/check', methods=["POST"])
def check():
    if request.method=="POST":
        result=request.get_json(force=True)
        ip = str(result[0])
        
        e = ecks.Ecks()
        toflash = ""
        tab = "&nbsp;&nbsp;&nbsp;&nbsp;"

        ecksdiskdefs = {1:"Other", 2:"RAM", 3:"Virtual Memory", 4:"Fixed Disk", 5:"Removable Disk", 6:"Floppy Disk", 7:"Compact Disk", 8:"RAM Disk", 9:"Flash Memory", 10:"Network Disk"}

        uptime = str(e.get_data(ip, 'public', 'uptime'))
        disk_data = e.get_data(ip, 'public', 'disk')
        cpu_data = e.get_data(ip, 'public', 'cpu')

        toflash += "Uptime : " +uptime +"<br>"
        toflash += "CPU Usage: <br>" +tab +"User : " +str(cpu_data[0]) +"%<br>" +tab +"System : " +str(cpu_data[1]) +"%<br>" +tab +"Idle : " +str(cpu_data[2]) +"%<br>"
        toflash += "Disk : <br>" +tab
        for i in disk_data:
            toflash += ecksdiskdefs[i[0]] +"&nbsp;&nbsp;" +i[1] +" : " +str(i[2]/2**20) +"MB TOTAL, " +str(i[3]/2**20) +"MB USED <br>" +tab

        return json.dumps({"success":"True", "message":toflash}),200,{'ContentType':'application/json'}
    
@app.route('/download')
def download():
    path = "diskdata.txt"
    return send_file(path)

if __name__ == '__main__':
    app.run(debug = True)