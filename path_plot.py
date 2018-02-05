import re, math
import matplotlib.pyplot as plt

infile = 'mypath-1Feb2018.out-2D-GCM'

myfile = open(infile,'r')
mydata = myfile.readlines()

x_out, y_out = [], []
x_exit, y_exit = [], []
x_path, y_path = [], []
actn = []

for line in mydata:
    if re.match('.*Exit point.*',line):   # Actually-attained outer turning points
        mycols = line.split(' ')
        mycols = filter(None,mycols)
        x_exit.append(float(mycols[3]))
        y_exit.append(float(mycols[4]))
        actn.append(float(mycols[5]))
    if re.match('.*path:.*',line):        # Minimum action path
        mycols = line.split(' ')
        mycols = filter(None,mycols)
        x_path.append(float(mycols[1]))
        y_path.append(float(mycols[2]))

plt.plot(x_out, y_out, 'k+')
plt.plot(x_exit, y_exit, 'r^')
plt.plot(x_path, y_path, 'b')
plt.xlim(0,400)
plt.ylim(0,50)
plt.xlabel('q20')
plt.ylabel('q30')

plt.show()

smin = min(actn)
exit_probs = open('exit_probs.out','w')
for x,y,s in zip(x_exit,y_exit,actn):
#    try:
#        prob = 1.0/(1+math.exp(2*s))
#    except:
#        prob = float('inf')
    prob = math.exp(2*(smin-s)) # approximate ratio of tunneling prob compared to max tunneling prob/min action path
    exit_probs.write('{:>5}  {:>5}  {:>12.5}\n'.format(x,y,prob))
exit_probs.close()
