'''
Created on 15 Jun 2015

@author: marinos
'''
import unittest

import Analyses

class Test(unittest.TestCase):
    
    mujava_result_dir = '/home/marinos/Workbench/mujava/result'
    experiment_dir = '/home/marinos/Desktop/bisect'
    
    include_methods=[]

    def testBisectTed(self):
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, self.include_methods)
        mutated_class = 'Bisect'
        mutated_method = 'double_sqrt(double)'
        
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 135)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 11)
        
        self.assertTrue('AOIS_43' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_44' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_47' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_48' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_59' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_60' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_73' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_74' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_79' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_80' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIU_4' in equiv_muts_per_class[mutated_class][mutated_method])
        
        
    def testBisectNed(self):
        mutated_class = 'Bisect'
        mutated_method = 'double_sqrt(double)'
        
        muts_per_class, equiv_muts_per_class = Analyses.ned(self.mujava_result_dir, self.include_methods)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 0)
