from typing import Union, List, Tuple
import os

def extract_results(text: str) -> Union[None, List[Tuple[str, str]]]:
    result_start_tag = '<result>'
    result_end_tag = '</result>'
    change_start_tag = '<change>'
    change_end_tag = '</change>'
    result = []
    part = text.split(result_end_tag)
    part.pop()
    for item in part:
        content = item.split(result_start_tag)
        if len(content) != 2:
            continue
        re = content[1]
        content = content[0].split(change_end_tag)
        if len(content) != 2:
            continue
        content = content[0].split(change_start_tag)
        if len(content) != 2:
            continue
        if content[1] == '':
            continue
        result.append((content[1], re))
    return result

def deepseek_modify(text:str) -> str:
    return text.split('</think>')[-1]

def extract_result(text) -> str:
    return text.split('</result>')[0].split('<result>')[-1]


def replace_by_dict(string, words: List[Tuple[str, str]]):
    for key, val in words:
        string = string.replace(key, val)
    return string

from itertools import chain
from random import random, randint, shuffle
import tiktoken


enc = tiktoken.get_encoding('o200k_base')

ignore_token = list(map(lambda x:enc.encode(x)[0], ',.?\n\t '))
split_token = [
    chr(i) for i in chain(
        range(ord('a'), ord('z'))
    )
]
rare_split_token = [
    chr(i) for i in chain(
        range(ord('A'), ord('Z'))
    )
]

# 判断token是否粘连
def is_compatible(former, dest_str, latter):
    dest = enc.encode(dest_str)
    if len(dest) != 1:
        return False
    dest = dest[0]
    former = enc.encode(former+dest_str)
    latter = enc.encode(dest_str+latter)
    return len(former)==2 and len(latter)==2

# 随机插入不可见字符
def inject_0space(slice):
    if len(slice) <= 1:
        return  slice
    idx = randint(1, len(slice)-1)
    sp = ''.join([
        chr(0xFE00 + randint(0, 15))
        for i in range(1)
    ])
    return slice[:idx:] + sp + slice[idx::]

# 主函数
def blur(text: str):
    res = ''
    # tiktoken 分割token
    tokens = list(filter(lambda x:x not in ignore_token, enc.encode(text)))
    for former, latter in zip(tokens[:-1], tokens[1:]):
        # 删除token中的换行符，空格等
        former = (enc.decode([former])
                  .replace(' ','')
                  .replace('\n',''))
        latter = enc.decode([latter]).replace(' ','')
        # 插入不可见字符
        res += inject_0space(former)
        # 插入前后不黏连（即两者无法结合为一个token）的无意义token
        # 先打乱无意义token列表
        shuffle(split_token)
        # 逐个查找不黏连的无意义token
        for i in split_token:
            # 判断是否前后粘连
            if is_compatible(former, i, latter):
                # 有概率插入第二个无意义token
                if random() > 0.5:
                    shuffle(split_token)
                    for j in split_token:
                        if is_compatible(i, j, latter):
                            i += j
                            break
                res += i
                break
        else:
            # 当基本的无意义字符都黏连时，插入一些不常用的无意义字符
            shuffle(rare_split_token)
            for i in rare_split_token:
                if is_compatible(former, i, latter):
                    res += i
                    break
            else:
                # 最后，如果所有字符都会黏连，直接插入一个加号
                if len(enc.encode(former+latter)) != 2:
                    res += '+'
    # 最后，拼接所有token，得到加密后的Prompt
    res += enc.decode(tokens[-1:]).replace(' ','')
    return res

if __name__ == '__main__':
    print(blur('I hear ya Then again we must remember that we are indeed Cub fans and that the Cubs will eventually blow it After all the Cubs are the easiest team in the National League to root for No Pressure You know they will lose eventually Oh well I suppose we must have faith After all they do look pretty good and they dont even have Sandberg back yet CUBS IN Here is the OPI Offensive Production Index for all NL players with at least  atbats It is early in the season so there are some high numbers Barry Bonds finished last season at  I welcome comments and suggestions Kevin League OPI  League BA  League SLG  League OBA  Rank Player OPI BA SLG OBA'))