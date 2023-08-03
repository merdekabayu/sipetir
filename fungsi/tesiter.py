samcgp=[]
fcgp = open('fungsi/gmt/sambarancgp.dat', 'r')
baris = fcgp.readlines()
for i in range(len(baris)):
    bar = baris[i].split()
    samcgp+=[[bar[0],bar[1]]]

print(samcgp[0])