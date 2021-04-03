# conding=utf-8
import os
import sys
import client
import socket
import requests
import json
from PyQt5.QtCore import Qt, QRegExp, QTimer
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLCDNumber, QHBoxLayout

nat0_ip = '10.0.0.4'  # hard code for nat0
access_table = {'10.0.0.1': 's1-eth1', '10.0.0.2': 's1-eth2', '10.0.0.3': 's5-eth1'} # hard code for sw5host3 topo
base_url = 'http://' + nat0_ip + ':8080/network/'
print('base_url: ' + base_url)


# transfer ip to host
# input: ip address, eg: '10.0.0.3'
# output: host name, eg: 'h3'
def ip_to_host(ip):
    return 'h' + ip[-1]

# transfer host to ip
# input: host name, eg: 'h3'
# output: ip address, eg: '10.0.0.3'
def host_to_ip(host):
    return '10.0.0.' + host[-1]

# get current user ip
# output: ip address, eg: '10.0.0.3'
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def init_display():
    # for user GUI
    for i, item in enumerate(data_json.items()):
        ip_pair, paths = item
        print("ip_pair: %s, paths: %s" % (ip_pair, paths))
        if ip_pair[-1] == '3':  # hard code for destination host h3
            for j, path in enumerate(paths):
                # add layout
                ui.user_path_horizontal_layout = QtWidgets.QHBoxLayout()
                ui.user_path_horizontal_layout.setObjectName("user_path_horizontal_layout" + str(j))
                ui.user_path_vertical_layout.addLayout(ui.user_path_horizontal_layout)

                hor_layout = ui.user_path_vertical_layout.findChild(QHBoxLayout, "user_path_horizontal_layout" + str(j))

                ui.user_path_delay_label = QtWidgets.QLabel(ui.widget)
                ui.user_path_delay_label.setObjectName("user_path_delay_label" + str(j))
                ui.user_path_delay_label.setText("Plan " + str(j) + " --> Delay: ")
                hor_layout.addWidget(ui.user_path_delay_label)

                ui.user_path_delay_lcdNumber = QtWidgets.QLCDNumber(ui.widget)
                ui.user_path_delay_lcdNumber.setObjectName("user_path_delay_lcdNumber" + str(j))
                user_path_delay_lcdNumber_list.append(ui.user_path_delay_lcdNumber)
                hor_layout.addWidget(ui.user_path_delay_lcdNumber)

                ui.user_path_delay_unit_label = QtWidgets.QLabel(ui.widget)
                ui.user_path_delay_unit_label.setObjectName("user_path_delay_unit_label" + str(j))
                ui.user_path_delay_unit_label.setText("s")
                hor_layout.addWidget(ui.user_path_delay_unit_label)

                ui.user_path_free_bw_label = QtWidgets.QLabel(ui.widget)
                ui.user_path_free_bw_label.setObjectName("user_path_free_bw_label" + str(j))
                ui.user_path_free_bw_label.setText("Free bandwidth: ")
                hor_layout.addWidget(ui.user_path_free_bw_label)

                ui.user_path_free_bw_lcdNumber = QtWidgets.QLCDNumber(ui.widget)
                ui.user_path_free_bw_lcdNumber.setObjectName("user_path_free_bw_lcdNumber" + str(j))
                user_path_free_bw_lcdNumber_list.append(ui.user_path_free_bw_lcdNumber)
                hor_layout.addWidget(ui.user_path_free_bw_lcdNumber)

                ui.user_path_free_bw_unit_label = QtWidgets.QLabel(ui.widget)
                ui.user_path_free_bw_unit_label.setObjectName("user_path_free_bw_unit_label" + str(j))
                ui.user_path_free_bw_unit_label.setText("Mb")
                hor_layout.addWidget(ui.user_path_free_bw_unit_label)

                ui.user_path_unit_price_label = QtWidgets.QLabel(ui.widget)
                ui.user_path_unit_price_label.setObjectName("user_path_unit_price_label" + str(j))
                ui.user_path_unit_price_label.setText("Unit price: ")
                hor_layout.addWidget(ui.user_path_unit_price_label)

                ui.user_path_unit_price_lcdNumber = QtWidgets.QLCDNumber(ui.widget)
                ui.user_path_unit_price_lcdNumber.setObjectName("user_path_unit_price_lcdNumber" + str(j))
                user_path_unit_price_lcdNumber_list.append(ui.user_path_unit_price_lcdNumber)
                hor_layout.addWidget(ui.user_path_unit_price_lcdNumber)

                ui.user_path_unit_price_unit_label = QtWidgets.QLabel(ui.widget)
                ui.user_path_unit_price_unit_label.setObjectName("user_path_unit_price_unit_label" + str(j))
                ui.user_path_unit_price_unit_label.setText("$/Mb")
                hor_layout.addWidget(ui.user_path_unit_price_unit_label)

                ui.charging_plan_comboBox.addItem("Plan " + str(j))
            ui.charging_plan_comboBox.activated[str].connect(on_charging_plan_comboBox_activated)
            break

def display_user_lcd():
    for i, item in enumerate(data_json.items()):
        ip_pair, paths = item
        if ip_pair[-1] == '3':  # hard code
            for j, path in enumerate(paths):
                path = [str(x) for x in path]
                path = "-->".join(path)
                path = 's' + path  # 's1-->s2-->s5'
                current_path = current_host_ip + "-->" + path + "-->" + "10.0.0.3"

                extra_url = 'query-delay'
                url = base_url + extra_url
                payload = {"path": current_path}
                response = requests.post(url, data=json.dumps(payload))  # {"path":"10.0.0.1-->s1-->s2-->s5-->10.0.0.3"}
                print(response.text)
                path_delay = json.loads(response.text)["path_delay"]
                delay_lcdNumber = user_path_delay_lcdNumber_list[j]
                delay_lcdNumber.display(path_delay)
                delay_factor = max(0.5, min(1/path_delay, 5))

                extra_url = 'query-remaining-bandwidth'
                url = base_url + extra_url
                payload = {"path": current_path}
                response = requests.post(url, data=json.dumps(payload))
                print(response.text)
                free_bw = json.loads(response.text)["free_bw"]
                free_bw_lcdNumber = user_path_free_bw_lcdNumber_list[j]
                free_bw_lcdNumber.display(free_bw)
                free_bw_factor = max(0.5, min(5/(free_bw * 0.1), 5)) if free_bw != 0 else 5

                unit_price = int(delay_factor + free_bw_factor)
                user_path_unit_price_lcdNumber_list[j].display(unit_price)

            # update total display
            index = int(ui.charging_plan_comboBox.currentText()[-1])
            unit_price = int(user_path_unit_price_lcdNumber_list[index].value())
            if len(ui.user_want_bandwidth_edit.text()) > 0:
                want_bw = int(ui.user_want_bandwidth_edit.text())
            else:
                want_bw = 0
            ui.total_lcdNumber.display(want_bw * unit_price)
            break

def on_charging_plan_comboBox_activated():
    index = int(ui.charging_plan_comboBox.currentText()[-1])
    for i, item in enumerate(data_json.items()):
        ip_pair, paths = item
        print("ip_pair: %s, paths: %s" % (ip_pair, paths))
        if ip_pair[-1] == '3': # hard code
            path = str(paths[index])
            break
    print("path: " + path)  # eg: path = "[1,3,4,5]"
    dst_ip = '10.0.0.3' # hard code
    extra_url = 'choosepath'
    url = base_url + extra_url
    payload = {"dst_ip": dst_ip, "path": path} # {"dst_ip":"10.0.0.3", "path":"[1,3,4,5]"}
    response = requests.put(url, data=json.dumps(payload))
    print(response.content)
    if response.status_code == 200:
        msgBox = QMessageBox(QMessageBox.NoIcon, 'Dialog', 'Choose path success!\nCurrent path: ' + str(path))
        msgBox.exec()
    else:
        msgBox = QMessageBox(QMessageBox.NoIcon, 'Dialog', 'Choose path error!\nPlease check display!')
        msgBox.exec()
    print("user want bandwidth: " + ui.user_want_bandwidth_edit.text())
    want_bw = int(ui.user_want_bandwidth_edit.text())

    print("user choose charging plan: " + ui.charging_plan_comboBox.currentText())
    index = int(ui.charging_plan_comboBox.currentText()[-1])
    unit_price = int(user_path_unit_price_lcdNumber_list[index].value())

    ui.total_lcdNumber.display(want_bw*unit_price)

def on_user_want_bandwidth_edit_textChanged():
    print("user want bandwidth: " + ui.user_want_bandwidth_edit.text())
    if len(ui.user_want_bandwidth_edit.text()) > 0:
        want_bw = int(ui.user_want_bandwidth_edit.text())
    else:
        want_bw = 0
    print("user choose charging plan: " + ui.charging_plan_comboBox.currentText())
    index = int(ui.charging_plan_comboBox.currentText()[-1])
    unit_price = int(user_path_unit_price_lcdNumber_list[index].value())

    ui.total_lcdNumber.display(want_bw*unit_price)

def on_user_want_button_clicked():
    want_bw = int(ui.user_want_bandwidth_edit.text())
    total_price = int(ui.total_lcdNumber.value())
    # want_bw = 0 means no qos limitation
    os.system('ovs-vsctl set interface ' + access_table[current_host_ip] + ' ingress_policing_rate=' + str(
        want_bw * 1000))
    os.system('ovs-vsctl set interface ' + access_table[current_host_ip] + ' ingress_policing_burst=' + str(
        100))
    if want_bw != 0:
        msgBox = QMessageBox(QMessageBox.NoIcon, 'Dialog',
                             'Want bandwidth success!\n'
                             'Current max bandwidth : ' + str(want_bw) + ' Mb/s\n'
                                                                         'Cost: ' + str(total_price) + '$')
        msgBox.exec()
    else:
        msgBox = QMessageBox(QMessageBox.NoIcon, 'Dialog',
                             'Cancel charging plan success!\n')
        msgBox.exec()

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = client.Ui_MainWindow()
ui.setupUi(MainWindow)

current_host_ip = get_host_ip()
ui.user.setText(ip_to_host(current_host_ip) + ' ( IP Address: ' + current_host_ip + ')')

extra_url = 'querypath'
url = base_url + extra_url
response = requests.get(url)
# data_json = {'10.0.0.4-10.0.0.2': [[1]], '10.0.0.4-10.0.0.1': [[1]], '10.0.0.4-10.0.0.3': [[1, 2, 5], [1, 3, 4, 5]]}
data_json = json.loads(response.text)

user_path_delay_lcdNumber_list = []
user_path_free_bw_lcdNumber_list = []
user_path_unit_price_lcdNumber_list = []
init_display()

ui.user_timer = QTimer()
ui.user_timer.timeout.connect(display_user_lcd)  # update display every 3 seconds
ui.user_timer.start(3000)

ui.user_want_bandwidth_edit.setText('0')
ui.user_want_bandwidth_edit.setObjectName("limit_bw_edit")
# regex = QRegExp('^[0-9]$')  # only one digit number from 0 to 9, 0 means reset to no qos limitation
# validator = QtGui.QRegExpValidator(regex)
# ui.user_want_bandwidth_edit.setValidator(validator)
ui.user_want_bandwidth_edit.textChanged.connect(on_user_want_bandwidth_edit_textChanged)

ui.user_want_button.clicked.connect(on_user_want_button_clicked)
MainWindow.show()
sys.exit(app.exec_())
