# HPL Lab
High-Performance Linpack benchmark solves uniformly random system of linear equations to determine the system’s floating-point computational power. The results of HPL is the optimistic performance of the system, which is usually not match in real-world applications.

The linear equations are generated by HPL parameters N, NB, P, and Q.
- N is the problem size
- NB is the the block size
- P is the number of rows
- Q is the number of columns
  
<img width="468" alt="image" src="https://user-images.githubusercontent.com/11095946/153784916-f6468e90-9f78-4e48-8387-11cf9883e9f0.png">

## HPL.dat and slurm.bat
  ### [HPL.dat](HPL.dat)
  HPL.dat provides HPL with the parameters it should use to run. Details on the HPL.dat file can be found on [netlib.org](https://www.netlib.org/benchmark/hpl/tuning.html).
  ```
    HPLinpack benchmark input file
    Innovative Computing Laboratory, University of Tennessee
    HPL.out      output file name (if any) 
    6            device out (6=stdout,7=stderr,file)
    1            # of problems sizes (N)
    82897        Ns
    1            # of NBs
    128          NBs
    0            PMAP process mapping (0=Row-,1=Column-major)
    1            # of process grids (P x Q)
    16           Ps
    16           Qs
    16.0         threshold
    1            # of panel fact
    2            PFACTs (0=left, 1=Crout, 2=Right)
    1            # of recursive stopping criterium
    4            NBMINs (>= 1)
    1            # of panels in recursion
    2            NDIVs
    1            # of recursive panel fact.
    1            RFACTs (0=left, 1=Crout, 2=Right)
    1            # of broadcast
    1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
    1            # of lookahead depth
    1            DEPTHs (>=0)
    2            SWAP (0=bin-exch,1=long,2=mix)
    64           swapping threshold
    0            L1 in (0=transposed,1=no-transposed) form
    0            U  in (0=transposed,1=no-transposed) form
    1            Equilibration (0=no,1=yes)
    8            memory alignment in double (> 0)
  ```
  
  
  
  ### [slurm.bat](slurm.bat)
  Slurm is a workload manager for cluster machines. 60% of the worlds Top 500 supercomputers use slurm, so being well-versed in it's operations can be a huge advantage when looking for a job in the field. You can learn more about Slurm [here](https://slurm.schedmd.com/overview.html). Slurm.bat is the slurm batch script that sets enviroment variables and actually runs HPL on the cluster. Below is an example of a slurm batch script.
  
  ```bash
    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -p hpl
    #SBATCH --ntasks-per-node=128
    #SBATCH --exclusive
    #SBATCH -t 0:30:00
    #SBATCH -o slurm-output.log

    cd $SLURM_SUBMIT_DIR

    export OMP_NUM_THREADS=1
    export OMP_PLACES=cores
    export OMP_PROC_BIND=close

    python srun_hpl.py | tee hpl.out
  ```
</details>

The purpose of this lab is to create a script that will generate different HPL parameters. You may use any programming language and IDE to generate this script, as long as:
- You are able to make changes to the file structure
  - i.e. read and write to files and make directories
- You are able to run linux commands from the script
```python
  # python system call to create directory called runs in the test directory
  os.system('mkdir test/runs')
```
- This program assumed your working directory looks like this:
```
working_direcotry
|- your_program.whatever
|- xhpl
```

## Prerequisites
- This lab requires the following:
  - python installed (>= version 2.6)
  - [srun.py](src/srun.py) installed in working directory
## Determine HPL Parameters
<details>
  <summary> Create a method that determines NB.</summary>
  
  - NB is the block size:
    - Want NB to be large enough to give good DGEMM performance
    - If NB is too large, the cache efficiency begins to drop
    - Different DGEMM libraries may have different optimal NB values, but usually that value is a multiple of 8
     - Hint: restrict your testing to 64 <= NB <= 320
  - This method should return an array of integers.
</details>

<details>
  <summary>Create a method that determines N.</summary>

  - N is the matrix size (# of equations):
    - Floating point work varies as N<sup>3</sup>, communication volume varies as N<sup>2</sup>, so the computation:communication ratio improves as N increases
    - 2X increase in problem size → up to 8X increase in run time
    - Memory usage in GiB is approximately 8*N<sup>2</sup>/10243
    - Each node has 256 GiB of memory but Slurm is configured to allow jobs to use ~80% of that
    - If you want to size a 2-node (nnodes = 2) job to use approximately 70% (mem_perc = .70) of memory, then N = sqrt(mem_perc * nnodes * 256 * 10243/8) = 219325
      - Does it help for N to be a multiple of NB?
    - Make sure N isn’t too small, since results of parameterization experiments for small N may not be the same as those for large N
  - This method should return an array of integers.
</details>

<details>
  <summary>Create a method that determines P and Q.</summary>
  
  - P and Q are the process grid dimensions
    - Need P * Q = # of MPI ranks
    - The process grid shouldn’t be too rectangular (e.g., 1x128 and 128x1 are not likely to be good)
    - Usually P <= Q with Q/P <= 4 works well, but it’s worth experimenting with other decompositions
    - For HPL, it’s best to utilize all the cores, so # of MPI ranks * # of OpenMP threads should equal the total number of cores in your job
      - Note that for HPL it is generally *not* beneficial to use both a core and its hyperthread partner for computation – one should be left idle
  - This method should return _two_ arrays of integers
</details>

## Create an HPL.dat file with above parameters
Your program should call each method created above, and creating an "HPL.dat" file. Below is the pseudocode in Python:
- If your program runs correctly, you will be creating ALOT of new files. I would recommend developing a file structure to organize all of the outputs. Output files are:
  - A log file generated by slurm when submitting a batch request
  - "tee" command also generates a log file based off of the "sruns" output
  - You will be creating an .dat file with the HPL parameters
  - You will be creating a .bat file with the slurm parameters
  - xhpl will generate the results of the test 

```python
  # MPI ranks is equal to the amount of CPUs per node. nnode is number of nodes
  mpi_ranks = nnodes * 128
  P, Q = determine_PandQ(mpi_ranks)
  NB = determine_NB()
  
  for nb in NB:
    
    N = determine_N(nb)
    for n in N:
    
      for i in range(0, len(P)):
        p = P[i]
        q = Q[i]
        
        # the output filename should look like this: "20220215R084500-N1_n128000_nb128_p16_q16"
          # that date is the February 15, 2022 at 08:45:00, Eastern standard time
        # timestamp is important when running multiple scripts so that you can troubleshoot errors and organize file
        timestamp = format_date(YYYYMMDDRHHMMSS)    # where R is the timezone "EST"
        parameter = format_param()                  # Should have the following format "N1_n128000_nb128_p16_q16"; where N is number of nodes
        output_filename = timestamp+parameter # see above for directions
   
        # create an "HPL.dat" file for each combination of parameters, but name it "output_filename".dat and write it to a directory
        create_dat(output_filename+".txt", nb, n, p, and q)
        
        sleep(1) # this will pause the program for a second so that timestamp is different
```
## Create an slurm.dat file
Using the slurm.bat file example provided above, create a batch file make the following changes:
- Note: the {} denotes variables previously used in the HPL.dat file
- When calling the ./xhpl, xhpl needs an HPL.dat file in the same directory so it knows what parameters to run
1. #SBATCH -o {output_filename}\_sbatch.log
2. ... | tee {output_filename}\_srun.out
