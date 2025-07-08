# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(450, 350)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radio_12h = QRadioButton(self.groupBox)
        self.radio_12h.setObjectName(u"radio_12h")

        self.verticalLayout_2.addWidget(self.radio_12h)

        self.radio_24h = QRadioButton(self.groupBox)
        self.radio_24h.setObjectName(u"radio_24h")

        self.verticalLayout_2.addWidget(self.radio_24h)

        self.radio_custom = QRadioButton(self.groupBox)
        self.radio_custom.setObjectName(u"radio_custom")

        self.verticalLayout_2.addWidget(self.radio_custom)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.label_format_tip = QLabel(self.groupBox)
        self.label_format_tip.setObjectName(u"label_format_tip")
        self.label_format_tip.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_format_tip)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_status = QLabel(self.groupBox_2)
        self.label_status.setObjectName(u"label_status")

        self.verticalLayout_3.addWidget(self.label_status)

        self.label_current_format = QLabel(self.groupBox_2)
        self.label_current_format.setObjectName(u"label_current_format")

        self.verticalLayout_3.addWidget(self.label_current_format)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_confirm = QPushButton(self.centralwidget)
        self.btn_confirm.setObjectName(u"btn_confirm")

        self.horizontalLayout.addWidget(self.btn_confirm)

        self.btn_cancel = QPushButton(self.centralwidget)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.horizontalLayout.addWidget(self.btn_cancel)

        self.btn_restore = QPushButton(self.centralwidget)
        self.btn_restore.setObjectName(u"btn_restore")

        self.horizontalLayout.addWidget(self.btn_restore)

        self.btn_language = QPushButton(self.centralwidget)
        self.btn_language.setObjectName(u"btn_language")

        self.horizontalLayout.addWidget(self.btn_language)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u65f6\u95f4\u683c\u5f0f\u8bbe\u7f6e\u5de5\u5177", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u65f6\u95f4\u663e\u793a\u683c\u5f0f", None))
        self.radio_12h.setText(QCoreApplication.translate("MainWindow", u"12\u5c0f\u65f6\u5236 (\u4e0a\u5348/\u4e0b\u5348)", None))
        self.radio_24h.setText(QCoreApplication.translate("MainWindow", u"24\u5c0f\u65f6\u5236", None))
        self.radio_custom.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u683c\u5f0f", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u81ea\u5b9a\u4e49\u683c\u5f0f", None))
        self.label_format_tip.setText(QCoreApplication.translate("MainWindow", u"\u683c\u5f0f\u63d0\u793a: ", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u72b6\u6001", None))
        self.label_status.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u7cfb\u7edf: ", None))
        self.label_current_format.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u65f6\u95f4\u683c\u5f0f: ", None))
        self.btn_confirm.setText(QCoreApplication.translate("MainWindow", u"\u5e94\u7528\u8bbe\u7f6e", None))
        self.btn_cancel.setText(QCoreApplication.translate("MainWindow", u"\u53d6\u6d88", None))
        self.btn_restore.setText(QCoreApplication.translate("MainWindow", u"\u6062\u590d\u9ed8\u8ba4", None))
        self.btn_language.setText(QCoreApplication.translate("MainWindow", u"English", None))
    # retranslateUi

