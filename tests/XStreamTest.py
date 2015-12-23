'''
Created on 27 Jun 2015

@author: marinos
'''
import unittest

import Analyses


class Test(unittest.TestCase):

    mujava_result_dir = '/home/marinos/Workbench/mujava/result'
    experiment_dir = '/home/marinos/Desktop/xstream'
    
    include_methods=['java.lang.String_decodeName(java.lang.String)']
    
    def testDecodeNameTed(self):
         
        muts_per_class, equiv_muts_per_class = Analyses.ted(self.experiment_dir, [self.include_methods[0]])
        mutated_class = 'XmlFriendlyNameCoder'
        mutated_method = self.include_methods[0]
         
        self.assertTrue(len(muts_per_class[mutated_class][mutated_method]) == 156)
        self.assertTrue(len(equiv_muts_per_class[mutated_class][mutated_method]) == 0)
          

         
    def testDecodeNed(self):
        mutated_class = 'xcom.thoughtworks.xstream.io.xml.XmlFriendlyNameCoder'
        
        muts_per_class, equiv_muts_per_class = Analyses.ned(self.mujava_result_dir, self.include_methods)
        
        self.assertTrue(len(equiv_muts_per_class[mutated_class][self.include_methods[0]]) == 0)
