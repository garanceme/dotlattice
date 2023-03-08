# dotlattice

Dot-lattice feature (orientation) extraction project by Garance Merholz - 8 March 2023

Project created under Ubuntu 20.04 with Python 3.9 
File system based on Patrick Mineault's "true neutral cookiecutter" template: https://goodresearch.dev/setup.html

# Instructions to run:

Linux (Ubuntu 22.04):
- I recommend installing Anaconda and pygame if you don't have them, to have all necessary libraries; https://docs.conda.io/projects/conda/en/stable/user-guide/install/linux.html and https://www.pygame.org/wiki/GettingStarted
- In a terminal, cd to the dotlattice folder
	- create a dotlattice environment: $ conda create --name dotlattice python=3.9
	- activate the environment: $ conda activate dotlattice
	- install libraries: $ conda install pandas numpy scipy matplotlib seaborn
- Open the Anaconda Navigator > Environments > dotlattice; click on Channels > Add... > conda-forge
- In a new terminal cd to dotlattice, activate dotlattice environment again and install pygame: $ python -m pip install -U pygame==2.2.0 --user
- Open the file src/parameters.py with a text editor and update path_to_expfolder
- Run the file: run_experiment.py (tested with Spyder 5.4.0 and terminal) (had to move to main folder not scripts, to be able to see the other folders)


Mac:

Windows:

