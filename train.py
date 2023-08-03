import os
import sys
import shutil
import random
import subprocess
import matrix2vec
import cluster2matrix

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

mecab_libexec_dir = '/work/oka/bin/mecab0996/libexec/mecab/'
mecab_bin = '/work/oka/bin/mecab0996/bin/mecab'

unidic_cwj = os.path.join(current_dir, 'unidic/unidic-cwj-202302/')
unidic_csj = os.path.join(current_dir, 'unidic/unidic-csj-202302/')

bayon_bin = '/work/oka/bin/bayon/bin/bayon'

src_seed_dir = os.path.join(current_dir, 'madic_seed')
factory_dir = os.path.join(current_dir, 'factory')

cc100_split_dir = os.path.join(current_dir, 'data/cc100/split_files/') 
wiki40b_split_dir = os.path.join(current_dir, 'data/wiki40b/split_files/')

cc100_raw_list = [os.path.join(cc100_split_dir, f)
					for f in os.listdir(cc100_split_dir) if not f.startswith('__')]
wiki40b_raw_list = [os.path.join(wiki40b_split_dir, f)
					for f in os.listdir(wiki40b_split_dir) if not f.startswith('__')]


def train(work_dir_num: int, _pre_num: int = -1, _comp_ratio: float = 0.1, _c1: float = 1.0, _c2: float = 1.0, _c3: float = 1.0):

	work_dir = os.path.join(factory_dir, str(work_dir_num))
		
	os.makedirs(work_dir)
	
	seed_dir = os.path.join(work_dir, 'seed')
	shutil.copytree(src_seed_dir, seed_dir)
	
	cc100_file_raw = random.choice(cc100_raw_list)
	wiki40b_file_raw = random.choice(wiki40b_raw_list)

	shutil.copy2(cc100_file_raw, seed_dir)
	shutil.copy2(wiki40b_file_raw, seed_dir)

	cc100_file_raw = os.path.join(seed_dir, os.path.basename(cc100_file_raw))
	wiki40b_file_raw = os.path.join(seed_dir, os.path.basename(wiki40b_file_raw))

	mecab_process_unidic_cwj = subprocess.run([mecab_bin, '-d', unidic_cwj,\
												'-o', os.path.join(seed_dir, 'wiki40b.mecab'), wiki40b_file_raw],\
												shell=False)
	
	mecab_process_unidic_csj = subprocess.call([mecab_bin, '-d', unidic_csj,\
												'-o', os.path.join(seed_dir, 'cc100.mecab'), cc100_file_raw],\
												shell=False)	

	with open(os.path.join(seed_dir, 'corpus'), 'w', encoding='utf-8') as fout_catcp:
		cat_corpus_process = subprocess.call(['cat', os.path.join(seed_dir, 'wiki40b.mecab'), os.path.join(seed_dir, 'cc100.mecab')],\
											shell=False, stdout=fout_catcp)

	mecab_dict_index_process_1 =  subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-dict-index'), '-d', seed_dir, '-o', seed_dir],\
											shell=False)

	if _pre_num == -1:

		mecab_cost_train_process = subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-cost-train'), '-d', seed_dir,\
												'-c', str(_c1), '-p', '10',\
												os.path.join(seed_dir, 'corpus'), os.path.join(seed_dir, 'model.def')],\
												shell=False)
	else:

		pre_model = os.path.join(factory_dir, str(_pre_num), 'final_2', 'model.def')
		mecab_cost_train_process = subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-cost-train'), '-d', seed_dir,\
												'-c', str(_c2), '-p', '10',\
												'-M', pre_model,\
												os.path.join(seed_dir, 'corpus'), os.path.join(seed_dir, 'model.def')],\
												shell=False)

	final_dir = os.path.join(work_dir, 'final')
	os.makedirs(final_dir)

	mecab_dict_gen_process = subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-dict-gen'), '-o', final_dir, '-d', seed_dir,\
											 '-m', os.path.join(seed_dir, 'model.def')],\
											shell=False)

	os.rename(os.path.join(final_dir, 'matrix.def'), os.path.join(final_dir, '____matrix.def____'))
	os.rename(os.path.join(final_dir, 'left-id.def'), os.path.join(final_dir, '____left-id.def____'))
	os.rename(os.path.join(final_dir, 'right-id.def'), os.path.join(final_dir, '____right-id.def____'))
	os.rename(os.path.join(final_dir, 'lex.csv'), os.path.join(final_dir, '____lex.csv____'))
	os.rename(os.path.join(final_dir, 'unk.def'), os.path.join(final_dir, '____unk.def____'))
	
	right_id_num = None
	left_id_num = None
	with open(os.path.join(final_dir, '____matrix.def____'), 'r', encoding='utf-8') as fin_matrix_head:
		line = fin_matrix_head.readline()
		line = line.strip()
		right_id_num, left_id_num = line.split(' ')
	copr_right_id_num = str(int(float(right_id_num) * _comp_ratio))
	copr_left_id_num = str(int(float(left_id_num) * _comp_ratio))
	
	matrix2vec.trans(os.path.join(final_dir, '____matrix.def____'), os.path.join(final_dir, 'right_id.vec'))
		
	with open(os.path.join(final_dir, 'right_id.cluster'), 'w', encoding='utf-8') as fout_right_id_cluster:
		bayon_process_right =  subprocess.run([bayon_bin, '-n', copr_right_id_num, '-p',\
										os.path.join(final_dir, 'right_id.vec')],\
										shell=False, stdout=fout_right_id_cluster)
	
	cluster2matrix.trans(os.path.join(final_dir, 'right_id.cluster'), os.path.join(final_dir, 'right_id.vec'),\
								os.path.join(final_dir, '____right-id.def____'), os.path.join(final_dir, '____lex.csv____'),\
								os.path.join(final_dir, '____unk.def____'))

	os.rename(os.path.join(final_dir, 'matrix.def'), os.path.join(final_dir, '__matrix.def__'))
	os.rename(os.path.join(final_dir, 'lex.csv'), os.path.join(final_dir, '__lex.csv__'))
	os.rename(os.path.join(final_dir, 'unk.def'), os.path.join(final_dir, '__unk.def__'))

	matrix2vec.trans(os.path.join(final_dir, '__matrix.def__'), os.path.join(final_dir, 'left_id.vec'), _is_left=True)
	
	with open(os.path.join(final_dir, 'left_id.cluster'), 'w', encoding='utf-8') as fout_left_id_cluster:
		bayon_process_left =  subprocess.run([bayon_bin, '-n', copr_left_id_num, '-p',\
										os.path.join(final_dir, 'left_id.vec')],\
										shell=False, stdout=fout_left_id_cluster)

	cluster2matrix.trans(os.path.join(final_dir, 'left_id.cluster'), os.path.join(final_dir, 'left_id.vec'),\
							os.path.join(final_dir, '____left-id.def____'), os.path.join(final_dir, '__lex.csv__'),\
							os.path.join(final_dir, '__unk.def__'), _is_left=True)

	mecab_dict_index_process_2 =  subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-dict-index'), '-d', final_dir, '-o', final_dir],\
											shell=False)
	
	mecab_process_madic_wiki40b = subprocess.run([mecab_bin, '-d', final_dir,\
												'-o', os.path.join(final_dir, 'wiki40b.mecab'), wiki40b_file_raw],\
												shell=False)

	mecab_process_madic_cc100 = subprocess.call([mecab_bin, '-d', final_dir,\
												'-o', os.path.join(final_dir, 'cc100.mecab'), cc100_file_raw],\
												shell=False)

	with open(os.path.join(final_dir, 'corpus'), 'w', encoding='utf-8') as fout_catcp_2:
		cat_corpus_process_2 = subprocess.call(['cat', os.path.join(final_dir, 'wiki40b.mecab'), os.path.join(final_dir, 'cc100.mecab')],\
												shell=False, stdout=fout_catcp_2)	

	os.rename(os.path.join(final_dir, 'model.def'), os.path.join(final_dir, '____model.def____'))

	mecab_cost_train_process = subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-cost-train'), '-d', final_dir,\
											'-c', str(_c3), '-p', '10', '-M', os.path.join(final_dir, '____model.def____'),\
											os.path.join(seed_dir, 'corpus'), os.path.join(final_dir, 'model.def')],\
											shell=False)

	final_dir_2 = os.path.join(work_dir, 'final_2')
	os.makedirs(final_dir_2)
	
	mecab_dict_gen_process_2 = subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-dict-gen'), '-o', final_dir_2, '-d', final_dir,\
											'-m', os.path.join(final_dir, 'model.def')],\
											shell=False)

	mecab_dict_index_process_3 =  subprocess.run([os.path.join(mecab_libexec_dir, 'mecab-dict-index'), '-d', final_dir_2, '-o', final_dir_2],\
											shell=False)


if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)

	if argc >= 2:
		
		start_num = int(argvs[1])
		
		comp_ratio = 0.1
		if argc >= 3:
			comp_ratio = float(argvs[2])
		
		c1 = 1.0 # initial UniDic de train 
		if argc >= 4:
			c1 = float(argvs[3])
 
		c2 = 1.0 # UniDic de train
		if argc >= 5:
			c2 = float(argvs[4])

		c3 = 1.0 # CompDic de train
		if argc >= 6:
			c3 = float(argvs[5])

		print(f'comp_ratio: {comp_ratio}')
		print(f'c1: {c1}')
		print(f'c2: {c2}')
		print(f'c3: {c3}')

		for j, i in enumerate(range(start_num, start_num + 15)):
			if j == 0:
				train(i, _comp_ratio=comp_ratio, _c1=c1, _c2=c2, _c3=c3)
			else:
				train(i, _pre_num=i-1, _comp_ratio=comp_ratio, _c1=c1, _c2=c2, _c3=c3)
	else:
		print('\npython3 train.py start_num *comp_ratio *c1 *c2 *c3\n')
