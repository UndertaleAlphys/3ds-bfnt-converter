if __name__ == '__main__':
    f = open('LOG.txt', 'r')
    d = f.read()
    r = dict()
    f.close()
    current_file = None
    for line in d.split('\n'):
        e = line.strip().split()
        if not e:
            pass
        elif e[0] == 'FILE':
            current_file = e[1]
        else:
            current_text = e[1]
            if r.get(current_file) is None:
                r[current_file] = {}
            if r[current_file].get(current_text) is None:
                r[current_file][current_text] = [dict() for _ in range(16)]
            lst = list(map(int, e[2:]))
            for i in range(0x10):
                curr_num = r[current_file][current_text][i].get(lst[i], 0)
                r[current_file][current_text][i][lst[i]] = curr_num + 1
    for file in r:
        print('FILE\t' + file)
        for texture in r[file]:
            print('\ttexture\t' + texture)
            for i in range(0x10):
                code_pair_lst = [code_pair for code_pair in r[file][texture][i].items()]
                print(f'\t\t{hex(i):<4}')
                if len(code_pair_lst) >= 5:
                    print('\t\t\tNo result')
                else:
                    code_pair_lst.sort(key=lambda p: p[1], reverse=True)
                    for pair in code_pair_lst:
                        print(f'\t\t\t{pair[0]}:{pair[1]}')
