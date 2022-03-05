from PyQt6.QtWidgets import QWidget

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        # region setting plots

        layout = QtWidgets.QVBoxLayout(self)
        self.canvas = FigureCanvas(Figure())
        layout.addWidget(self.canvas)
        layout.addWidget(NavigationToolbar(self.canvas, self))

        axs = self.canvas.figure.subplots(2, 2)
        gs = axs[0, 0].get_gridspec()

        for ax in axs[0, ::]:
            ax.remove()
        axbig = self.canvas.figure.add_subplot(gs[0, ::])

        self.axs = [axbig, axs[1, 0], axs[1, 1]]

        self.add_text()

        self.canvas.figure.tight_layout()

        # endregion

    def refit(self):
        self.canvas.figure.tight_layout()

    def add_text(self):
        self.axs[0].set_xlabel('tempo (s)')
        self.axs[0].set_ylabel(r'mensurando')

        self.axs[1].set_xlabel(r'comprimento de onda $\lambda$ ($\mu m$)')
        self.axs[1].set_ylabel(r'potência (dBW)')

        self.axs[2].set_xlabel('tempo (s)')
        self.axs[2].set_ylabel(r'$\lambda_{res}$ ($\mu m$)')
