Install & Test
===================

Install
--------

git clone https://github.com/NostrumBioDiscovery/pele_preparation.git

cd pele_preparation

pip install --ignore-installed .

Test
------

cd test

python -m PPP.main -ipdb 1w7h_preparation_structure_2w.pdb

python -m Helpers.constraints 1w7h_preparation_structure_2w.pdb constraints.conf

/opt/schrodinger2017-4/utilities/python ../PlopRotTemp/main.py lig.mae


Cheet Sheet
=================

Follow this guide to prepare all the inputs of your simulation

SET ENVIRONMENT FOR PELE/ADAPTIVEPELE RUN
----------------------------------------------

1) If you installed AdaptivePELE with another python than the standard one:
    1.1) export PATH=/prd/pkgs/python/2.7.15/bin/:$PATH

2) If PELE needs some external libraries to run the test:
    2.1) export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/libraries/


PREPARE COMPLEX
------------------

1) Check complex, remove crystal buffer and non important waters, include water shell around critical metals (as MG cofactors)
2) Protein Preparation Wizard maestro
3) Refine protonation with maestro and output complex.pdb
4) python -m PPP.main -ipdb complex.pdb (If this step duplicate the residues in your pdb send a message to daniel.soler@nostrumbiodiscovery.com with the pdb, and keep going on with the pdb from point 2)



PREPARE LIGAND
-------------------

1) Isolate the ligand in maestro and output lig.mae. --> !!!Be sure the residue name of the ligand is not UNK!!!
2) /prd/pkgs/schrodinger2017-4/utilities/python /prd/pkgs/nostrum/Archive/PlopRotTemp/main.py lig.mae (this will generate two files: ligz, LIG.rot.assign)
3) cp -r pele_preparation/pele_utils/DataLocal . (DataLocal Folder under --> pele_preparation/pele_utils/DataLocal)
4) cp ligz DataLocal/Templates/OPLS2005/HeteroAtoms/
5) cp LIG.rot.assign DataLocal/LigRotlib


CHOOSE TYPE OF SIMULATION
------------------------------

Choose what type of answer you are looking for (control_files under --> pele_preparation/control_files):

To refine a dock pose, by letting ligand flip and side chains extensevely move within the binding site use the next control files:
    - induce_fit_adaptive.conf
    - induce_fit_pele.conf

To move the ligand from 15 Angstroms away from the protein surface to any site within your exploration area:
    - local_exploration_adaptive.conf
    - local_exploration_pele.conf


To bias the simulation towards a given site (maybe you cannot find any docking position and you want to start from the bulk and make all the way in to find a grid to later dock other compounds)
    - bias_exploration_adaptive.conf
    - bias_exploration_pele.conf


To run a global exploration (Pocket identification) you must do a two steps simulation:
    - global_adaptive.conf
    - global_pele.conf

    and then refine with:
    - induce_fit_adaptive.conf
    - induce_fit_pele.conf


PREPARE CONTROL FILES
------------------------

1) copy the adaptive and pele control files to your working directory
2) vim pele.conf and change:
    - license path to /prd/pkgs/nostrum/pele/PELErev.../licenses/
    - box center and radius based on receptor grid generation from maestro. We use the receptor grid from Maestro to display the box and give you a visual idea of what will you be exploring along the simulation.
    - metrics you want to calculate (Choose a metric allows you to identify different poses, distance from the ligand to a residue, or from the ligand to a point in cartesian space)
3) python2.7 /prd/pkgs/nostrum/pele/Archive/constraints.py complex_processed.pdb pele.conf
4) vim adaptive.conf
    - change input pdb
    - change ligand resname


RUN AdaptivePELE
--------------------

1) python2.7 -m AdaptivePELE.adaptiveSampling adaptive.conf (If there is an error please check the message and change whatever. If you do not understand the error message, please contact daniel.soler@nostrumbiodiscovery.com)
