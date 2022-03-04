import os

import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import QtCore
from creator.calibrate_2 import Ui_CalibrationWindow2
import json
from math import ceil
from Loader import FileLoader
import processing
from time import time
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


MODELS_PATH = os.path.join(os.getenv("APPDATA"), "litel_osa", "calibration")
LAST_MODEL = os.path.join(os.getenv("APPDATA"), "litel_osa", "last_calibrated.json")


class CalibrationWindow2(Ui_CalibrationWindow2, QDialog):
    update_trigger = QtCore.pyqtSignal()

    def __init__(self, calibration_model, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self.setWindowTitle("Calibração")

        self.calibration_model = calibration_model
        self.model_name.setText(calibration_model["name"])
        self.current_step = 0
        self.reset_info()

        # Parte do loader
        self.loader = FileLoader(self.entry_loaded, options["spectra_path"])
        self.loader.pause()

        # Carregando opções
        self.options = options
        self.n_samples = options.get("samples_per_step", 10)
        self.use_samples = ceil(self.n_samples * options.get("use_samples", 0.75))

        # outras inicializações
        self.update_trigger.connect(self.update_entry)
        self.spectra_info = pd.DataFrame()
        self.start_time = 0
        self.running = False

        # Mensagem de início
        dialog = QMessageBox(self)

        dialog.setWindowTitle("Calibração")
        dialog.setText(f"Pressione OK quando o sistema estiver pronto para "
                       f"iniciar a calibração.")

        dialog.setInformativeText(f"Primeiro passo: {self.parameter_text}  --  "
                                  f"{self.step_text}")

        dialog.exec()

        # Iniciando de fato o programa
        self.start_step()

    def reset_info(self):
        self.parameter.setText(self.parameter_text)
        self.step.setText(self.step_text)
        self.progressBar.setValue(0)

    @property
    def parameter_text(self):
        text = self.calibration_model["parameter"]
        text += ": "
        text += str(self.calibration_model["steps"][self.current_step])
        text += " "
        text += self.calibration_model["unit"]

        return text

    @property
    def step_text(self):
        text = "Passo: "
        text += str(self.current_step + 1)
        text += "/"
        text += str(len(self.calibration_model["steps"]))

        return text

    def finish_step(self):
        self.running = False
        self.loader.pause()

        if self.current_step == (len(self.calibration_model["steps"]) - 1):
            self.end_calibration()
            return

        self.next_step()

    @QtCore.pyqtSlot()
    def end_calibration(self):
        valleys = []
        values = []

        # Organizando os valores
        for i in range(len(self.calibration_model["steps"])):
            df = self.spectra_info.loc[self.spectra_info["step"] == i]

            # Com function=None no process, measurando é o vale ressonante 'principal'
            df = df.sort_values(by=["measurand"])

            median = self.n_samples//2
            df = df.iloc[median - self.use_samples//2:
                         median + ceil(self.use_samples/2)]

            valleys += list(df["measurand"])
            # len(df.index) deve ser igual a self.use_samples, mas assim garante se não for
            values += [self.calibration_model["steps"][i] for _ in df.index]

        valleys = np.array(valleys).reshape(-1, 1)

        regression = LinearRegression().fit(valleys, values)
        r2 = regression.score(valleys, values)

        predictions = regression.predict(valleys)
        mae = mean_absolute_error(values, predictions)
        rmse = mean_squared_error(values, predictions)**(1/2)

        # Salvando
        self.calibration_model["last_calibration"]["a"] = regression.coef_[0]
        self.calibration_model["last_calibration"]["b"] = regression.intercept_
        self.calibration_model["last_calibration"]["R2"] = r2
        self.calibration_model["last_calibration"]["MAE"] = mae
        self.calibration_model["last_calibration"]["RMSE"] = rmse

        path = os.path.join(MODELS_PATH, self.calibration_model["name"] + ".json")
        with open(path, "w") as file:
            json.dump(self.calibration_model, file)

        with open(LAST_MODEL, "w") as file:
            json.dump(self.calibration_model, file)

        # Mensagem de saída
        dialog = QMessageBox(self)

        dialog.setWindowTitle("Calibração concluída")
        dialog.setText(f"A calibração foi concluída. Pressione OK para "
                       f"fechar a janela.")
        dialog.setInformativeText(f"Métricas calculadas: \n"
                                  f"R2: {r2:.4e}\n"
                                  f"mae: {mae:.4e}\n"
                                  f"rmse: {rmse:.4e}\n")

        dialog.exec()
        self.close()

    @QtCore.pyqtSlot()
    def next_step(self):
        dialog = QMessageBox(self)

        dialog.setWindowTitle("Passo concluído")
        dialog.setText(f"Passo {self.current_step + 1} concluído. "
                       f"Pressione OK quando o sistema estiver pronto para o "
                       f"próximo passo. \n")

        self.current_step += 1
        dialog.setInformativeText(f"Próximo passo: {self.parameter_text}  --  "
                                  f"{self.step_text}")

        dialog.exec()
    
        self.reset_info()
        self.start_step()

    def start_step(self):
        self.running = True
        self.loader.resume()

    def entry_loaded(self, spectrum):
        if not self.running:
            return

        # Extraindo informações
        spectrum, info = processing.process(spectrum, self.options, function=None)
        info["time"] = time() - self.start_time
        info["step"] = self.current_step

        self.spectra_info = pd.concat([self.spectra_info, pd.DataFrame([info, ])], ignore_index=True)
        # self.spectra_info = processing.reorganize_valleys(self.spectra_info)

        self.update_trigger.emit()

    def update_entry(self):
        # Conferindo e atualiando a quantidade de amostras
        sub_df = self.spectra_info.loc[self.spectra_info["step"] == self.current_step]
        samples_taken = len(sub_df.index)

        self.progressBar.setValue(100*samples_taken//self.n_samples)

        if samples_taken >= self.n_samples:
            self.finish_step()