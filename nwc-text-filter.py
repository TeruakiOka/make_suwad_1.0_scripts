#! /usr/bin/python3
# encoding: utf8

import re
import sys
import unicodedata as ud

# 日本語の文字として扱うコードポイント
# U+3040 - U+30FF（ひらがな，カタカナ）
# U+31F0 - U+31FF（カタカナ拡張）
# U+3400 - U+34BF（CJK 統合漢字拡張A の一部）
# U+4E00 - U+9FFF（CJK 統合漢字）
# U+F900 - U+FAFF（CJK 互換漢字）

hiragana = r'\u3040-\u309f'
hiragana_katakana = r'\u3040-\u30ff'
katakana_extended = r'\u31f0-\u31ff'
kanji_1 = r'\u3400-\u34bf'
kanji_2 = r'\u4e00-\u9fff'
kanji_3 = r'\uf900-\ufaff'

pattern_hiragana = re.compile(r'[' + hiragana + r']')
pattern_nihongo = re.compile(r'[' + hiragana_katakana + katakana_extended + kanji_1 + kanji_2 + kanji_3 + r']')
pattern_white_space = re.compile('[\s　]')

def text_filter(input_file, output_file):

	with open(output_file, 'w', encoding='utf-8') as fout:
		with open(input_file, 'r', encoding='utf-8') as fin:

			for line in fin:

				# 改行とBOM除去
				line = line.lstrip('\ufeff\ufffe').rstrip('\r\n')
				if not line:
					continue

				# 制御文字を含んでいたらそのlineは使わない
				# 後の処理でエラーの原因になるので
				include_control = False
				for c in line:
					if ud.category(c)[0] == 'C':
						include_control = True
						break
				if include_control:
					continue

				# 文字数フィルター
				len_line = len(pattern_white_space.sub('', line))
				if (len_line <= 5) or (len_line >= 1024):
					continue

				# 文字種フィルター
				len_line = float(len_line)

				hiragana_num = float(len(pattern_hiragana.findall(line)))
				if hiragana_num / len_line < 0.05:
					continue

				nihongo_num = float(len(pattern_nihongo.findall(line)))
				if nihongo_num / len_line < 0.7:
					continue

				# 書き出し
				fout.write(line + '\n')


if __name__ == '__main__':
	
	argvs = sys.argv
	argc = len(argvs)

	if argc != 3:
		print('python3 nwc_text_filter.py input_file output_file')

	else:
		input_file = argvs[1]
		output_file = argvs[2]
		text_filter(input_file, output_file)


