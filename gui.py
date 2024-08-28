import configparser

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, QThreadPool, Slot)
from PySide6.QtGui import (QAction, QFont, QIcon)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel, QLayout, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QWidget)
import tools.recovery
from tools.get_ip import get_network_devices
from tools.network import ip_refresh


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 510)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(900, 510))
        MainWindow.setMaximumSize(QSize(900, 510))
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        MainWindow.setFont(font)
        MainWindow.setWindowTitle(u"InfraTools")
        MainWindow.setWindowIcon(QIcon(r"C:\Users\usuario\PycharmProjects\CAEd_gui_infra_tools\img\tech.ico"))
        MainWindow.setAnimated(True)
        self.action_version = QAction(MainWindow)
        self.action_version.setObjectName(u"actionVersao")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"actionSobre")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(900, 460))
        self.centralwidget.setMaximumSize(QSize(900, 460))
        self.centralwidget.setFont(font)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

        # Recovery Label
        self.label_recover = QLabel(self.centralwidget)
        self.label_recover.setObjectName(u"label_recuperar")
        self.gridLayout.addWidget(self.label_recover, 0, 0, 1, 3)

        self.pushButton_recover = QPushButton(self.centralwidget)
        self.pushButton_recover.setObjectName(u"pushButton_recuperar")
        self.gridLayout.addWidget(self.pushButton_recover, 1, 0, 1, 3)

        #self.label_4 = QLabel(self.centralwidget)
        #self.label_4.setObjectName(u"label_4")
        #self.gridLayout.addWidget(self.label_4, 2, 3, 1, 3)

        #self.pushButton_2 = QPushButton(self.centralwidget)
        #self.pushButton_2.setObjectName(u"pushButton_2")
        #self.gridLayout.addWidget(self.pushButton_2, 3, 3, 1, 3)

        # IP reset
        self.ip_reset_label = QLabel(self.centralwidget)
        self.ip_reset_label.setObjectName(u"ip_reset_label")
        self.gridLayout.addWidget(self.ip_reset_label, 2, 0, 1, 3)

        self.ip_reset = QPushButton(self.centralwidget)
        self.ip_reset.setObjectName(u"ip_reset")
        self.gridLayout.addWidget(self.ip_reset, 3, 0, 1, 3)

        # Recovery itens
        self.label_sfc = QLabel(self.centralwidget)
        self.label_sfc.setObjectName(u"labelSfc")
        self.gridLayout.addWidget(self.label_sfc, 6, 4, 1, 1)

        self.label_sfc_status = QLabel(self.centralwidget)
        self.label_sfc_status.setObjectName(u"labelSfc_status")
        self.gridLayout.addWidget(self.label_sfc_status, 6, 5, 1, 1)

        self.label_chkdsk = QLabel(self.centralwidget)
        self.label_chkdsk.setObjectName(u"labelChkdsk")
        self.gridLayout.addWidget(self.label_chkdsk, 6, 2, 1, 1)
        self.label_chkdsk_status = QLabel(self.centralwidget)
        self.label_chkdsk_status.setObjectName(u"labelChkdsk_status")
        self.gridLayout.addWidget(self.label_chkdsk_status, 6, 3, 1, 1)

        self.label_dism = QLabel(self.centralwidget)
        self.label_dism.setObjectName(u"labeldism")
        self.gridLayout.addWidget(self.label_dism, 6, 0, 1, 1)

        self.label_dism_status = QLabel(self.centralwidget)
        self.label_dism_status.setObjectName(u"labelSfc_status")
        self.gridLayout.addWidget(self.label_dism_status, 6, 1, 1, 1)

        # Local data
        self.label_ip = QLabel(self.centralwidget)
        self.label_ip.setObjectName(u"labelip")
        self.gridLayout.addWidget(self.label_ip, 7, 0, 1, 1)
        self.label_ping_data = QLabel(self.centralwidget)
        self.label_ping_data.setObjectName(u"labelpingdata")
        self.gridLayout.addWidget(self.label_ping_data, 7, 1, 1, 1)

        self.label_mac = QLabel(self.centralwidget)
        self.label_mac.setObjectName(u"labelmac")
        self.gridLayout.addWidget(self.label_mac, 7, 2, 1, 1)
        self.label_mac_data = QLabel(self.centralwidget)
        self.label_mac_data.setObjectName(u"labelmacdata")
        self.gridLayout.addWidget(self.label_mac_data, 7, 3, 1, 1)

        # Ping status
        self.ping_label = QLabel(self.centralwidget)
        self.ping_label.setObjectName(u"label_2")
        self.gridLayout.addWidget(self.ping_label, 0, 3, 1, 3)

        self.pushButton_ping = QPushButton(self.centralwidget)
        self.pushButton_ping.setObjectName(u"pushButton_ping")
        self.gridLayout.addWidget(self.pushButton_ping, 1, 3, 1, 3)

        self.label_ping_domain = QLabel(self.centralwidget)
        self.label_ping_domain.setObjectName(u"labelPingcaed")
        self.gridLayout.addWidget(self.label_ping_domain, 8, 0, 1, 1)

        self.label_ping_domain_status = QLabel(self.centralwidget)
        self.label_ping_domain_status.setObjectName(u"labelPing_status")
        self.gridLayout.addWidget(self.label_ping_domain_status, 8, 1, 1, 1)

        self.label_ping = QLabel(self.centralwidget)
        self.label_ping.setObjectName(u"labelChkdsk")
        self.gridLayout.addWidget(self.label_ping, 8, 2, 1, 1)

        self.label_ping_status_host_1 = QLabel(self.centralwidget)
        self.label_ping_status_host_1.setObjectName(u"labelChkdsk_status")
        self.gridLayout.addWidget(self.label_ping_status_host_1, 8, 3, 1, 1)

        self.label_ping_status_host_2 = QLabel(self.centralwidget)
        self.label_ping_status_host_2.setObjectName(u"labelChkdsk_status")
        self.gridLayout.addWidget(self.label_ping_status_host_2, 9, 3, 1, 1)

        self.label_ping_status_host_3 = QLabel(self.centralwidget)
        self.label_ping_status_host_3.setObjectName(u"labelChkdsk_status")
        self.gridLayout.addWidget(self.label_ping_status_host_3, 10, 3, 1, 1)

        ## Create Main
        self.horizontalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 24))
        self.menu_about = QMenu(self.menubar)
        self.menu_about.setObjectName(u"menuSobre")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_about.menuAction())
        self.menu_about.addSeparator()
        self.menu_about.addAction(self.action_version)
        self.menu_about.addSeparator()
        self.menu_about.addAction(self.action_about)
        self.thread_manager = QThreadPool()
        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi
    def retranslateUi(self, MainWindow):
        MainWindow.setStatusTip("")
        # Menu
        self.action_version.setText(QCoreApplication.translate("MainWindow", u"Versão", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"Sobre", None))
        self.menu_about.setTitle(QCoreApplication.translate("MainWindow", u"Ajuda", None))

        # Recovery
        self.label_recover.setText(
            QCoreApplication.translate("MainWindow", u"<b>Recuperar sistema:</b>", None))
        self.pushButton_recover.setText(QCoreApplication.translate("MainWindow", u"Realizar recuperação", None))
        self.pushButton_recover.clicked.connect(self.recovery_thread)

        # Ping
        self.ping_label.setText(QCoreApplication.translate("MainWindow", u"<b>Pingar servidores:</b>", None))
        self.pushButton_ping.setText(QCoreApplication.translate("MainWindow", u"Executar pings", None))
        self.pushButton_ping.clicked.connect(self.ping_thread)

        # Renew IP
        self.ip_reset_label.setText(QCoreApplication.translate("MainWindow", u"<b>Gerar novo IP:</b>", None))
        self.ip_reset.setText(QCoreApplication.translate("MainWindow", u"Atualizar IP", None))
        self.ip_reset.clicked.connect(self.renew_ip_thread)


        # Recovery Status

        self.label_dism.setText(QCoreApplication.translate("MainWindow", u"<b>Status DISM: </b>"))
        self.label_dism_status.setText(QCoreApplication.translate("MainWindow", u"Não executado"))

        self.label_chkdsk.setText(QCoreApplication.translate("MainWindow", u"<b>Status CHKDSK: </b>"))
        self.label_chkdsk_status.setText(QCoreApplication.translate("MainWindow", u"Não executado"))

        self.label_sfc.setText(QCoreApplication.translate("MainWindow", u"<b>Status SFC: </b>", None))
        self.label_sfc_status.setText(QCoreApplication.translate("MainWindow", u"Não executado"))

        # Dism and ip

        self.label_ip.setText(QCoreApplication.translate("MainWindow", u"<b>Meu ip atual:</b>"))
        self.label_ping_data.setText(QCoreApplication.translate("MainWindow", ip))

        self.label_mac.setText(QCoreApplication.translate("MainWindow", u"<b>MAC:</b>"))
        self.label_mac_data.setText(QCoreApplication.translate("MainWindow", mac))

        # 8 1 1 1 Estado da opcao de ping

        self.label_ping_domain.setText(QCoreApplication.translate("MainWindow", u"<b>Ping dominio: </b>", None))
        self.label_ping_domain_status.setText(QCoreApplication.translate("MainWindow", u"Não executado"))

        self.label_ping.setText(QCoreApplication.translate("MainWindow", u"<b>Ping servers:</b>"))
        self.label_ping_status_host_1.setText(QCoreApplication.translate("MainWindow", u"Não executado"))
        self.label_ping_status_host_2.setText(QCoreApplication.translate("MainWindow", u"Não executado"))
        self.label_ping_status_host_3.setText(QCoreApplication.translate("MainWindow", u"Não executado"))

    @Slot()
    def define_estado_em_execucao(self):
        self.label_sfc_status.setText(QCoreApplication.translate("MainWindow", u"Executando em segundo plano..."))
        self.label_chkdsk_status.setText(QCoreApplication.translate("MainWindow", u"Executando em segundo plano..."))

    # Usa thread_manager para não travar a gui
    # # Cria o metodo recupera
    @Slot()
    def recupera_os(self):
        sfc, chkdsk, dism_check, dism_restore = tools.recovery.os_recovery()
        print(f"sfc: {sfc[0]}, chkdsk: {chkdsk[0]}, dism_check: {dism_check[0]}, dism_restore: {dism_restore[0]}")

        #SFC
        if sfc > 0:
            self.label_sfc_status.setText(QCoreApplication.translate("MainWindow", u"ERRO"))
        elif sfc == 3:
            self.label_sfc_status.setText(QCoreApplication.translate("MainWindow", u"Necessário reinicializar"))
        else:
            self.label_sfc_status.setText(QCoreApplication.translate("MainWindow", u"Executado"))

        #CHKDSK
        if chkdsk == 3:
            self.label_chkdsk_status.setText(QCoreApplication.translate("MainWindow", u"Necessário reinicializar"))
        elif chkdsk > 0:
            self.label_chkdsk_status.setText(QCoreApplication.translate("MainWindow", u"ERRO"))
        else:
            self.label_chkdsk_status.setText(QCoreApplication.translate("MainWindow", u"Executado"))

        #DISM
        if dism_restore == 3:
            self.label_dism_status.setText(QCoreApplication.translate("MainWindow", u"Necessário reinicializar"))
        elif dism_restore > 0:
            self.label_dism_status.setText(QCoreApplication.translate("MainWindow", u"ERRO"))
        else:
            self.label_dism_status.setText(QCoreApplication.translate("MainWindow", u"Executado"))

    @Slot()
    def recovery_thread(self):
        self.thread_manager.start(self.define_estado_em_execucao)
        self.thread_manager.start(self.recupera_os)

    # # Cria metodo para pingar usando thread_manager
    @Slot()
    def ping(self):
        def status(return_servers, label):
            status_ip, ip = return_servers[0], return_servers[1]
            dado = status_ip[0]
            status_ip = int(dado[0])
            if status_ip == 0:
                label.setText(QCoreApplication.translate("MainWindow", u"" + ip + " contactado"))
            else:
                label.setText(QCoreApplication.translate("MainWindow", u"" + ip + " Erro ao contactar"))

        labels = [self.label_ping_status_host_1, self.label_ping_status_host_2, self.label_ping_status_host_3]
        status_server, domain_status = tools.network.ping_tools(ips, domain)

        x = 0
        for servers in status_server:
            status(servers, labels[x])
            x += 1

        if domain_status == 0:
            self.label_ping_domain_status.setText(QCoreApplication.translate("MainWindow", u"Servidor conectado!"))
        else:
            self.label_ping_domain_status.setText(QCoreApplication.translate("MainWindow", u"ERRO!"))

    @Slot()
    def ping_thread(self):
        self.thread_manager.start(self.ping)

    @Slot()
    def renew_ip_thread(self):
        self.thread_manager.start(self.renew_ip)

    @Slot()
    def renew_ip(self):
        renova = ip_refresh()


def load_config(file_ini):
    config = configparser.ConfigParser()
    config.read(file_ini)
    return config


config = load_config(r'.\config.ini')
ips = config['hosts']['ips'].split(',')
domain = config['domain']['name']
ip, mac = get_network_devices()

app = QApplication([])
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()
app.exec()
