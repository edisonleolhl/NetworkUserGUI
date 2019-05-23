# conding=utf-8
import os
import sys
import client
import socket
import requests
import json
from PyQt5.QtCore import Qt, QRegExp, QTimer
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLCDNumber

nat0_ip = '10.0.0.4'
access_table = {'10.0.0.1': 's1-eth1', '10.0.0.2': 's1-eth2', '10.0.0.3': 's5-eth1'}
max_bw = 25
base_url = 'http://' + nat0_ip + ':8080/network/'
print('base_url: ' + base_url)


def ip_to_host(ip):
    return 'h' + ip[-1]


def host_to_ip(host):
    return '10.0.0.' + host[-1]


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
    # if not click the query path button for the first time,
    # then delete all widges in 'choose_path_layout', 'query_delay_layout', 'query_bw_layout' and 'limit_bw_layout'
    if ui.query_bw_layout.count() > 0:
        for i in reversed(range(ui.choose_path_layout.count())):
            ui.choose_path_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.query_delay_layout.count())):
            ui.query_delay_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.query_bw_layout.count())):
            ui.query_bw_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.limit_bw_layout.count())):
            ui.limit_bw_layout.itemAt(i).widget().setParent(None)
        ui.timer.stop()
    ui.query_path_browser.setText('Available paths are as follows:')
    for i, item in enumerate(data_json.items()):
        ip_pair, paths = item
        src_ip, dst_ip = ip_pair.split('-')
        src = ip_to_host(src_ip)
        dst = ip_to_host(dst_ip)
        if dst == ui.dst_comboBox.currentText()[0:2]:  # if 'h3' == 'h3'
            print('current destination is ' + dst)
            ui.query_path_browser.append('--------------------' + src + '-->' + dst + ' ( IP Address: ' + dst_ip + ')' +
                                         '--------------------')
            # 'choose_path_layout' contains a label and a comboBox
            ui.choose_path_label = QtWidgets.QLabel(ui.widget)
            ui.choose_path_label.setObjectName("choose_path_label")
            ui.choose_path_label.setText(src + '-->' + dst)
            ui.choose_path_layout.setWidget(i, QtWidgets.QFormLayout.LabelRole, ui.choose_path_label)

            ui.choose_path_comboBox = QtWidgets.QComboBox(ui.widget)
            ui.choose_path_comboBox.setObjectName("choose_path_comboBox")
            ui.choose_path_layout.setWidget(i, QtWidgets.QFormLayout.FieldRole, ui.choose_path_comboBox)
            for i, path in enumerate(paths):
                display_path = src + '-->'
                for switch_id in path:
                    display_path += 's' + str(switch_id) + '-->'
                display_path += dst
                ui.query_path_browser.append('Path' + str(i + 1) + ': ' + display_path)
                ui.choose_path_comboBox.addItem(display_path)
            ui.choose_path_comboBox.activated[str].connect(on_choose_path_comboBox_activated)

            ui.timer = QTimer()
            ui.timer.timeout.connect(display_lcd)
            ui.timer.start(1000)

            # 'query_delay_layout' contains a delay_lcdNumber, a label and a button
            ui.delay_lcdNumber = QtWidgets.QLCDNumber(ui.widget)
            ui.delay_lcdNumber.setDigitCount(10)
            ui.delay_lcdNumber.setSegmentStyle(QLCDNumber.Flat)
            ui.delay_lcdNumber.setStyleSheet("font: bold; color: red;")
            ui.delay_lcdNumber.setObjectName("delay_lcdNumber")
            ui.query_delay_layout.addWidget(ui.delay_lcdNumber)
            ui.query_delay_unit_label = QtWidgets.QLabel(ui.widget)
            ui.query_delay_unit_label.setObjectName("query_delay_unit_label")
            ui.query_delay_unit_label.setText('s')
            ui.query_delay_unit_label.setAlignment(Qt.AlignCenter)
            ui.query_delay_layout.addWidget(ui.query_delay_unit_label)
            ui.query_delay_button = QtWidgets.QPushButton(ui.widget)
            ui.query_delay_button.setObjectName("query_delay_button")
            ui.query_delay_button.setText("Query !")
            ui.query_delay_layout.addWidget(ui.query_delay_button)
            ui.query_delay_button.clicked.connect(on_query_delay_button_clicked)

            # 'query_bw_layout' contains a bw_lcdNumber, a bw_unit_label and a query_remaining_bw_button
            ui.bw_lcdNumber = QtWidgets.QLCDNumber(ui.widget)
            ui.bw_lcdNumber.setDigitCount(10)
            ui.bw_lcdNumber.setSegmentStyle(QLCDNumber.Flat)
            ui.bw_lcdNumber.setStyleSheet("font: bold; color: red;")
            ui.bw_lcdNumber.setObjectName("bw_lcdNumber")
            ui.query_bw_layout.addWidget(ui.bw_lcdNumber)
            ui.query_bw_unit_label = QtWidgets.QLabel(ui.widget)
            ui.query_bw_unit_label.setObjectName("query_bw_unit_label")
            ui.query_bw_unit_label.setText('Mb/s')
            ui.query_bw_unit_label.setAlignment(Qt.AlignCenter)
            ui.query_bw_layout.addWidget(ui.query_bw_unit_label)
            ui.query_remaining_bw_button = QtWidgets.QPushButton(ui.widget)
            ui.query_remaining_bw_button.setObjectName("query_remaining_bw_button")
            ui.query_remaining_bw_button.setText("Query !")
            ui.query_bw_layout.addWidget(ui.query_remaining_bw_button)
            ui.query_remaining_bw_button.clicked.connect(on_query_remaining_bw_button_clicked)

            # 'limit_bw_layout' contains a limit_bw_edit, a limit_bw_unit_label and a limit_bw_button
            ui.limit_bw_edit = QtWidgets.QLineEdit(ui.widget)
            ui.limit_bw_edit.setText('0-9 only! 0 means no limitation!')
            ui.limit_bw_edit.setObjectName("limit_bw_edit")
            regex = QRegExp('^[0-9]$')  # only one digit number from 0 to 9, 0 means no qos limitation
            validator = QtGui.QRegExpValidator(regex)
            ui.limit_bw_edit.setValidator(validator)
            ui.limit_bw_layout.addWidget(ui.limit_bw_edit)
            ui.limit_bw_unit_label = QtWidgets.QLabel(ui.widget)
            ui.limit_bw_unit_label.setObjectName("limit_bw_unit_label")
            ui.limit_bw_layout.addWidget(ui.limit_bw_unit_label)
            ui.limit_bw_button = QtWidgets.QPushButton(ui.widget)
            ui.limit_bw_button.setObjectName("limit_bw_button")
            ui.limit_bw_button.setText("Limit !")
            ui.limit_bw_layout.addWidget(ui.limit_bw_button)
            ui.limit_bw_button.clicked.connect(on_limit_bw_button_clicked)
            break

def on_choose_path_comboBox_activated(text):
    print('Choose path success!\nCurrent path: ' + text)  # 'h1-->s1-->s3-->s4-->s5-->h3'
    dst_ip = host_to_ip(text[-2:])  # '10.0.0.3'
    print('dst_ip: ' + dst_ip)
    path = [int(x) for x in text.replace('s', '').split('-->')[1:-1]]  # '[1, 3, 4, 5]'
    path = str(path).replace(' ', '')  # remove blanks --> '[1,3,4,5]'
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
    # if not click the query path button for the first time,
    # then delete all widges in 'choose_path_layout', 'query_delay_layout', 'query_bw_layout' and 'limit_bw_layout'
    if ui.choose_path_label:
        for i in reversed(range(ui.choose_path_layout.count())):
            ui.choose_path_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.query_delay_layout.count())):
            ui.query_delay_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.query_bw_layout.count())):
            ui.query_bw_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(ui.limit_bw_layout.count())):
            ui.limit_bw_layout.itemAt(i).widget().setParent(None)
        ui.timer.stop()
    ui.query_path_browser.setText('')


def display_lcd():
    current_path_raw = ui.choose_path_comboBox.currentText()  # current_path_raw = 'h1-->s1-->h2'
    current_path = host_to_ip(current_path_raw[0:2]) + current_path_raw[2:-2] + host_to_ip(current_path_raw[-2:])

    extra_url = 'query-delay'
    url = base_url + extra_url
    payload = {"path": current_path}
    response = requests.post(url, data=json.dumps(payload))
    print(response.text)
    path_delay = json.loads(response.text)["path_delay"]
    ui.delay_lcdNumber.display(path_delay)

    extra_url = 'query-remaining-bandwidth'
    url = base_url + extra_url
    payload = {"path": current_path}
    response = requests.post(url, data=json.dumps(payload))
    print(response.text)
    free_bw = json.loads(response.text)["free_bw"]
    ui.bw_lcdNumber.display(free_bw)

def on_query_delay_button_clicked():
    print('query delay bw was pressed !')
    current_path_raw = ui.choose_path_comboBox.currentText()  # current_path_raw = 'h1-->s1-->h2'
    # print('current_path_raw: ' + current_path_raw)
    extra_url = 'query-delay'
    url = base_url + extra_url
    current_path = host_to_ip(current_path_raw[0:2]) + current_path_raw[2:-2] + host_to_ip(current_path_raw[-2:])
    print('current_path: ' + current_path)  # current_path = '10.0.0.1-->s1-->10.0.0.2
    payload = {"path": current_path}
    response = requests.post(url, data=json.dumps(payload))
    print(response.text)
    path_delay = json.loads(response.text)["path_delay"]
    ui.delay_lcdNumber.display(path_delay)


def on_query_remaining_bw_button_clicked():
    print('query remaining bw button was pressed !')
    current_path_raw = ui.choose_path_comboBox.currentText()  # current_path_raw = 'h1-->s1-->h2'
    # print('current_path_raw: ' + current_path_raw)
    extra_url = 'query-remaining-bandwidth'
    url = base_url + extra_url
    current_path = host_to_ip(current_path_raw[0:2]) + current_path_raw[2:-2] + host_to_ip(current_path_raw[-2:])
    print('current_path: ' + current_path)  # current_path = '10.0.0.1-->s1-->10.0.0.2
    payload = {"path": current_path}
    response = requests.post(url, data=json.dumps(payload))
    print(response.text)
    free_bw = json.loads(response.text)["free_bw"]
    ui.bw_lcdNumber.display(free_bw)


def on_limit_bw_button_clicked():
    print("limit bw button was pressed!")
    limit_bw = ui.limit_bw_edit.text()
    try:
        assert int(limit_bw)
        print('limit_bw: ' + limit_bw)
        limit_bw = int(limit_bw)
        # limit_bw = 0 means no qos limitation
        os.system('ovs-vsctl set interface ' + access_table[current_host_ip] + ' ingress_policing_rate=' + str(
            limit_bw * 1000))
        os.system('ovs-vsctl set interface ' + access_table[current_host_ip] + ' ingress_policing_burst=' + str(
            limit_bw * 100))
        msgBox = QMessageBox(QMessageBox.NoIcon, 'Dialog',
                             'Limit bandwidth success!\nCurrent max bandwidth : ' + str(limit_bw) + ' Mb/s')
        msgBox.exec()
    except Exception as e:
        msgBox = QMessageBox(QMessageBox.NoIcon, 'Error', 'Please input legal integer!!!\n'
                                                          'Legal integer includes from 0 to 9!\n'
                                                          '0 means no limitation, '
                                                          'you can submit 0 after limit max bandwidth '
                                                          'if you want to cancel the limitation')
        msgBox.exec()


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
print(
    response.text)  # {"10.0.0.4-10.0.0.2": [[1]], "10.0.0.4-10.0.0.3": [[1, 2, 5], [1, 3, 4, 5]], "10.0.0.4-10.0.0.1": [[1]]}
data_json = json.loads(response.text)
for i, item in enumerate(data_json.items()):
    ip_pair, paths = item
    ui.dst_comboBox.addItem('h' + str(ip_pair[-1]) + ' ( IP Address: ' + ip_pair.split('-')[-1] + ')')
ui.dst_comboBox.activated[str].connect(on_dst_comboBox_activated)
ui.query_path_button.setText('Query path to ' + ui.dst_comboBox.currentText() + ' !')

ui.query_path_button.clicked.connect(on_query_path_button_clicked)

MainWindow.show()
sys.exit(app.exec_())
