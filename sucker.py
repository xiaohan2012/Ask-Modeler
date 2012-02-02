with open('filtered_result','w') as in_f:    
    with open('crawled_result.dat','r') as f:
        for l in f.readlines():
            if 'pdb' in l:
                in_f.write(l)
