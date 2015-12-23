'''
Created on 25 Jun 2015

@author: marinos
'''
import unittest

import Analyses


class Test(unittest.TestCase):

    mujava_result_dir = '/home/marinos/Workbench/mujava/result'
    experiment_dir = '/home/marinos/Desktop/pamvotis'
    
    include_methods=['boolean_removeNode(int)', 'void_addNode(int,int,int,int,int,int)']
    
    def testSimulatorRemoveNodeTed(self):
          
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, [self.include_methods[0]])
        mutated_class = 'Simulator'
        mutated_method = self.include_methods[0]
          
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 55)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 6)
           
        self.assertTrue('AOIS_2292' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2291' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2297' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2302' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2298' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2301' in equiv_muts_per_class[mutated_class][mutated_method])
    
    
    def testSimulatorAddNodeTed(self):
         
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, [self.include_methods[1]])
        mutated_class = 'Simulator'
        mutated_method = self.include_methods[1]
         
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 318)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 31) # Did not detect: LOI_658 AOIU_257 of the dd case
          
        self.assertTrue('AORB_950' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AORB_954' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2267' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AORB_949' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIU_256' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2258' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2268' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2260' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2271' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2263' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2272' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2261' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2265' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('LOI_657' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2256' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AORB_956' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2266' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2257' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AORB_953' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2269' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2259' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2270' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2128' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2127' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AORB_955' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2264' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIU_258' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AORB_951' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2255' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AORB_952' in equiv_muts_per_class[mutated_class][mutated_method])
        self.assertTrue('AOIS_2262' in equiv_muts_per_class[mutated_class][mutated_method])
     
        
    def testSimulatorAdd_and_RemoveNodeNed(self):
        mutated_class = 'pamvotis.core.Simulator'
        
        muts_per_class, equiv_muts_per_class = Analyses.ned(self.mujava_result_dir, self.include_methods)
        
        self.assertTrue(len(equiv_muts_per_class[mutated_class][self.include_methods[0]]) == 0)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][self.include_methods[1]]) == 0)
