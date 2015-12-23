'''
Created on 15 Jun 2015

@author: marinos
'''
import unittest

import Analyses


class Test(unittest.TestCase):

    mujava_result_dir = '/home/marinos/Workbench/mujava/result'
    experiment_dir = '/home/marinos/Desktop/tr_example'
    
    include_methods=[]

    def testTriangleTed(self):   
        
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, self.include_methods)
        mutated_class = 'Triangle'
        mutated_method = 'int_classify(int,int,int)'
        
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 354)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 21)
        
        self.assertTrue('AOIS_129' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_130' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_133' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_134' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_137' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_138' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_139' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_140' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_25' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_26' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_37' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_38' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_49' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_50' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_77' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_78' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_81' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_82' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_83' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_84' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIU_2' in equiv_muts_per_class[mutated_class][mutated_method])
        
    def testTriangleNed(self):
        mutated_class = 'tr.Triangle'
        mutated_method = 'int_classify(int,int,int)'
        
        muts_per_class, equiv_muts_per_class = Analyses.ned(self.mujava_result_dir, self.include_methods)
        
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 0)
