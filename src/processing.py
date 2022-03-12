import json

import process_spectra as ps

# Colors generated from this website
# https://learnui.design/tools/data-color-picker.html
colors = ['#003f5c',
          '#2f4b7c',
          '#665191',
          '#a05195',
          '#d45087',
          '#f95d6a',
          '#ff7c43',
          '#ffa600']

import numpy as np
import pandas as pd


def process(spectrum, opts: dict, function=None):
    # Fazer o vale aproximado sempre colocar o número na frente (resonant_wl_0)
    function = function or (lambda x: x)

    info = {}

    spectrum, info = ps.funcs.mask_spectrum(spectrum, info, opts['wl_range'],
                                            quiet=True)

    spectrum, _info = ps.funcs.filter_spectrum(spectrum, info, 5, 3,
                                               quiet=True)

    info = {**info, **_info}

    spectrum, _info = ps.funcs.get_approximate_valley(spectrum, info,
                                    prominence=opts['prominence'],
                                    valley_samples=opts['valley_width'])

    info = {**info, **_info}
    best_index = int(info['best_index'])
    info['best_wl'] = info[f'resonant_wl_{best_index}']
    info['best_wl_power'] = info[f'resonant_wl_power_{best_index}']
    info['measurand'] = function(info[f'best_wl'])

    return spectrum, info


def reorganize_valleys(info):
    # not working for now
    info = info.copy()

    # Nothing to reorganize
    if len(info) == 1:
        return info

    n_valleys = len([x for x in info.columns if 'resonant_wl_power' in x])

    new_valleys = []
    last_valleys = []

    # Get the valleys
    for i in range(n_valleys):
        new_valley = (info[f'resonant_wl_{i}'].iloc[-1],
                      info[f'resonant_wl_power_{i}'].iloc[-1])
        if not np.isnan(new_valley[0]):
            new_valleys.append(new_valley)

        for j in range(2, len(info) + 1):
            if info[f'resonant_wl_{i}'].iloc[-j]:
                last_valleys.append(info[f'resonant_wl_{i}'].iloc[-j])
                break

    new_valleys_ordered = {}

    # Order the valleys. Se for seguir com a ideia, tem q melhorar. No momento
    # fica com opções subótimas, colocando um vale no lugar de outro
    if len(last_valleys) <= len(new_valleys):
        for i in range(len(last_valleys)):
            best_distance = 1e9            # arbitrary large
            best_value = (None, None)

            for new_valley in new_valleys:
                if new_valley[0] is None:
                    continue

                distance = abs(new_valley[0] - last_valleys[i])
                if distance < best_distance:
                    best_distance = distance
                    best_value = new_valley

            if best_value[0] is not None:
                new_valleys.remove(best_value)
            new_valleys_ordered[f'resonant_wl_{i}'] = best_value[0]
            new_valleys_ordered[f'resonant_wl_power_{i}'] = best_value[1]

    else:
        for i, new_valley in enumerate(new_valleys):
            best_distance = 1e9  # arbitrary large
            best_index = None

            for c, last_valley in enumerate(last_valleys):
                if last_valley is None:
                    continue

                distance = abs(last_valley - new_valley[0])
                if distance < best_distance:
                    best_distance = distance
                    best_index = c

            new_valleys_ordered[f'resonant_wl_{best_index}'] = new_valley[0]
            new_valleys_ordered[f'resonant_wl_power_{best_index}'] = new_valley[1]
            if best_index is not None:
                new_valleys.pop(best_index)

    # # If got here, there are more new valleys than old ones
    # baseline = len(last_valleys)
    # for c, valley in enumerate(new_valleys):
    #     new_valleys_ordered[f'resonant_wl_{baseline + c}'] = valley[0]
    #     new_valleys_ordered[f'resonant_wl_power_{baseline + c}'] = valley[1]
    
    # Replace on the dataframe
    for key, item in new_valleys_ordered.items():
        info[key].iloc[-1] = item

    return info


def plot_base(spectrum, axs, info, opts: dict):
    for ax in axs:
        ax.clear()

    if len(info) > opts['graph_window']:
        info = info.iloc[-opts['graph_window']:]

    axs[1].plot(spectrum[::, 0]*1e6, spectrum[::, 1], color='black')

    valleys = len([x for x in info.columns if 'resonant_wl_power' in x])
    best_valley = int(info['best_index'].iloc[-1])

    for i in range(valleys):
        markerwidth = 3 if i == best_valley else 2
        axs[1].plot(info[f'resonant_wl_{i}'].iloc[-1]*1e6,
                    info[f'resonant_wl_power_{i}'].iloc[-1],
                    'x',
                    markeredgewidth=markerwidth,
                    markersize=7,
                    color=colors[i])
    for i in range(valleys):
        axs[2].plot(info['time'],
                    info[f'resonant_wl_{i}']*1e6,
                    'o-',
                    color=colors[i])

    # axs[2].plot(info['time'], info[f'resonant_wl_{best_valley}'], 'o-',
    #             color=colors[0])


def plot(spectrum, axs, info, opts: dict):
    plot_base(spectrum, axs, info, opts)

    axs[0].plot(info['time'], info['measurand'], 'o-', color='black')

def plot_calibration(spectrum, axs, info, opts: dict, regression, ref_wl,
                     ref_measurand):
    plot_base(spectrum, axs, info, opts)

    non_outliers = info[~info['outlier']]
    outliers = info[info['outlier']]
    reference = info[info["measurand"] == ref_measurand]
    non_reference = info[info["measurand"] != ref_measurand]

    axs[0].plot(non_reference['best_wl']*1e6, non_reference['measurand'],
                'o', color='black')
    axs[0].plot(reference['best_wl'] * 1e6, reference['measurand'],
                'o', color='blue')          # pontos de referência em azul
    # axs[0].plot(outliers['best_wl']*1e6, outliers['measurand'],
    #             'o', color='red')
    # Descomentar para printar outliers em vermelho

    if regression:
        limits = np.array(axs[0].get_xlim()).reshape(-1, 1) # limites em um
        axs[0].plot(limits, regression.predict((limits) * 1e-6 - ref_wl), '--', color='blue')
        axs[0].set_xlim(limits)

def plot_only_spectrum(spectrum, axs, info, opts):
    axs[1].clear()

    axs[1].plot(spectrum[::, 0]*1e6, spectrum[::, 1], color='black')

    valleys = len([x for x in info.keys() if 'resonant_wl_power' in x])
    best_valley = int(info['best_index'])

    for i in range(valleys):
        markerwidth = 3 if i == best_valley else 2
        axs[1].plot(info[f'resonant_wl_{i}']*1e6,
                    info[f'resonant_wl_power_{i}'],
                    'x',
                    markeredgewidth=markerwidth,
                    markersize=7,
                    color=colors[i])
