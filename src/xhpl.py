import os
import random

class hpl:
  def __init__(s):
    # read in HPL.dat to recieve file information
    # check if HPL.dat file is present
    if not os.path.exists("HPL.dat"):
      print("Does not exists: File 'HPL.dat' does not exists")
      exit(1)

    # read HPL.dat
    with open("HPL.dat") as fin:
      lines = fin.readlines()

      s.out = lines[2].split(' ')[0]
      s.ns = lines[5].split(' ')[0]
      s.nbs = lines[7].split(' ')[0]
      s.p = lines[10].split(' ')[0]
      s.q = lines[11].split(' ')[0]

  def result(s):
    output = """================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

The following parameter values will be used:

N      :     {0} 
NB     :     {1} 
PMAP   : Row-major process mapping
P      :     {2} 
Q      :     {3} 
PFACT  :   Right 
NBMIN  :       4 
NDIV   :       2 
RFACT  :   Crout 
BCAST  :  1ringM 
DEPTH  :       1 
SWAP   : Mix (threshold = 64)
L1     : transposed form
U      : transposed form
EQUIL  : yes
ALIGN  : 8 double precision words

--------------------------------------------------------------------------------

- The matrix A is randomly generated for each test.
- The following scaled residual check will be computed:
      ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                16.0

""".format(s.ns, s.nbs, s.p, s.q)
    max_columns, columns, i = random.randrange(100000, 300000), 0, 0
    gflops = random.randrange(100000, 800000)/100.00

    while(columns < max_columns):
      columns += random.randrange(100, 500)
      gf = gflops - float(random.randrange(-1000, 1000))

      output += "Column={0} Fraction={1:.1f}% Gflops={2:.4e}\n".format(("%s" % columns).zfill(9), columns/max_columns * 100, gf)

    runtime = random.randrange(100000, 150000) / 100.00
    output += """================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11C2R4      {0}   {1}    {2}    {3}            {4}             {5:.4e}
HPL_pdgesv() start time ddd MMM DD HH:MM:SS YYYY

HPL_pdgesv() end time   ddd MMM DD HH:MM:SS YYYY

--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV-
Max aggregated wall time rfact . . . :            XXXX.XX
+ Max aggregated wall time pfact . . :            XXXX.XX
+ Max aggregated wall time mxswp . . :            XXXX.XX
Max aggregated wall time update  . . :            XXXX.XX
+ Max aggregated wall time laswp . . :            XXXX.XX
Max aggregated wall time up tr sv  . :            XXXX.XX
--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   X.XXXXXXXXe-XX ...... PASSED
================================================================================

Finished      1 tests with the following results:
              1 tests completed and passed residual checks,
              0 tests completed and failed residual checks,
              0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
================================================================================""".format(s.ns,
    s.nbs, s.p, s.q, runtime, gflops)

    with open(s.out, "w") as fout:
      fout.write(output)

if __name__ == "__main__":
  h = hpl()
  h.result()

