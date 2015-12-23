'''
Created on 8 Jul 2015

@author: marinos
'''
import unittest

import Analyses


class Test(unittest.TestCase):

    mujava_result_dir = '/home/marinos/Workbench/mujava/result'
    experiment_dir = '/home/marinos/Desktop/jodatime'
    
    include_methods = ['long_add(long,int)']
    
    def testAddTed(self):
         
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, [self.include_methods[0]])
        mutated_class = 'BasicMonthOfYearDateTimeField'
        mutated_method = self.include_methods[0]
         
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 257)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 22)
        
        self.assertTrue('AOIS_13' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_14' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_27' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_28' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_47' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_48' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_67' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_68' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_71' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_72' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_91' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_92' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_97' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_98' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_119' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_120' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_121' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_122' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_123' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_124' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_127' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_128' in equiv_muts_per_class[mutated_class][mutated_method])
          

         
    def testAddNed(self):
        mutated_class = 'org.joda.time.chrono.BasicMonthOfYearDateTimeField'
        
        muts_per_class, equiv_muts_per_class = Analyses.ned(self.mujava_result_dir, self.include_methods)
        
        self.assertTrue(len(equiv_muts_per_class[mutated_class][self.include_methods[0]]) == 0)
