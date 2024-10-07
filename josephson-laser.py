#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import subprocess

cir_filename = 'josephson-laser-josim.py.cir'
cir_file = open(cir_filename, 'w')

# f0: resonance frequency of half-wave mode L = λ/2
# ZL: load impedance at right end of transmission line resonator
def gen_resonator(Z0, N, f0, ZL=1e6): 
    # V(x,t) = exp(iωt +- γx)
    # γ = iω sqrt(L * C)
    # 
    sqrt_LC = 1 / (2* N * f0)
    L = sqrt_LC * Z0
    C = L / Z0**2
    print("L = %g, C = %g\n" % (L, C))
    print(".subckt RESONATOR 1", file=cir_file)
    for i in range(1,N):
        print("L%d   %d    %d      %g" % (i, i, i+1, L), file=cir_file)
        print("C%d   %d     0      %g" % (i, i+1, C), file=cir_file)
    print("RL   %d    0      %g" % (N, ZL), file=cir_file)
    print(".ends", file=cir_file)


run_time = 500e-9
delta_t = 2e-12

N_res=200
f0_res = 10e9
Z0_res = 50
L_source = 10e-9
R_source = 100
Ic = 50e-9

CJ = 1e-15
RN = 20*Z0_res
R0 = RN
V_max = 1 * Ic * (R_source + RN)

gen_resonator(Z0_res, N_res, f0_res)

print("VDC  0    1       pwl(0     %g    %g    0)" % (V_max, run_time), file=cir_file)
print("RS   1      2      %g" % R_source, file=cir_file)
print("LS   2      3      %g" % L_source, file=cir_file)
print("X1 RESONATOR 3", file=cir_file)
print("B1   3       0     jjmod", file=cir_file)
print(".model jjmod jj(rtype=1, vg=2.8e-3, cap=%g, r0=%g, rn=%g, icrit=%g)" % (CJ, R0, RN, Ic), file=cir_file)
print(".tran %g %g" % (delta_t, run_time), file=cir_file)
print("""
.print DEVV VDC
.print DEVI VDC
.print DEVV B1
.print DEVI B1
.print PHASE B1
""", file=cir_file)

cir_file.close() # flush output


output_csv = cir_filename + '.csv'
subprocess.run(["josim-cli", cir_filename, '-o', output_csv])


data = np.genfromtxt(output_csv, delimiter=",", skip_header=1)
print("data shape = ", data.shape)
tstep = data[1,0] - data[0,0]
q = int((1/f0_res) / tstep) * 3

print("tstep = ", tstep)
print("q = ", q)

data = signal.decimate(data, q, axis=0)
time_vals = data[:,0]
phi0 = 2.0678338484619295e-15

v_vals = data[:,3]
i_vals = data[:,4]
phase_vals = data[:,5]
v_vals_phase = np.gradient(phase_vals) / np.gradient(time_vals) * phi0 / (2*np.pi)
plt.plot(time_vals, -v_vals_phase, label="V")
plt.plot(time_vals, -i_vals, label="I")
plt.plot(time_vals, np.gradient(phase_vals), label="grad phi")
plt.grid()
plt.legend()
plt.show()

plt.ylabel('V / (Φ_0 * f0)')
plt.grid()
plt.plot(-v_vals / (phi0 * f0_res), -i_vals, '.')
plt.show()
