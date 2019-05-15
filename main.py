import sys
import client
import socket
import requests
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

nat0_ip = '10.0.0.4'
base_url = 'http://'+ nat0_ip +':8080/network/'
print(base_url)

def ip_to_host(ip):
    return 'h' + ip[-1]

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def on_query_button_clicked():
    print('query button was pressed!')
    extra_url = 'querypath'
    url = base_url + extra_url
    response = requests.get(url)
    print(response.text) # {"10.0.0.4-10.0.0.2": [[1]], "10.0.0.4-10.0.0.3": [[1, 2, 5], [1, 3, 4, 5]], "10.0.0.4-10.0.0.1": [[1]]}
    data_json = json.loads(response.text)
    print(data_json)
    ui.query_path_browser.setText('Available paths are as follows:')
    for ip_pair, paths in data_json.items():
        src_ip, dst_ip = ip_pair.split('-')
        src = ip_to_host(src_ip)
        dst = ip_to_host(dst_ip)
        ui.query_path_browser.append('--------------------' + src + '-->' + dst + ' ( IP Address: ' + dst_ip + ')' +
                                     '--------------------')
        for i, path in enumerate(paths):
            display_path = 'Path' + str(i+1) + ': ' + src + '-->'
            for switch_id in path:
                display_path += 's' + str(switch_id) + '-->'
            display_path += dst
            ui.query_path_browser.append(display_path)



app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = client.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

ui.query_button.clicked.connect(on_query_button_clicked)

# get current user ip
current_host_ip = get_host_ip()
print(current_host_ip)
ui.user.setAlignment(Qt.AlignLeft)
ui.user.setText(ip_to_host(current_host_ip) + ' ( IP Address: ' + current_host_ip + ')')
sys.exit(app.exec_())