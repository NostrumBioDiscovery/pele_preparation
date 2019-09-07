Install & Test
===================

Install
--------

git clone https://github.com/NostrumBioDiscovery/pele_preparation.git

cd pele_preparation

pip install --ignore-installed .

yum install gcc gcc-c++ kernel-devel python-devel tkinter python-pmw glew-devel \
  freeglut-devel libpng-devel freetype-devel libxml2-devel glm-devel

git clone https://github.com/schrodinger/pymol-open-source.git

cd pymol-open-source

python setup.py install --home=/installation/path/

export PYTHONPATH=$PYTHONPATH:/installation/path/lib/python/


Test 
------------

cd tests/test_helpers

python -m PPP.main -ipdb 1w7h_preparation_structure_2w.pdb

python -m Helpers.constraints 1w7h_preparation_structure_2w.pdb constraints.conf

export SCHRODINGER_PYTHONPATH=" "

export PYTHONNOUSERSITE=" "

/opt/schrodinger2017-4/utilities/python ../../PlopRotTemp/main.py lig.mae


