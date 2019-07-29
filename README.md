Install & Test
===================

Install
--------

git clone https://github.com/NostrumBioDiscovery/pele_preparation.git

cd pele_preparation

pip install .

Test
------

cd test

python -m PPP.main -ipdb 1w7h_preparation_structure_2w.pdb

python -m Helpers.constraints 1w7h_preparation_structure_2w.pdb constraints.conf

/opt/schrodinger2017-4/utilities/python ../PlopRotTemp/main.py lig.mae

