
def write_to_csv(filename, prop_name, depths, props):
    with open(filename, 'w') as f:
        f.write('#depth,' + prop_name + '\n')
        for n in range(len(depths)):
            f.write(str(depths[n])+','+str(props[n])+'\n')