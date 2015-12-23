'''
Created on 25 Jun 2015

@author: marinos
'''
import unittest

import Analyses


class Test(unittest.TestCase):

    mujava_result_dir = '/home/marinos/Workbench/mujava/result'
    experiment_dir = '/home/marinos/Desktop/commons'
    
    include_methods=['java.lang.String_capitalize(java.lang.String,char)', 'java.lang.String_wrap(java.lang.String,int,java.lang.String,boolean)']

    def testCommonsCapitalizeTed(self):   
         
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, self.include_methods)
        mutated_class = 'WordUtils'
        mutated_method = self.include_methods[0]
         
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 69)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 2)
          
        self.assertTrue('AOIS_95' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_96' in equiv_muts_per_class[mutated_class][mutated_method])
         
    def testCommonsWrapTed(self):   
     
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, self.include_methods)
        mutated_class = 'WordUtils'
        mutated_method = self.include_methods[1]
         
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 198)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 12)
          
        self.assertTrue('AOIS_41' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_42' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_47' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_48' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_75' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_76' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_81' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_82' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_83' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_84' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_89' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_90' in equiv_muts_per_class[mutated_class][mutated_method])

        
    def testCommonsNed(self):
        mutated_class = 'xorg.apache.commons.lang.WordUtils'
        
        muts_per_class, equiv_muts_per_class = Analyses.ned(self.mujava_result_dir, self.include_methods)
        
        self.assertTrue(len(equiv_muts_per_class[mutated_class][self.include_methods[0]]) == 0)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][self.include_methods[1]]) == 0)
        
        
        
        
        
        
