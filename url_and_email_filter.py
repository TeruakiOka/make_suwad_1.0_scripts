#! /usr/bin/python3
# encoding: utf8

import re
import sys

pattern_url = re.compile(r'(https?|ftp)(:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+)', re.ASCII)
pattern_email = re.compile(r'[\w\.\-\+]+@[\w\-]+\.[\w\.\-]+', re.ASCII)

def url_and_email_filter(input_file, output_file):

	with open(output_file, 'w', encoding='utf-8') as fout:
		with open(input_file, 'r', encoding='utf-8') as fin:
			
			for line in fin:

				# 改行とBOM除去
				line = line.lstrip('\ufeff\ufffe').rstrip('\r\n')
				if not line:
					continue

				if (pattern_url.search(line) is None) and \
					(pattern_email.search(line) is None):
					fout.write(line + '\n')

				else:
					print(pattern_url.findall(line))
					print(pattern_email.findall(line))
					print(line + '\n')

if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)

	if argc != 3:
		print('python3 url_and_email_filter.py input_file output_file')

	else:
		input_file = argvs[1]
		output_file = argvs[2]
		url_and_email_filter(input_file, output_file)
