# Form implementation generated from reading ui file 'calibrate_1.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CalibrationWindow1(object):
    def setupUi(self, CalibrationWindow1):
        CalibrationWindow1.setObjectName("CalibrationWindow1")
        CalibrationWindow1.resize(529, 533)
        self.verticalLayout = QtWidgets.QVBoxLayout(CalibrationWindow1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.delete_model = QtWidgets.QPushButton(CalibrationWindow1)
        self.delete_model.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_model.sizePolicy().hasHeightForWidth())
        self.delete_model.setSizePolicy(sizePolicy)
        self.delete_model.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../assets/cross.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.delete_model.setIcon(icon)
        self.delete_model.setObjectName("delete_model")
        self.horizontalLayout.addWidget(self.delete_model)
        self.comboBox = QtWidgets.QComboBox(CalibrationWindow1)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.next = QtWidgets.QPushButton(CalibrationWindow1)
        self.next.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next.sizePolicy().hasHeightForWidth())
        self.next.setSizePolicy(sizePolicy)
        self.next.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../assets/arrow.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.next.setIcon(icon1)
        self.next.setObjectName("next")
        self.horizontalLayout.addWidget(self.next)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(CalibrationWindow1)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(CalibrationWindow1)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.parameter = QtWidgets.QLineEdit(CalibrationWindow1)
        self.parameter.setReadOnly(False)
        self.parameter.setObjectName("parameter")
        self.horizontalLayout_2.addWidget(self.parameter)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(CalibrationWindow1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.unit = QtWidgets.QLineEdit(CalibrationWindow1)
        self.unit.setText("")
        self.unit.setReadOnly(False)
        self.unit.setObjectName("unit")
        self.horizontalLayout_3.addWidget(self.unit)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.label_3 = QtWidgets.QLabel(CalibrationWindow1)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_11.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        spacerItem2 = QtWidgets.QSpacerItem(20, 382, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(CalibrationWindow1)
        QtCore.QMetaObject.connectSlotsByName(CalibrationWindow1)

    def retranslateUi(self, CalibrationWindow1):
        _translate = QtCore.QCoreApplication.translate
        CalibrationWindow1.setWindowTitle(_translate("CalibrationWindow1", "Dialog"))
        self.delete_model.setToolTip(_translate("CalibrationWindow1", "Deletar modelo de calibra????o"))
        self.delete_model.setStatusTip(_translate("CalibrationWindow1", "Deletar modelo de calibra????o"))
        self.comboBox.setPlaceholderText(_translate("CalibrationWindow1", "Selecione um modelo de calibra????o"))
        self.next.setToolTip(_translate("CalibrationWindow1", "Selecionar modelo"))
        self.next.setStatusTip(_translate("CalibrationWindow1", "Selecionar modelo"))
        self.label.setText(_translate("CalibrationWindow1", "Par??metro:"))
        self.label_2.setText(_translate("CalibrationWindow1", "Unidade:"))
        self.label_3.setText(_translate("CalibrationWindow1", "Passos"))
