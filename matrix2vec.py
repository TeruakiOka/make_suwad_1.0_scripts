import sys
import os

def trans(_input_file: str, _output_file: str, _is_left: bool = False) -> None:

	output_lists = {}
	with open(_input_file, 'r', encoding='utf-8') as fin:
		for i, line in enumerate(fin):
			line = line.strip('\r\n')
			if line:
				if i > 0:
					right_id, left_id, cost = line.split(' ')

					class_name = int(right_id)
					key = int(left_id)

					if _is_left:
						class_name = int(left_id)
						key = int(right_id)

					val = int(cost)

					if class_name not in output_lists:
						output_lists[class_name] = {}

					output_lists[class_name][key] = val

	with open(_output_file, 'w', encoding='utf-8') as fout:
		for class_id in sorted(output_lists):
			output_line = [str(class_id)]
			for key in sorted(output_lists[class_id]):
				cost = output_lists[class_id][key]
				output_line.append(str(key))
				output_line.append(str(cost))
			fout.write('\t'.join(output_line) + '\n')

if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)

	if argc not in [3, 4]:
		print(f'\npython3 matrix2vec.py matrix.def outputfile')
		print(f'python3 matrix2vec.py matrix.def outputfile LEFT\n')
		sys.exit(0)

	input_file = argvs[1]
	output_file = argvs[2]

	is_left = False
	if argc == 4 and argvs[3] == 'LEFT':
		is_left = True
	
	print(f'INPUT:\t{input_file}')
	print(f'OUTPUT:\t{output_file}')

	if is_left:
		print('IS_LEFT ON')

	trans(input_file, output_file, _is_left=is_left)
