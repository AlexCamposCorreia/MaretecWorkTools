import os



if __name__ == '__main__':
    

    multiplier = 1000/20 * 100



    model_profiles_loc = '/model_results/profiles/'

    dirs = next(os.walk('.'))[1]
    cp_dirs = list(filter(lambda x: x.startswith('campanha'), dirs))

    #print([x + model_profiles_loc for x in cp_dirs])

    for cp_dir in cp_dirs:
        files_in_dir = list(os.walk(cp_dir + model_profiles_loc))[0][2]
        for fname in files_in_dir:
            if fname.startswith('phytoplankton'):
                print(cp_dir+model_profiles_loc+fname)
                f = open(cp_dir+model_profiles_loc+fname, 'r')
                f2 = open(cp_dir+model_profiles_loc+fname.replace('phytoplankton', 'chlorophyll'), 'w')
                f2.write('# depth,chlorophyll\n')
                for line in f.readlines():
                    if line.startswith('#'):
                        continue
                    else:
                        line = line.split(',')
                        line[1] = float(line[1]) * multiplier
                        f2.write(line[0]+','+str(line[1])+'\n')
                f.close()
                f2.close()
