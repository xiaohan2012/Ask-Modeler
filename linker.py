def get_target_url(tar_name,src_fp='result.csv'):
    """"""
    with open(src_fp,'r') as f:
        counter = 0
        for l in f.readlines():
            counter+=1
            if tar_name in l:
                return counter
        return -1
def get_modeler_url(target_url,src_fp='modeller_task.dat'):
    with open(src_fp,'r') as f:
        for l in f.readlines():
            if target_url in l:
                return l.split(':<',1)[1]

