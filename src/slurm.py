import os
import re
import sys


if __name__ == "__main__":
  # check parameters for file name
  if len(sys.argv) != 2:
    print("Usage: python slurm.py FILENAME")
    exit(1)

  bat = sys.argv[1]

  if not os.path.exists(bat):
    print("Does not exists: File '{}' does not exists.".format(bat))
    exit(1)
  else:
    slurm_out = None
    srun_out = None
    with open(bat, "r") as fin:
      content = fin.readlines()

      for line in content:
        if "#SBATCH -o" in line:
          slurm_out = line.split(' ')[-1]
        if "| tee" in line:
          srun_out = line.split(' ')[-1]

    os.system("python srun.py")
    os.system("touch {}".format(srun_out))
    os.system("touch {}".format(slurm_out))
