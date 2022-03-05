import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QDialog, QDialogButtonBox, QVBoxLayout,
                             QLabel, QMessageBox, QFileDialog)
from creator.options import Ui_OptionsDialog
import json


CONFIG_PATH = os.path.join(os.getenv('APPDATA'), 'litel_osa', 'config.json')
DEFAULT = {'out_file': 'out.csv',
           'batch_size': 50,
           'spectra_path': './spectra',
           'wl_range': [1.5e-6, 1.6e-6],
           'mov_mean': 5,
           'graph_window': 100,
           'prominence': 5,
           'valley_width': 100}

# TODO adicionar opções:
# Amostras por passo - "samples_per_step"
# Amostras utilizadas (em %) - "use_samples"


class OptionsDialog(Ui_OptionsDialog, QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(628, 405)
        self.load()

        self.buttonBox.accepted.connect(self.save)
        self.reset_btn.clicked.connect(self.reset)
        self.browse_spectra.clicked.connect(self.browse_spectra_dialog)
        self.browse_out_file.clicked.connect(self.browse_out_file_dialog)

        self.setWindowTitle("Opções")

    def save(self):
        output = {'out_file': self.out_file.text(),
                  'batch_size': self.batch_size.value(),
                  'spectra_path': self.spectra_path.text(),
                  'wl_range': [self.wl_min.value() * 1e-6,
                               self.wl_max.value() * 1e-6],
                  'mov_mean': self.mov_mean.value(),
                  'graph_window': self.graph_window.value(),
                  'prominence': self.prominence.value(),
                  'valley_width': self.valley_width.value()}

        with open(CONFIG_PATH, 'w') as file:
            json.dump(output, file)

    def load(self):
        if not os.path.exists(CONFIG_PATH):
            config = DEFAULT
        else:
            with open(CONFIG_PATH, 'r') as file:
                config = json.load(file)

        self.out_file.setText(config['out_file'])
        self.batch_size.setValue(config['batch_size'])
        self.spectra_path.setText(config['spectra_path'])

        wl_range = config['wl_range']
        self.wl_min.setValue(wl_range[0]*1e6)
        self.wl_max.setValue(wl_range[1]*1e6)

        self.mov_mean.setValue(config['mov_mean'])
        self.graph_window.setValue(config['graph_window'])
        self.prominence.setValue(config['prominence'])
        self.valley_width.setValue(config['valley_width'])

    def reset(self):
        config = DEFAULT

        self.out_file.setText(config['out_file'])
        self.batch_size.setValue(config['batch_size'])
        self.spectra_path.setText(config['spectra_path'])

        wl_range = config['wl_range']
        self.wl_min.setValue(wl_range[0]*1e6)
        self.wl_max.setValue(wl_range[1]*1e6)

        self.mov_mean.setValue(config['mov_mean'])
        self.graph_window.setValue(config['graph_window'])
        self.prominence.setValue(config['prominence'])
        self.valley_width.setValue(config['valley_width'])

    def browse_spectra_dialog(self):
        file_dialog = QFileDialog(self)

        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)

        file_dialog.exec()
        self.spectra_path.setText(file_dialog.selectedFiles()[0])

    def browse_out_file_dialog(self):
        file_dialog = QFileDialog(self)

        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setNameFilter("CSV (*.csv)")

        file_dialog.exec()
        self.out_file.setText(file_dialog.selectedFiles()[0])

    def closeEvent(self, event):

        quit_msg = "Gostaria de salvar as mudanças?"
        buttons = QMessageBox.StandardButton.Save |\
                  QMessageBox.StandardButton.Discard

        reply = QMessageBox.question(self, 'Sair sem salvar',
                         quit_msg, buttons=buttons)

        if reply == QMessageBox.StandardButton.Save:
            self.save()
        event.accept()
