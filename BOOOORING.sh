for folder in 30-*; do sed -i "s/walltime=0.:00:00/walltime=10:00:00/" $folder/*.pbs; done

for folder in 30-*; do sed -i "s/3.e-./3.e-1/" $folder/hfodd.d; mv $folder/*.out $folder/out/; done

# 02
# 00
for index in 1 27 28 31 41 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87; do cp 30-02_fission/restart/HFODD_*0$index.REC 30-00_fission/restart; done

# minus2
for index in 35 41 58 59 60 61 62 63 64 66 68 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87; do cp 30-00_fission/restart/HFODD_*0$index.REC 30-minus2_fission/restart; done

# 04
cp 30-02_fission/restart/HFODD_*87.REC 30-04_fission/restart/

# 06

# 08

# 16
cp 30-18_fission/restart/HFODD_*001.REC 30-16_fission/restart/
cp 30-18_fission/restart/HFODD_*071.REC 30-16_fission/restart/

# 14
cp 30-16_fission/restart/*.REC 30-14_fission/restart/

# 12
for index in 54 55 56 57 58 59 60 61 62 63 64 65 66 68 69 70 78 79 80 81 82 83 84 85 86 87; do cp 30-14_fission/restart/HFODD_*0$index.REC 30-12_fission/restart; done

# 10
for index in 34 35 36 40 41 42 43 44 45 46 47 48 57 58 59 60 62 63 64 65 66 68 69 76 77 78 79 80 84 86 87; do cp 30-12_fission/restart/HFODD_*0$index.REC 30-10_fission/restart; done

# 18
# 20

# 22

# 24

# 26

# 28

# 30
