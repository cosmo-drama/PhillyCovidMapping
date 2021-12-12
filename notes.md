## Package Management
we will use a combination of conda and pip to manage our packages within 1 virtual environment. 

you'll want to run the following in a terminal to create a conda environment with the required packages: 

```bash
conda create --name PhillyCovid-env --file requirements.txt
```
once this is complete, run `conda activate PhillyCovid-env` to activate the environment. 

If you add any packages to this environment, you should run the following: 

```bash
conda list --explicit > requirements.txt
```
This will update the requirements.txt file with your added packages so that I can create the same environment on my system. 
