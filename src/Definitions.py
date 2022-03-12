import os

MODELS_PATH = os.path.join(os.getenv('APPDATA'), 'litel_osa', 'calibration')
LAST_MODEL = os.path.join(os.getenv("APPDATA"), "litel_osa", "last_calibrated.json")
CONFIG_PATH = os.path.join(os.getenv('APPDATA'), 'litel_osa', 'config.json')

DEFAULT_OPTIONS = {'out_file': 'out.csv',
                   'batch_size': 50,
                   'spectra_path': './spectra',
                   'wl_range': [1.5e-6, 1.6e-6],
                   'mov_mean': 5,
                   'graph_window': 100,
                   'prominence': 5,
                   'valley_width': 100}