# -*- coding: utf-8 -*-
"""
Created on Sep 16 2021

@author: felip
"""

import os
from os import listdir
from os.path import isfile, join
import time


def move_files(sender, recipient, T=0):
	files = [f for f in listdir(sender) if isfile(join(sender, f))]
	for file in files:
		print(f'Transfering {file}...')
		if T>0:
			time.sleep(T)
		try:
			os.replace(sender+file, recipient+file)
		except:
			Exception('Tranfer error')

def exit():
	print(f'finished... \nReturning files...')
	time.sleep(1)
	move_files(to_path, from_path)

from_path = 'test_data/from/'
to_path = 'test_data/to/'

print(f'Ctrl+C to finish program....')
user_input = 'a'
try:
	user_input = input(f'Enter [s] to start the emulation: ')
	if user_input == 's':
		move_files(from_path, to_path, T=1)

except KeyboardInterrupt:
	print(f'\nUser ')
	exit()


exit()
