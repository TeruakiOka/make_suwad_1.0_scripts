import mojimoji
import sys

if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)

	if argc != 3:
		print('\npython3 h2z.py input_file output_file\n')
		sys.exit(0)

	input_file = argvs[1]
	output_file = argvs[2]

	print(f'INPUT:\t{input_file}')
	print(f'OUTPUT:\t{output_file}')

	with open(output_file, 'w', encoding='utf-8') as fout:
		with open(input_file, 'r', encoding='utf-8') as fin:
			for line in fin:
				line = line.lstrip('\ufeff\ufffe').rstrip('\r\n')
				line = mojimoji.han_to_zen(line, ascii=True, digit=True, kana='True')
				fout.write(f'{line}\n')
 
