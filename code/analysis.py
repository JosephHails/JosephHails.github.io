import pycorrector
import os
import json

dst_path = '../source/_posts/'

def get_files():
    files = os.listdir(dst_path)
    return files

def print_typos(file):
    with open(dst_path + file, "r", encoding='utf-8') as f:
        lines = f.readlines()
    log = []
    flag = 0
    main = 0
    line_ct = 0

    log.append("File {} start".format(file))
    while line_ct<len(lines):
        line = lines[line_ct]
        if main == 0:
            if '---' in line:
                flag += 1
                if flag == 2:
                    main = 1
            if "typo: false" in line:
                return 1, log
        else:
            corrected_sent, detail = pycorrector.correct(line)
            if len(detail) > 0:
                log.append("   Errors at line {}: {}".format(line_ct, detail))
        line_ct += 1
    log.append("File {} ended \n======".format(file))

    return 0, log
            
if __name__ == "__main__":
    files = get_files()
    ignore_ct = 0
    not_ignore_ct = 0
    log = []

    try:
        with open('../checked.json', 'r', encoding = 'utf-8') as f:
            checked_list = json.load(f)
    except:
        checked_list = []

    init = len(checked_list)

    for file in files:
        if file not in checked_list:
            ignore, log_tp = print_typos(file)
            log += log_tp
            if ignore:
                ignore_ct += 1
            else:
                not_ignore_ct += 1
            checked_list.append(file)
    with open('../checked.json', 'w', encoding='utf-8') as f:
        checked_list = json.dump(checked_list, f, indent=4, ensure_ascii=False)

    log.append("Typo Anal Done! \n With {} checked".format(not_ignore_ct))
    log.append("{} ignored...".format(ignore_ct))
    log.append("{} already checked before...".format(init))

    with open('../log.txt', 'w', encoding= 'utf-8') as f:
        for line in log:
            f.write(line + '\n')
    
    print("All done.")
