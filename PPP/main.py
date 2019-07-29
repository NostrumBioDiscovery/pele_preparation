#!/bin/python
import sys
from prody import *

from adjustments_module import WritingAtomNames, FixStructureResnames, FixAtomNames, SolveClashes
from checks_module import CheckMutation, CheckClashes
from checks_module import CheckStructure, CheckforGaps
from global_processes import ParseArguments, FindInitialAndFinalResidues, PDBwriter, RenumberStructure
from hydrogens_addition import FixStructure
from mutational_module import Mutate
from global_variables import coordination_geometries

__author__ = 'jelisa'

"""
This block adds the hid, hip, and hie residues to prody. Otherwise this would consider
this aminoacids as heteroatoms.
"""
addNonstdAminoacid('HID', 'aromatic', 'basic', 'cyclic', 'large', 'polar', 'surface')
addNonstdAminoacid('HIE', 'aromatic', 'basic', 'cyclic', 'large', 'polar', 'surface')
addNonstdAminoacid('HIP', 'aromatic', 'basic', 'cyclic', 'large', 'polar', 'surface')
addNonstdAminoacid('CYT', 'neutral', 'acyclic', 'medium', 'polar', 'buried')
addNonstdAminoacid('LYN', 'neutral', 'acyclic', 'large', 'polar', 'buried')


def main(input_pdb, pdb_resolution, output_pdb="", no_gaps_ter=False, charge_terminals=False, make_unique=False,
         remove_terminal_missing=False, mutant_multiple=False, mutation=""):
    try:
        initial_structure = parsePDB(input_pdb)
    except IOError:
        print "The file '{}' isn't a valid file\nCheck that it does exist and try again.".format(input_pdb)
        sys.exit()
    initial_residue, final_residue = FindInitialAndFinalResidues(initial_structure)
    # ff_parameters = ReadForceFieldParameters(force_field)

    print "* Checking for insertion codes."
    insertion_codes = [icode for icode in initial_structure.getIcodes() if icode]
    if insertion_codes:
        print "  * Due to the insertion codes the structure will be RENUMBERED starting from 1 for each chain.\n" \
              "  ** Otherwise PELE would fail."
        structure2use = RenumberStructure(initial_structure)
    else:
        structure2use = initial_structure
    print "* Checking for gaps."
    gaps, not_gaps = CheckforGaps(structure2use, pdb_resolution)
    if gaps is None and not_gaps is None:
        print "WARNING: Problems when checking for gaps, so don't trust the existence of gaps."
        gaps, not_gaps = {}, {}
    print "* Checking and Fixing the Residues Names:"
    structure2use = FixStructureResnames(structure2use, make_unique)
    print "* Checking and fixing the Atoms Names:"
    structure2use = FixAtomNames(structure2use, gaps, not_gaps)
    print "* Checking the structure for missing atoms:"
    residues2fix, residues2remove, metals2coordinate, residues_without_template = CheckStructure(structure2use, gaps,
                                                                                                 not_gaps,
                                                                                                 charge_terminals,
                                                                                                 remove_terminal_missing)
    if residues2fix:
        print '* Placing the missing atoms and removing the extra atoms:'
        structure2use = FixStructure(structure2use, residues2fix, gaps, charge_terminals)

    if not mutation:
        print 'Writing the structure to {}'.format(output_pdb[0])
        if make_unique:
            ligand_chain = structure2use.select("chain {}".format(make_unique))
            if ligand_chain:
                not_proteic_ligand = structure2use.select("chain {}".format(make_unique)).hetero
            else:
                not_proteic_ligand = None
            PDBwriter(output_pdb[0], WritingAtomNames(structure2use), make_unique, residues2remove,
                      no_gaps_ter, not_proteic_ligand, gaps, not_gaps)
        else:
            not_proteic_ligand = None
            PDBwriter(output_pdb[0], WritingAtomNames(structure2use), make_unique, residues2remove,
                      no_gaps_ter, not_proteic_ligand, gaps, not_gaps)

        return residues_without_template, gaps, metals2coordinate
    else:
        clashes = []
        mutated_structure = None
        for mutation, output_file in zip(mutation, output_pdb):
            print '* Checking the mutation:'
            print " Mutation: {0[ini_resname]} {0[chain]} {0[resnum]} {0[fin_resname]}".format(mutation)
            correct_mutation = CheckMutation(structure2use, mutation)
            if not correct_mutation:
                exit_message = "The mutation was incorrect, check your parameters.\n" \
                               "The checked structure will be written to {}".format(output_file)
                PDBwriter(output_file, WritingAtomNames(structure2use), make_unique, gaps, no_gaps_ter, not_gaps)
                continue
            else:
                print "Output_file name: {0}".format(output_file)
                mutated_structure, zmatrix = Mutate(structure2use, mutation)
                if not mutant_multiple:
                    if mutation[0]['fin_resname'] in ["ALA", "GLY"]:
                        print "The ALA and the GLY don't have any rotamer to try."
                    else:
                        print "Checking Clashes:"
                        try:
                            clashes = CheckClashes(mutated_structure, mutation, zmatrix,
                                                   initial_residue, final_residue)
                        except ValueError:
                            pass
                        else:
                            if not clashes:
                                print "Structure without clashes."
                            else:
                                mutated_structure = SolveClashes(mutated_structure, clashes,
                                                                 mutation, zmatrix,
                                                                 initial_residue, final_residue)
                    mutated_structure.setTitle("mutated structure")
                    PDBwriter(output_file, WritingAtomNames(mutated_structure), make_unique, gaps, no_gaps_ter,
                              not_gaps)
                else:
                    print "Multiple mutations at the same time are still under development."
                    structure2use = mutated_structure
        if mutant_multiple and mutated_structure is not None:
            PDBwriter(output_pdb, WritingAtomNames(mutated_structure), gaps, not_gaps, no_gaps_ter)
    # return residues_without_template, gaps, metals2coordinate


if __name__ == '__main__':
    arguments = ParseArguments()
    if arguments is None:
        sys.exit()
    else:
        main(arguments.input_pdb, arguments.pdb_resolution, output_pdb=arguments.output_pdb,
             no_gaps_ter=arguments.no_gaps_ter, charge_terminals=arguments.charge_terminals,
             make_unique=arguments.make_unique, remove_terminal_missing=arguments.remove_terminal_missing,
             mutant_multiple=arguments.mutant_multiple, mutation=arguments.mutation)
