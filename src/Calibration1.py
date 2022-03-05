import sys
import os
from PyQt6.QtWidgets import (QSpacerItem, QSizePolicy, QDoubleSpinBox,
                             QPushButton, QDialog, QInputDialog,
                             QLabel, QMessageBox, QFileDialog, QHBoxLayout)
from PyQt6.QtGui import QIcon
from creator.calibrate_1 import Ui_CalibrationWindow1
import json
from copy import deepcopy


MODELS_PATH = os.path.join(os.getenv('APPDATA'), 'litel_osa', 'calibration')


class StepText(QHBoxLayout):
    def __init__(self, index, value, icon, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spacer_left = QSpacerItem(8, 16, QSizePolicy.Policy.Fixed,
                                       QSizePolicy.Policy.Minimum)
        self.addItem(self.spacer_left)

        self.label = QLabel(parent)
        self.label.setText(f"{index+1}")
        self.addWidget(self.label)

        self.value = QDoubleSpinBox(parent)
        self.value.setValue(value)
        self.addWidget(self.value)

        self.delete_step_btn = QPushButton(parent)
        self.delete_step_btn.setEnabled(True)
        self.delete_step_btn.setText("")
        self.delete_step_btn.setIcon(icon)
        self.addWidget(self.delete_step_btn)

        self.spacer_right = QSpacerItem(8, 16, QSizePolicy.Policy.Fixed,
                                        QSizePolicy.Policy.Minimum)

        self.addItem(self.spacer_right)

    def delete(self):
        for i in reversed(range(self.count())):
            if not isinstance(self.itemAt(i), QSpacerItem):
                self.itemAt(i).widget().setParent(None)


class CalibrationWindow1(Ui_CalibrationWindow1, QDialog):
    NEW_MODEL = "++ <Criar novo modelo>"
    DEFAULT_MODEL = {"name": "",
                     "parameter": "",
                     "unit": "",
                     "steps": [],
                     "last_calibration": {"a": 1,
                                          "b": 0,
                                          "R2": -1,
                                          "MAE": -1,
                                          "RMSE": -1
                                          }
                     }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("Calibração")

        if not os.path.isdir(MODELS_PATH):
            os.mkdir(MODELS_PATH)

        self.options = []
        self.reset_options()
        self.last_option = self.options[0]
        self._current_option = self.DEFAULT_MODEL

        self.parameter.textChanged.connect(self.update_parameter)
        self.unit.textChanged.connect(self.update_unit)
        self.delete_model.clicked.connect(self.delete_current)
        self.next.clicked.connect(self.next_clicked)

        self.new_step_btn = QPushButton(self)
        self.new_step_btn.setEnabled(True)
        self.new_step_btn.setText("")
        self.new_step_btn.setIcon(QIcon("../assets/plus.png"))
        self.new_step_btn.clicked.connect(self.create_step)
        self.new_step_btn.hide()

        self.steps = []
        self.reset_steps()

        self.comboBox.currentTextChanged.connect(self.selected_option)

        # Esses botões não ficaram com os ícones bem configurados do .ui

        self.delete_model.setIcon(QIcon("../assets/cross.png"))
        self.next.setIcon(QIcon("../assets/arrow.png"))

        # Pro foco não começar no de deletar
        self.next.setFocus()

        # Para passar a informação de saída quando fechar
        self.close_reason = "close"

    def reset_options(self):
        self.options = [file[:-5] for file in os.listdir(MODELS_PATH)
                        if file[-5:] == ".json"] +\
                       [self.NEW_MODEL, ]
        self.comboBox.clear()
        for option in self.options:
            self.comboBox.addItem(option)

    # Callback de botão
    def selected_option(self):
        if self.comboBox.currentText() == self.NEW_MODEL:
            self.select_new_model()
            return

        if self.comboBox.currentText() == "":
            self.current_option = self.DEFAULT_MODEL
            self.clear_steps()
        else:
            filename = os.path.join(MODELS_PATH,
                                    f"{self.comboBox.currentText()}.json")

            with open(filename, "r") as file:
                self.current_option = json.load(file)

            self.reset_steps()

    @property
    def current_option(self):
        return self._current_option

    @current_option.setter
    def current_option(self, new_option):
        self.save_current()
        self._current_option = new_option

    @property
    def current_path(self):
        return os.path.join(MODELS_PATH, self.current_option["name"] + ".json")

    def select_new_model(self):
        while True:
            name, ok = QInputDialog.getText(self, 'Criar novo modelo',
                                            'Digite o nome do novo modelo:')
            if ok:
                if name in self.options:
                    continue

                model = deepcopy(self.DEFAULT_MODEL)
                model["name"] = name

                with open(os.path.join(MODELS_PATH, f"{name}.json"), 'x') as file:
                    json.dump(model, file)

            else:
                self.comboBox.setCurrentIndex(-1)

            break

        self.reset_options()
        self.comboBox.setCurrentText(name)

    def save_current(self):
        # Se n tem nome, n tem o q salvar
        if self.current_option["name"] == "":
            return -1
        # Se n existe, já foi deletado, n deve ser salvo
        if not os.path.exists(self.current_path):
            return -1

        with open(self.current_path, "w") as file:
            json.dump(self.current_option, file)

    def clear_steps(self):
        # parâmetro e unidade
        self.parameter.setText("")
        self.unit.setText("")

        # passos
        for step in self.steps:
            step.delete()
            self.gridLayout.removeItem(step)

        self.steps = []

        self.gridLayout.removeWidget(self.new_step_btn)

        self.new_step_btn.hide()

    def reset_steps(self):
        self.clear_steps()
        if self.current_option["name"] == "":
            return
        
        # parâmetro e unidade
        self.parameter.setText(self.current_option["parameter"])
        self.unit.setText(self.current_option["unit"])
        
        # passos
        icon = QIcon("../assets/cross.png")
        for c, step_value in enumerate(self.current_option["steps"]):
            new_step = StepText(c, step_value, icon, self)

            # O lambda dessa forma é para poder passar o valor, não a referência
            new_step.delete_step_btn.clicked.connect(lambda *, n=c: self.delete_step(n))
            new_step.value.valueChanged.connect(lambda *, n=c: self.update_step(n))

            self.steps.append(new_step)

            # Colunas com 7 linhas
            self.gridLayout.addLayout(new_step, c % 7, c // 7, 1, 1)

        n_steps = len(self.current_option["steps"])

        self.gridLayout.addWidget(self.new_step_btn, n_steps % 7,
                                  n_steps // 7, 1, 1)
        self.new_step_btn.show()

    def delete_current(self):
        if self.current_option["name"] == "" or \
                not os.path.exists(self.current_path):
            return

        os.remove(self.current_path)
        self.reset_options()

    # Callback de botão
    def create_step(self):
        self.current_option["steps"].append(0)
        self.reset_steps()

    # Callback de botão
    def delete_step(self, index):
        self.current_option["steps"].pop(index)
        self.reset_steps()

    # Callback de input
    def update_step(self, index):
        self.current_option["steps"][index] = self.steps[index].value.value()

    # Callback de input
    def update_parameter(self):
        self.current_option["parameter"] = self.parameter.text()

    # Callback de input
    def update_unit(self):
        self.current_option["unit"] = self.unit.text()

    # Callback de botão
    def next_clicked(self):
        if len(self.current_option["steps"]) == 0:
            dialog = QMessageBox(self)
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText("Erro")
            dialog.setInformativeText("Não pode passar para a próxima " +
                                      "fase sem passos no modelo")
            dialog.setWindowTitle("Erro")
            dialog.exec()
            return

        self.close_reason = "next"
        self.close()

    def closeEvent(self, event):
        self.save_current()
        event.accept()
