#!/usr/bin/env python3
import numpy as np
f = open('JJA.cir', 'w')
frustration = 0.1

# current in x-direction
Nx = 50
Ny = 50
Ic = 500e-9
Rn = 50
Imax = Ny * Ic * 1.1
t = 10e-9
# current source
print("IDC\t0\t%d\tpwl(0 0 %g %g %g 0)" %( Nx*Ny+1, t, Imax, 2*t), file=f)
print(".model jjmod jj(rtype=1, vg=200uV, cap=1fF, r0=%g, rN=%g, icrit=%g)" % (Rn, Rn, Ic), file=f)
print(".spread B=0.1", file=f)
def node_index(ix, iy):
    return ix + Nx*iy +1
def right_neighbor(ix, iy):
    return node_index(ix+1, iy)

def upper_neighbor(ix, iy):
    return node_index(ix, iy+1)

print("# horizontal JJs", file=f)
# write internal horizontal JJs in JJA
for iy in range(Ny):
    for ix in range(Nx-1): # column index
        print("B%d_%dh\t%d\t%d\t\tjjmod" % (ix, iy, node_index(ix, iy), right_neighbor(ix, iy)), file=f)
        
# write internal vertical JJs in JJA
print("# vertical JJs", file=f)
for ix in range(Nx):
    for iy in range(Ny-1):
        print("B%d_%dv\t%d\t%d\t\tjjmod" % (ix, iy, node_index(ix,iy), upper_neighbor(ix, iy)), file=f)

# write horizontal junctions to right terminal (GND)
print("# horizontal JJs to right terminal", file=f)
for iy in range(Ny):
    ix = Nx-1
    print("BR%d\t%d\t%d\t\tjjmod" % (iy, node_index(ix, iy), 0), file=f)
    
    
# write horizontal junctions to right terminal (GND)
print("# horizontal JJs to left terminal (node M*N+1)", file=f)
for iy in range(Ny):
    ix = 0
    print("BL%d\t%d\t%d\t\tjjmod" % (iy, Nx*Ny+1, node_index(ix, iy)), file=f)


print(".tran 1p %g 0 1p" % (2*t), file=f)
print(".print P(%d)" % (Nx*Ny+1), file=f)
print(".print DEVI IDC", file=f)
print(".print P(B0_0h)", file=f)
print(".print P(B0_2h)", file=f)
      
print(".print DEVV %d" % (Nx*Ny+1), file=f)
f.close()

    
