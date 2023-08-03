import sys
import os
import toolbox as tb

def trans(_cluster_file:str, _vec_file: str, _id_def_file: str, _lex_csv_file: str, _unk_def_file: str, _is_left: bool = False) -> None:

	# bayon 出力の読み込み
	id2class = {0: 0} # right-id(or left-id) -> class 変換辞書
	class2max_sim_id = {0: 0} # class -> 代表ベクトルにあたる right-id (or left-id) 変換辞書
	with open(_cluster_file, 'r', encoding='utf-8') as fin_c:
		for line in fin_c:
			line = line.strip('\r\n')
			if line:
				line = line.split('\t')
				class_name = int(line[0])
				_it = iter(line[1:])
				max_sim = None
				max_sim_id = None
				for _id, _point in zip(_it, _it):
					_id = int(_id)
					_point = float(_point)
					if _id != 0:
						id2class[_id] = class_name
					if (max_sim_id is None) or (_point > max_sim):
						max_sim_id = _id
						max_sim = _point
				class2max_sim_id[class_name] = max_sim_id
				
	# (bayon の入力に使った)ベクトルファイルの読み込み
	id2vec = {}
	with open(_vec_file, 'r', encoding='utf-8') as fin_v:
		for line in fin_v:
			line = line.rstrip('\r\n')
			if line:
				line = line.split('\t')
				_vec_head_id = int(line[0])
				_vec = {}
				_it = iter(line[1:])
				for _id, _cost in zip(_it, _it):
					_id = int(_id)
					_cost = int(_cost)
					_vec[_id] = _cost
				id2vec[_vec_head_id] = _vec
	
	# *-id.def の書き換え(元の *-id.def は rename 済み)
	output_id_file_name = 'right-id.def'
	if _is_left:
		output_id_file_name = 'left-id.def'
	with open(os.path.join(os.path.dirname(_id_def_file), output_id_file_name), 'w', encoding='utf-8') as fout_id_def:
		with open(_id_def_file, 'r', encoding='utf-8') as fin_id_def:
			for line in fin_id_def:
				line = line.split(' ', 1)
				_id = int(line[0])
				_id = id2class[_id]
				line[0] = _id
				fout_id_def.write(f'{line[0]} {line[1]}')

	# matrix.def の書き換え(元の matrix.def は rename済み)
	# # right
	if not _is_left:
		with open(os.path.join(os.path.dirname(_id_def_file), 'matrix.def'), 'w', encoding='utf-8') as fout_matrix:
			fout_matrix.write(f'{len(class2max_sim_id)} {len(id2vec[0])}\n')
			for class_name in sorted(class2max_sim_id):
				_right_id = class2max_sim_id[class_name]
				_vec = id2vec[_right_id]
				for _left_id in sorted(_vec):
					_cost = _vec[_left_id]
					fout_matrix.write(f'{class_name} {_left_id} {_cost}\n')
	# # left
	else:
		with open(os.path.join(os.path.dirname(_id_def_file), 'matrix.def'), 'w', encoding='utf-8') as fout_matrix:
			fout_matrix.write(f'{len(id2vec[0])} {len(class2max_sim_id)}\n')
			for _right_id in sorted(id2vec[0]):
				for class_name in sorted(class2max_sim_id):
					_left_id = class2max_sim_id[class_name]
					_vec = id2vec[_left_id]
					_cost = _vec[_right_id]
					fout_matrix.write(f'{_right_id} {class_name} {_cost}\n')

	# lex.csv の書き換え(元の lex.csv はrename済み)
	with open(os.path.join(os.path.dirname(_lex_csv_file), 'lex.csv'), 'w', encoding='utf-8') as fout_lex:
		with open(_lex_csv_file, 'r', encoding='utf-8') as fin_lex:
			for line in fin_lex:
				line = line.rstrip('\r\n')
				if line:
					line = tb.csv_splitter(line)
					if not _is_left:
						_right_id = int(line[2])
						_right_id = id2class[_right_id]
						line[2] = str(_right_id)
					else:
						_left_id = int(line[1])
						_left_id = id2class[_left_id]
						line[1] = str(_left_id)
					line = tb.csv_joinner(line)
					fout_lex.write(f'{line}\n')

	# unk.def の書き換え（元のunk.defは書き換え済み）
	with open(os.path.join(os.path.dirname(_unk_def_file), 'unk.def'), 'w', encoding='utf-8') as fout_unk:
		with open(_unk_def_file, 'r', encoding='utf-8') as fin_unk:
			for line in fin_unk:
				line = line.rstrip('\r\n')
				if line:
					line = tb.csv_splitter(line)
					if not _is_left:
						_right_id = int(line[2])
						_right_id = id2class[_right_id]
						line[2] = str(_right_id)
					else:
						_left_id = int(line[1])
						_left_id = id2class[_left_id]
						line[1] = str(_left_id)
					line = tb.csv_joinner(line)
					fout_unk.write(f'{line}\n')


if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)

	if argc not in [6, 7]:
		print(f'\npython3 cluster2matrix.py right_id.cluster right_id.vec right-id.def lex.csv unk.def')
		print(f'\npython3 cluster2matrix.py left_id.cluster left_id.vec left-id.def lex.csv unk.def LEFT\n')
		sys.exit(0)

	print(f'INPUT: {argvs[1]}')
	print(f'INPUT: {argvs[2]}')
	print(f'INPUT: {argvs[3]}')
	print(f'INPUT: {argvs[4]}')
	print(f'INPUT: {argvs[5]}')
	is_left = False
	if argc == 7 and argvs[6] == 'LEFT':
		print('IS_LEFT: ON')
		is_left = True

	trans(argvs[1], argvs[2], argvs[3], argvs[4], argvs[5], _is_left=is_left)
