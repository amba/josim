#!/usr/bin/env python3
import numpy as np
f = open('JJA.cir', 'w')
frustration = 0.1
N = 2
M = 2
Imax = 10.5e-6
t = 100e-9
# current source
print("IDC\t0\t%d\tpwl(0 0 %g %g %g 0)" %( N*M+1, t, Imax, 2*t), file=f)
print(".model jjmod jj(rtype=1, vg=200uV, cap=10fF, r0=100, rN=100, icrit=2.50uA)", file=f)
# write internal horizontal JJs in JJA
print("# horizontal JJs", file=f)
for i in range(1,M+1):
    for j in range(1, N):
        print("B%d%dh\t%d\t%d\t\tjjmod" % (i, j, 2*(i-1)*N + j, 2*(i-1)*N + j + 1), file=f)
        print("P%d%dh\t%d\t%d\t\t DC %g" % (i, j, 2*(i - 1)*N + j+1, 2*(i-1)*N + j + 2, frustration * 2 * np.pi), file = f)
# write internal vertical JJs in JJA
print("# vertical JJs", file=f)
for j in range(1,N+1):
    for i in range(1,M):
        print("B%d%dv\t%d\t%d\t\tjjmod" % (i, j, (2*i-1)*N + j, (2*i-1)*N + j + N), file=f)

# write horizontal junctions to right terminal (GND)
print("# horizontal JJs to right terminal", file=f)
for i in range(1,M+1):
    print("BR%d\t%d\t%d\t\tjjmod" % (2*i, 2*i*N, 0), file=f)
    
# write horizontal junctions to right terminal (GND)
print("# horizontal JJs to left terminal (node M*N+1)", file=f)
for i in range(1,M+1):
    print("BL%d\t%d\t%d\t\tjjmod" % (2*i, N*M+1, (2*i-1)*N + 1), file=f)


print(".tran 0.1p %g 0 0.1p" % (2*t), file=f)
print(".print DEVI IDC", file=f)
print(".print DEVV %d" % (M*N+1), file=f)
f.close()

    
