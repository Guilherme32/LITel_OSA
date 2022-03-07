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
from PlotWidget import PlotWidget


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

        # plot
        self.plot_widget = PlotWidget()
        self.verticalLayout.addWidget(self.plot_widget)
        self.plot_widget.refit()
        self.plot_widget.add_text_calibration()

        # Parte do loader
        self.loader = FileLoader(self.entry_loaded, options["spectra_path"])
        self.loader.pause()

        # Carregando opções
        self.options = options
        self.n_samples = options.get("samples_per_step", 10)

        # outras inicializações
        self.update_trigger.connect(self.update_entry)
        self.spectra_info = pd.DataFrame()
        self.start_time = time()
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

    @property
    def current_sub_df(self):
        return self.spectra_info.loc[self.spectra_info["step"] == self.current_step]

    def finish_step(self):
        self.running = False
        self.loader.pause()

        if self.current_step == (len(self.calibration_model["steps"]) - 1):
            self.end_calibration()
            return

        self.next_step()

    @QtCore.pyqtSlot()
    def end_calibration(self):
        regression, X, y = self.fit(return_params=True)
        r2 = regression.score(X, y)

        predictions = regression.predict(X)
        mae = mean_absolute_error(y, predictions)
        rmse = mean_squared_error(y, predictions)**(1/2)

        self.calibration_model["last_calibration"]["a"] = regression.coef_[0]
        self.calibration_model["last_calibration"]["b"] = regression.intercept_
        self.calibration_model["last_calibration"]["R2"] = r2
        self.calibration_model["last_calibration"]["MAE"] = mae
        self.calibration_model["last_calibration"]["RMSE"] = rmse

        self.save()

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

    def save(self):
        path = os.path.join(MODELS_PATH, self.calibration_model["name"] + ".json")
        with open(path, "w") as file:
            json.dump(self.calibration_model, file)

        with open(LAST_MODEL, "w") as file:
            json.dump(self.calibration_model, file)

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
        info["measurand"] = self.calibration_model["steps"][self.current_step]
        info["outlier"] = False

        self.spectra_info = pd.concat([self.spectra_info, pd.DataFrame([info, ])], ignore_index=True)

        self.mark_outliers()
        regression_model = self.fit()

        processing.plot_calibration(spectrum,
                        self.plot_widget.axs,
                        self.spectra_info,
                        self.options,
                        regression_model)

        self.plot_widget.add_text_calibration()
        self.plot_widget.canvas.figure.canvas.draw()

        self.update_trigger.emit()

    def update_entry(self):
        # Conferindo e atualiando a quantidade de amostras
        sub_df = self.current_sub_df
        samples_taken = len(sub_df.index)

        self.progressBar.setValue(100*samples_taken//self.n_samples)

        if samples_taken >= self.n_samples:
            self.finish_step()

    def mark_outliers(self):
        """Removendo com o método iqr"""

        sub_df = self.current_sub_df
        if len(sub_df.index) < 5:
            return None

        q1 = self.current_sub_df["best_wl"].quantile(0.25)
        q3 = self.current_sub_df["best_wl"].quantile(0.75)
        iqr = q3 - q1

        lims = q1 - 1.5 * iqr, q3 + 1.5 * iqr

        mask = (sub_df["best_wl"] < lims[0]) | (sub_df["best_wl"] > lims[1])
        out_index = sub_df[mask].index
        not_out_index = sub_df[~mask].index

        self.spectra_info.loc[out_index, "outlier"] = True
        self.spectra_info.loc[not_out_index, "outlier"] = False

    def fit(self, return_params=False):
        if self.current_step == 0:
            return None

        model = LinearRegression()

        sub_df = self.spectra_info[~self.spectra_info["outlier"]]
        X = np.array(sub_df["best_wl"]).reshape(-1, 1)
        y = sub_df["measurand"]

        model.fit(X, y)

        if return_params:
            return model, X, y

        return model

    def closeEvent(self, event):
        self.running = False
        self.loader.pause()

        event.accept()
