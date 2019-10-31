
input_file = './F3_2018.xyz'
output_file = './F3_2018_cut.xyz'

lon_min = -9.6055
lon_max = -8.5892
lat_min = 37.3720
lat_max = 38.3821

separator = ' '

MOHIDxyzBlock = True

print('Working...')

f1 = open(input_file, 'r')
f2 = open(output_file, 'w')

if MOHIDxyzBlock:
    f2.write('<begin_xyz>\n')

while True:
    l = f1.readline()
    if l == '':
        break
    l = l.strip('\n; ')
    l = l.split(';')
    l = list(map(lambda x: float(x), l))
    if lon_min <= l[0] <= lon_max and lat_min <= l[1] <= lat_max:
        l[2] = -l[2]
        l = list(map(lambda x: str(x), l))
        f2.write(separator.join(l) + '\n')

f2.write('<end_xyz>\n')

f1.close()
f2.close()

print('Finished.')
