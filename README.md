# 20220213_hpl-lab
High-Performance Linpack benchmark solves uniformly random system of linear equations to determine the system’s floating-point computational power. The results of HPL is the optimistic performance of the system, which is usually not match in real-world applications.

The linear equations are generated by HPL parameters N, NB, P, and Q.
  N is the problem size
  NB is the the block size
  P is the number of rows
  Q is the number of columns
  
<img width="468" alt="image" src="https://user-images.githubusercontent.com/11095946/153784916-f6468e90-9f78-4e48-8387-11cf9883e9f0.png">

N is the matrix size (# of equations)
• Floating point work varies as N3
, communication volume varies as N2
, so the
computation:communication ratio improves as N increases
• 2X increase in problem size → up to 8X increase in run time
• Memory usage in GiB is approximately 8*N2
/10243
–Each node has 256 GiB of memory but Slurm is configured to allow jobs to use ~80% of that
–If you want to size a 2-node job to use approximately 70% of memory, then N = sqrt(0.7 * 2 * 256 * 10243
/
8) = 219325 (does it help for N to be a multiple of NB?)
–Make sure N isn’t too small, since results of parameterization experiments for small N may not be the
same as those for large N

