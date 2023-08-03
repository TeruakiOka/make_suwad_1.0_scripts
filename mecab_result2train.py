#! /usr/bin/python3
# encoding: utf8

import sys
from toolbox import csv_splitter, csv_joinner


def translate(input_file, output_file):

	with open(output_file, 'w', encoding='utf-8') as fout:
		with open(input_file, 'r', encoding='utf-8') as fin:
			
			for line in fin:
				
				line = line.lstrip('\ufffe\ufeff').rstrip('\r\n')
				if not line:
					continue
				if line == 'EOS':
					fout.write('EOS\n')
				else:
					surface, line = line.split('\t')
					line = csv_splitter(line)
					line = [col if col else '*' for col in line]
					line = surface + '\t' + csv_joinner(line) + '\n'
					fout.write(line)

if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)

	if argc != 3:

		print('python3 mecab_result2train.py input(.mecab) output(.mecab)')	
	
	else:
		
		input_file = argvs[1]
		output_file = argvs[2]
		print('INPUT:', input_file)
		print('OUTPUT:', output_file)
		translate(input_file, output_file)		

