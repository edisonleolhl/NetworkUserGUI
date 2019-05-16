# conding=utf-8
import sys
import client
import socket
import requests
import json
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

nat0_ip = '10.0.0.4'
base_url = 'http://'+ nat0_ip +':8080/network/'
print('base_url: ' + base_url)

def ip_to_host(ip):
    return 'h' + ip[-1]

def host_to_ip(host):
    return '10.0.0.'+ host[-1]

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def on_query_path_button_clicked():
    print('query path button was pressed!')
    # disconnect signal, otherwise press button may invoke several events
    # ui.query_remaining_bw_button.clicked.disconnect(on_query_remaining_bw_button_clicked)
    # if not click the query path button for the first timet
    if ui.choose_path_label or ui.choose_path_comboBox:
        # delete all widges in choose path layou
        for i in reversed(range(ui.choose_path_formLayout.count())):
            ui.choose_path_formLayout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.bw_layout.count())):
            ui.bw_layout.itemAt(i).widget().setParent(None)

    ui.query_path_browser.setText('Available paths are as follows:')
    for i, item in enumerate(data_json.items()):
        ip_pair, paths = item
        src_ip, dst_ip = ip_pair.split('-')
        src = ip_to_host(src_ip)
        dst = ip_to_host(dst_ip)
        if dst == ui.dst_comboBox.currentText()[0:2]: # if 'h3' == 'h3'
            print('current destination is ' + dst)
            ui.query_path_browser.append('--------------------' + src + '-->' + dst + ' ( IP Address: ' + dst_ip + ')' +
                                         '--------------------')
            ui.choose_path_label = QtWidgets.QLabel(ui.widget)
            ui.choose_path_label.setObjectName("choose_path_label")
            ui.choose_path_label.setText(src + '-->' + dst )
            ui.choose_path_formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, ui.choose_path_label)

            ui.choose_path_comboBox = QtWidgets.QComboBox(ui.widget)
            ui.choose_path_comboBox.setObjectName("choose_path_comboBox")
            ui.choose_path_formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, ui.choose_path_comboBox)
            for i, path in enumerate(paths):
                display_path = src + '-->'
                for switch_id in path:
                    display_path += 's' + str(switch_id) + '-->'
                display_path += dst
                ui.query_path_browser.append('Path' + str(i+1) + ': ' + display_path)
                ui.choose_path_comboBox.addItem(display_path)
            ui.choose_path_comboBox.activated[str].connect(on_choose_path_comboBox_activated)

            ui.lcdNumber = QtWidgets.QLCDNumber(ui.widget)
            ui.lcdNumber.setObjectName("lcdNumber")
            ui.bw_layout.addWidget(ui.lcdNumber)
            ui.unit_label = QtWidgets.QLabel(ui.widget)
            ui.unit_label.setObjectName("unit_label")
            ui.unit_label.setText('Mb/s')
            ui.unit_label.setAlignment(Qt.AlignCenter)
            ui.bw_layout.addWidget(ui.unit_label)
            ui.query_remaining_bw_button = QtWidgets.QPushButton(ui.widget)
            ui.query_remaining_bw_button.setObjectName("query_remaining_bw_button")
            ui.query_remaining_bw_button.setText("Query !")
            ui.bw_layout.addWidget(ui.query_remaining_bw_button)

            ui.query_remaining_bw_button.clicked.connect(on_query_remaining_bw_button_clicked)
            break

def on_choose_path_comboBox_activated(text):
    print('Choose path success!\nCurrent path: ' + text) # 'h1-->s1-->s3-->s4-->s5-->h3'
    dst_ip = host_to_ip(text[-2:]) # '10.0.0.3'
    print('dst_ip: ' + dst_ip)
    path = [int(x) for x in text.replace('s','').split('-->')[1:-1]] # '[1, 3, 4, 5]'
    path = str(path).replace(' ', '') # remove blanks --> '[1,3,4,5]'
    extra_url = 'choosepath'
    url = base_url + extra_url
    payload = {"dst_ip": dst_ip, "path": path}
    response = requests.put(url, data=json.dumps(payload))
    print(response.content)
    msgBox = QMessageBox(QMessageBox.NoIcon, 'Dialog', 'Choose path success!\nCurrent path: ' + text)
    msgBox.exec()

def on_dst_comboBox_activated(text):
    print('Choose destination success!\nCurrent destination: ' + text)
    msgBox = QMessageBox(QMessageBox.NoIcon, 'Dialog', 'Choose destination success!\nCurrent destination: ' + text)
    msgBox.exec()
    ui.query_path_button.setText('Query path to ' + text + ' !')
    # if not click the query path button for the first time, then delete all widges in choose path layout
    if ui.choose_path_label or ui.choose_path_comboBox:
        for i in reversed(range(ui.choose_path_formLayout.count())):
            ui.choose_path_formLayout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.bw_layout.count())):
            ui.bw_layout.itemAt(i).widget().setParent(None)
    ui.query_path_browser.setText('')


def on_query_remaining_bw_button_clicked():
    print('query remaining bw button was presed !')
    current_path_raw = ui.choose_path_comboBox.currentText() # current_path_raw = 'h1-->s1-->h2'
    # print('current_path_raw: ' + current_path_raw)
    extra_url = 'query-remaining-bandwidth'
    url = base_url + extra_url
    current_path = host_to_ip(current_path_raw[0:2]) + current_path_raw[2:-2] + host_to_ip(current_path_raw[-2:])
    print('current_path: ' + current_path) # current_path = '10.0.0.1-->s1-->10.0.0.2
    payload = {"path": current_path}
    response = requests.post(url, data=json.dumps(payload))
    print(response.text)
    free_bw = json.loads(response.text)["free_bw"]
    ui.lcdNumber.display(free_bw)

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = client.Ui_MainWindow()
ui.setupUi(MainWindow)


# get current user ip
current_host_ip = get_host_ip()
print('current_host_ip : ' + current_host_ip)
ui.user.setAlignment(Qt.AlignLeft)
ui.user.setText(ip_to_host(current_host_ip) + ' ( IP Address: ' + current_host_ip + ')')

extra_url = 'querypath'
url = base_url + extra_url
response = requests.get(url)
print(response.text)  # {"10.0.0.4-10.0.0.2": [[1]], "10.0.0.4-10.0.0.3": [[1, 2, 5], [1, 3, 4, 5]], "10.0.0.4-10.0.0.1": [[1]]}
data_json = json.loads(response.text)
for i, item in enumerate(data_json.items()):
    ip_pair, paths = item
    ui.dst_comboBox.addItem('h' + str(ip_pair[-1]) + ' ( IP Address: ' + ip_pair.split('-')[-1] + ')')
ui.dst_comboBox.activated[str].connect(on_dst_comboBox_activated)
ui.query_path_button.setText('Query path to ' + ui.dst_comboBox.currentText() + ' !')


ui.query_path_button.clicked.connect(on_query_path_button_clicked)


MainWindow.show()
sys.exit(app.exec_())