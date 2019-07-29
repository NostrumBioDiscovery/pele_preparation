##############################
##CHEET SHEET PELE##
##############################


#SET ENVIRONMENT FOR PELE/ADAPTIVEPELE RUN#
###########################################

1) export PATH=/prd/pkgs/python/2.7.15/bin/:$PATH
2) export LD_LIBRARY:$LD_LIBRARY:/need/it/libraries

#PREPARE COMPLEX#
#################

1) Check complex, remove crystal buffer and non important waters, include water shell around critical metals (as MG cofactors)
2) Protein Preparation Wizard maestro
3) Refine protonation with maestro and output complex.pdb
4) python2.7 -m PPP.main -ipdb complex.pdb (If this step duplicate the residues in your pdb send a message to daniel.soler@nostrumbiodiscovery.com and keep with the pdb from point 2)



#PREPARE LIGAND#
################

1) Isolate the ligand in maestro and output lig.mae. !!!Be sure the residue name of the ligand is not UNK!!!
2) /prd/pkgs/schrodinger2017-4/utilities/python -m PlopRotTemp.main lig.mae (this will generate two files: ligz, LIG.rot.assign)
3) cp -r /prd/pkgs/nostrum/pele/Archive/PELE_files/DataLocal/ .
4) cp ligz DataLocal/Templates/OPLS2005/HeteroAtoms/
5) cp LIG.rot.assign DataLocal/LigRotlib

#CHOOSE TYPE OF SIMULATION#
###########################

Choose what type of answer you are looking for:

To refine a dock pose, by letting ligand and side chains extensevely flip and move within the binding site use the next control files:

    - induce_fit_adaptive.conf
    - induce_fit_pele.conf

To move the ligand from 15 Angstroms away from the protein surface to any site within your mid size exploration area:
    - local_exploration_adaptive.conf
    - local_exploration_pele.conf


To bias the simulation towards a given site (maybe you cannot find any docking position and you want to start from the bulk and make all the way in to find a grid to later dock other compounds)

    - bias_exploration_adaptive.conf
    - bias_exploration_pele.conf

