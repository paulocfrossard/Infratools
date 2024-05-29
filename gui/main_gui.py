from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
                               QLayout, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QSizePolicy, QStatusBar, QWidget)
import self

from tools.recovery import os_recovery


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
        MainWindow.setWindowTitle(u"MainWindow")
        MainWindow.setAnimated(True)
        self.actionVersao = QAction(MainWindow)
        self.actionVersao.setObjectName(u"actionVersao")
        self.actionSobre = QAction(MainWindow)
        self.actionSobre.setObjectName(u"actionSobre")
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

        # 0 0 1 1 RECUPERAR
        self.label_recuperar = QLabel(self.centralwidget)
        self.label_recuperar.setObjectName(u"label_recuperar")
        self.gridLayout.addWidget(self.label_recuperar, 0, 0, 1, 1)

        self.pushButton_recuperar = QPushButton(self.centralwidget)
        self.pushButton_recuperar.setObjectName(u"pushButton_recuperar")
        self.gridLayout.addWidget(self.pushButton_recuperar, 1, 0, 1, 1)

        # 5 1 1 1 TESTE X
        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 5, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.gridLayout.addWidget(self.label_6, 4, 1, 1, 1)

        # 4 0 1 1 TESTE Y
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 5, 0, 1, 1)

        # 0 1 1 1 TESTE D
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 1)

        # 2 0 1 1 Teste C
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)

        #2 1 1 1 Teste B
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)

        # 6 1 1 1 Teste de inserção via python
        ## Criando Status SFC /scannow
        self.labelSfc = QLabel(self.centralwidget)
        self.labelSfc.setObjectName(u"labelSfc")
        self.gridLayout.addWidget(self.labelSfc, 6, 0, 1, 1)

        self.labelSfc_status = QLabel(self.centralwidget)
        self.labelSfc_status.setObjectName(u"labelSfc_status")
        self.gridLayout.addWidget(self.labelSfc_status, 6, 1, 1, 1)
        ## Criando Status chkdsk /F
        self.labelChkdsk = QLabel(self.centralwidget)
        self.labelChkdsk.setObjectName(u"labelChkdsk")
        self.gridLayout.addWidget(self.labelChkdsk, 6, 2, 1, 1)
        self.labelChkdsk_status = QLabel(self.centralwidget)
        self.labelChkdsk_status.setObjectName(u"labelChkdsk_status")
        self.gridLayout.addWidget(self.labelChkdsk_status, 6, 3, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 24))
        self.menuSobre = QMenu(self.menubar)
        self.menuSobre.setObjectName(u"menuSobre")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSobre.menuAction())
        self.menuSobre.addSeparator()
        self.menuSobre.addAction(self.actionVersao)
        self.menuSobre.addSeparator()
        self.menuSobre.addAction(self.actionSobre)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setStatusTip("")
        # Menu
        self.actionVersao.setText(QCoreApplication.translate("MainWindow", u"Versão", None))
        self.actionSobre.setText(QCoreApplication.translate("MainWindow", u"Sobre", None))
        self.menuSobre.setTitle(QCoreApplication.translate("MainWindow", u"Ajuda", None))

        # Recupera
        self.label_recuperar.setText(
            QCoreApplication.translate("MainWindow", u"Recuperar sistema (chkdsk, sfc, dism)", None))
        self.pushButton_recuperar.setText(QCoreApplication.translate("MainWindow", u"Recuperar", None))
        self.pushButton_recuperar.clicked.connect(self.recupera_gui)
        # Opcao 2
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"E", None))
        # Opcao 3
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"A", None))
        # Opcao 4
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"F", None))
        # Opcao 5
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"B", None))
        # Opcao 6
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"D", None))
        # 6 1 1 1 Teste de inserção via python
        self.labelSfc.setText(QCoreApplication.translate("MainWindow", u"Status SFC: ", None))
        self.labelChkdsk.setText(QCoreApplication.translate("MainWindow", u"Status CHKDSK: "))
        self.labelSfc_status.setText(QCoreApplication.translate("MainWindow", u"Não executado"))
        self.labelChkdsk_status.setText(QCoreApplication.translate("MainWindow", u"Não executado"))
    def recupera_gui(self):
        sfc, chkdsk = os_recovery()
        print(sfc, chkdsk)


app = QApplication([])
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()
app.exec()
