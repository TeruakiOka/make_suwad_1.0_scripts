#! /usr/bin/python3
# encoding: utf8

import sys
import unicodedata as ud

def rewrite(input_file, output_file):
    with open(output_file, 'w', encoding='utf-8') as fout:
        with open(input_file, 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.lstrip('\ufeff\ufffe').rstrip('\r\n')
                line = line.replace('_START_ARTICLE_', '').replace('_START_SECTION_', '').replace('_START_PARAGRAPH_', '')
                if line.strip():
                    line = line.replace('_NEWLINE_', '\n')
                    paragraphs = line.replace('\t', '　').split('\n')
                    for p in paragraphs:
                        for c in p:
                            if ud.category(c)[0] == 'C':
                                p = ''
                                break
                        if p.strip():
                            fout.write(p + '\n')

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc == 3:
        input_file = argvs[1]
        output_file = argvs[2]
        print('INPUT:\t' + input_file)
        print('OUTPUT:\t' + output_file)
        rewrite(input_file, output_file)
