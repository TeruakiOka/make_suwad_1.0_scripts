#! /bin/python
# coding: utf-8

from io import StringIO
import csv


def csv_splitter(csv_line, empty_elem=''):
    fin = StringIO(str(csv_line))     # バイナリにしないとcsvのnextで怒られる
    splitted_line = next(csv.reader(fin))
    fin.close()
    ret = []
    for elem in splitted_line:
        if elem:
            ret.append(elem)
        else:
            ret.append(empty_elem)
    return ret


def csv_joinner(listed_line):
    ret = []
    for elem in listed_line:
        elem = elem.replace('"', '""')
        if ',' in elem:
            elem = '"' + elem + '"'
        ret.append(elem)
    return ','.join(ret)


if __name__ == '__main__':
    line = '1,2,3,abc,"ab,c"'
    print(line)
    line = csv_splitter(line)
    print(line)
    line = csv_joinner(line)
    print(line)
