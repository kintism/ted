'''
Created on 13 Jun 2015

@author: marinos
'''

import os
import shutil
import subprocess

rt_jar_location = ''
soot_executable = ''

def optimise(mujava_result_dir, experiment_dir, included_methods, handled_mutants=0):
    """ 
    Optimise the classes in *mujava_result_dir* by calling ``soot``.
    
    The optimised classes will be stored in *experiment_dir*.
    """
    if not os.path.exists(os.path.join(experiment_dir, 'bin')) or not os.path.exists(os.path.join(experiment_dir, 'optimisations')):
        print 'Cannot optimise: '
        print 'Paths: ', os.path.join(experiment_dir, 'bin'), ' and/or ',
        print os.path.join(experiment_dir, 'optimisations'),
        print 'do NOT exist. Returning...'
        return
                                                                                    
       
    experiment_classes = os.path.join(experiment_dir, 'bin')
    
    for mutated_class in os.listdir(mujava_result_dir):
        
        package_and_class = mutated_class.rsplit('.', 1)
        if len(package_and_class) == 1: package_and_class.insert(0, '')
        
        mutated_class_name = package_and_class[1]
        package_structure = package_and_class[0].replace('.', '/')
        
        optimisations_for_class = os.path.join(experiment_dir, 'optimisations', mutated_class_name)
        print '  mkdir', optimisations_for_class
        _createDir_dwim(optimisations_for_class)
        
        print 'Working for the traditional mutants'
        traditional_muts = os.path.join(mujava_result_dir,mutated_class,'traditional_mutants')
        
        for mutated_method in os.listdir(traditional_muts):
            
            if included_methods and not mutated_method in included_methods:
                print 'Mutated method %s not in the included ones' % mutated_method
                continue
            
            mutated_methods_path = os.path.join(traditional_muts,mutated_method)
            
            if os.path.isdir(mutated_methods_path):
                
                optimisations_for_method = os.path.join(optimisations_for_class, mutated_method)
                print '  mkdir', optimisations_for_method
                _createDir_dwim(optimisations_for_method)
                
                number_of_muts = 0;
                
                for root, dirs, files in os.walk(mutated_methods_path):
                    if not dirs and files:
                        mutant_name = os.path.basename(root)
                        print 'mutant: ', mutant_name
                        print '  Copying ', os.path.join(root, mutated_class_name + '.class')
                        print '  to ', os.path.join(experiment_classes, package_structure) 
                        shutil.copy(os.path.join(root, mutated_class_name + '.class'), os.path.join(experiment_classes, package_structure))                        
                        _executeSoot(soot_executable, experiment_classes, optimisations_for_method + '/optimised-' + mutant_name + '/', mutated_class, False)

                        number_of_muts += 1
                        
                        if handled_mutants and number_of_muts == handled_mutants:
                            break
                        
                    print '--------------------------------------------------'
                
                print
                print 'Handled %d mutants' % number_of_muts
        
        print 'Working for the original file'
        print '  Copying ', os.path.join(mujava_result_dir,mutated_class,'original', mutated_class_name + '.class')
        print '  to ', os.path.join(experiment_classes, package_structure) 
        shutil.copy(os.path.join(mujava_result_dir,mutated_class,'original', mutated_class_name + '.class'), os.path.join(experiment_classes, package_structure))
        _executeSoot(soot_executable, experiment_classes, optimisations_for_class + '/optimised-original/', mutated_class, False)
        

def _executeSoot(soot_jar, experiment_dir, dest_dir, target_class, jimple = True):
    command = 'java -jar %s -cp %s -d "%s" %s-O %s' % (soot_jar, experiment_dir + ':' + rt_jar_location, dest_dir, '-f jimple ' if jimple else '', target_class)
    print 'executing: ', command 
    subprocess.call(command, shell=True)
    
def _mydiffFiles(file1, file2):
    command = 'diff "%s" "%s"' % (file1, file2)
    return subprocess.call(command, shell=True)

def _createDir_dwim(d):
    if not os.path.exists(d):
        os.mkdir(d)



def ted(experiment_dir, included_methods):
    """
    Detect equivalent mutants via soot.
    
    This step must be performed after the ``optimisation`` phase, i.e. after the 
    :func:`optimise`. The *experiment_dir* is the same as the one used in the 
    previous phase.
    
    Returns two dictionaries that are structured in the following way:
    
    ``mutatedClasses -> mutated methods -> mutants``
    """
    equiv_muts_per_class = {}
    muts_per_class = {}
    
    optimised_classes_dir = os.path.join(experiment_dir, 'optimisations')

    for optimised_class in os.listdir(optimised_classes_dir):
        
        equiv_muts_per_method = {}
        muts_num_per_method = {}
        
        equiv_muts_per_class[optimised_class] = equiv_muts_per_method
        muts_per_class[optimised_class] = muts_num_per_method
    
        print 'Working for optimised methods of ', optimised_class
        optimised_methods_dir = os.path.join(optimised_classes_dir, optimised_class)
        
        original_program = os.path.join(optimised_methods_dir, 'optimised-original')
        print 'Original program at: ', original_program
        
        for optimised_method in os.listdir(optimised_methods_dir):
            print 'Working for optimised_method: ', optimised_method
            
            if 'optimised-original' in optimised_method:
                print 'skipping'
                continue
            
            if included_methods and not optimised_method in included_methods:
                print 'Optimised method %s not in the included ones' % optimised_method
                continue
            
            equiv_muts_per_method[optimised_method] = []
            muts_num_per_method[optimised_method] = []
            
            for root, dirs, files in os.walk(os.path.join(optimised_methods_dir, optimised_method)):
                
                print 'root: ', root
                print 'dirs: ', dirs
                # Note that files will always contain one class file (the optimised class). Thus, there is no problem using the files[0] expression.
                print 'files: ', files
                
                if files:
                    mutant_and_package = root.rsplit('optimised-', 1)[1].split('/', 1)
                    if len(mutant_and_package) == 1: mutant_and_package.append('')
                    print mutant_and_package
                    
                    print 'Working for mutant: ', mutant_and_package[0]
                    muts_num_per_method[optimised_method].append(mutant_and_package[0])
                    
                    print '  Comparing mut_file: ', os.path.join(root, files[0])
                    print '  with orig:', os.path.join(original_program, mutant_and_package[1],files[0])
                    if _mydiffFiles(os.path.join(root, files[0]), os.path.join(original_program, mutant_and_package[1],files[0])) == 0:
                        print '    Found equivalent mutant'
                        equiv_muts_per_method[optimised_method].append(mutant_and_package[0])
                    
                
                print '--------------------------------------------------'
    
    print         
    print '******** Summary ********'
    
    for mutated_class in muts_per_class:
        print 'Mutants of class ', mutated_class
        
        for mutated_method in muts_per_class[mutated_class]:
            print '  Mutants of method ', mutated_method
            print '  Number of muts ', len(muts_per_class[mutated_class][mutated_method])
            
            print '  Mutants '
            for mut in muts_per_class[mutated_class][mutated_method]:
                print '    ', mut
            
            mutsPerOperator(muts_per_class[mutated_class][mutated_method])
            
            print '  Equivalent mutants detected ', len(equiv_muts_per_class[mutated_class][mutated_method])
            for equiv_mut in equiv_muts_per_class[mutated_class][mutated_method]:
                print '    ', equiv_mut

            mutsPerOperator(equiv_muts_per_class[mutated_class][mutated_method])
            
    return muts_per_class, equiv_muts_per_class

def mutsPerOperatorInDict(muts_per_class):
    """
    This method takes as input one of the directories returned by the 
    :func:`ted`
    """
    
    mut_per_operator = {}
    total_muts = 0
    
    for mutated_class in muts_per_class:
        
        for mutated_method in muts_per_class[mutated_class]:
            
            total_muts += len(muts_per_class[mutated_class][mutated_method])
            for mut in muts_per_class[mutated_class][mutated_method]:
                mut_op = mut.split('_',1)[0]
                mut_per_operator[mut_op] = mut_per_operator.get(mut_op, 0) + 1
            
            
    _printMutsPerOperator(mut_per_operator)
    
    return mut_per_operator
            

def mutsPerOperator(muts):
    mut_per_operator = {}
    
    for mut in muts:
        mut_op = mut.split('_',1)[0]
        mut_per_operator[mut_op] = mut_per_operator.get(mut_op, 0) + 1
    
    _printMutsPerOperator(mut_per_operator)
    
    return mut_per_operator



def _printMutsPerOperator(mut_per_operator):
    
    for key in sorted(mut_per_operator):
        print key + ' |',
    
    print
    total = 0
    
    for key in sorted(mut_per_operator):
        total += mut_per_operator[key]
        print ('%' + str(len(key)) + 's |') % str(mut_per_operator[key]),
    
    print
    print '  Total muts handled: ', total
    print



def ned(mujava_result_dir, included_methods):
    """ 
    Detect equivalent mutants with the default compilation scheme of java.
    """
    total_equivs_found = 0
    equiv_muts_per_class = {}
    muts_per_class = {}
    
    for mutated_class in os.listdir(mujava_result_dir):
        
        equiv_muts_per_method = {}
        muts_num_per_method = {}
        
        equiv_muts_per_class[mutated_class] = equiv_muts_per_method
        muts_per_class[mutated_class] = muts_num_per_method
        
        package_and_class = mutated_class.rsplit('.', 1)
        if len(package_and_class) == 1: package_and_class.insert(0, '')
        
        mutated_class_name = package_and_class[1]
        
        print 'Original file found at'
        original_program = os.path.join(mujava_result_dir,mutated_class,'original', mutated_class_name + '.class')
        print original_program
        
        print 'Working for the traditional mutants'
        traditional_muts = os.path.join(mujava_result_dir,mutated_class,'traditional_mutants')
        
        for mutated_method in os.listdir(traditional_muts):
            
            if included_methods and not mutated_method in included_methods:
                print 'Optimised method %s not in the included ones' % mutated_method
                continue
            
            
            mutated_methods_path = os.path.join(traditional_muts,mutated_method)
            
            if os.path.isdir(mutated_methods_path):
                
                equiv_muts_per_method[mutated_method] = []
                muts_num_per_method[mutated_method] = []
                
                for root, dirs, files in os.walk(mutated_methods_path):
                    if not dirs and files:
                        mutant_name = os.path.basename(root)
                        print 'mutant: ', mutant_name
                        print '  Found at ', os.path.join(root, mutated_class_name + '.class')
                        muts_num_per_method[mutated_method].append(mutant_name)
                        
                        if _mydiffFiles(original_program, os.path.join(root, mutated_class_name + '.class')) == 0:
                            total_equivs_found += 1
                            print '    Found equivalent mutant'
                            equiv_muts_per_method[mutated_method].append(mutant_name)
                    
                        
                    print '--------------------------------------------------'
                
    print         
    print '******** Summary ********'
    
    for mutated_class in equiv_muts_per_class:
        print 'Mutants of class ', mutated_class
        
        for mutated_method in equiv_muts_per_class[mutated_class]:
            print '  Mutants of method ', mutated_method
            
            print '  Equivalent mutants detected ', len(equiv_muts_per_class[mutated_class][mutated_method])
            for equiv_mut in equiv_muts_per_class[mutated_class][mutated_method]:
                print '    ', equiv_mut

            mutsPerOperator(equiv_muts_per_class[mutated_class][mutated_method])

    return muts_per_class, equiv_muts_per_class


def nedFindDups(mujava_result_dir, included_methods, equiv_muts_per_class=None):
    """ 
    Detect duplicated mutants with NeD, i.e. utilising =javac=.
    """
    dup_muts_per_class = {}
    muts_per_class = {}
    
    for mutated_class in os.listdir(mujava_result_dir):
        
        dup_muts_per_mutant_per_method = {}
        muts_num_per_method = {}
        
        dup_muts_per_class[mutated_class] = dup_muts_per_mutant_per_method
        muts_per_class[mutated_class] = muts_num_per_method
        
        package_and_class = mutated_class.rsplit('.', 1)
        if len(package_and_class) == 1: package_and_class.insert(0, '')
        
        mutated_class_name = package_and_class[1]
        
        traditional_muts = os.path.join(mujava_result_dir,mutated_class,'traditional_mutants')
        
        for mutated_method in os.listdir(traditional_muts):
            
            print 'Working for method', mutated_method
            
            if included_methods and not mutated_method in included_methods:
                print 'Method %s not in the included ones' % mutated_method
                continue
            
            
            mutated_methods_path = os.path.join(traditional_muts,mutated_method)
            
            if os.path.isdir(mutated_methods_path):
                
                dup_muts_per_mutant_per_method[mutated_method] = {}
                muts_num_per_method[mutated_method] = []
                
                for root1, dirs1, files1 in os.walk(mutated_methods_path):
                    
                    print "dirs1:", dirs1
                    
                    if not dirs1 and files1:
                        mutant_name = os.path.basename(root1)
                        
                        print '--------------------------------------------------'
                        print 'Working for mutant1: ', mutant_name
                        print '  Found at ', os.path.join(root1, mutated_class_name + '.class')
                        muts_num_per_method[mutated_method].append(mutant_name)
                        
                        if equiv_muts_per_class and mutant_name in equiv_muts_per_class[mutated_class][mutated_method]:
                            print 'Mutant is detected as equivalent. Continuing...'
                            continue  
                    
                        dup_muts_per_mutant_per_method[mutated_method][mutant_name] = []
                        
                        for root2, dirs2, files2 in os.walk(mutated_methods_path):
                            if not dirs2 and files2:
                                mutant_name2 = os.path.basename(root2)
                                print '  Working for mutant2: ', mutant_name2
                            
                                if mutant_name2 in dup_muts_per_mutant_per_method[mutated_method]:
                                    print 'Already handled mutants... Continuing.'
                                    
                                    if mutant_name in dup_muts_per_mutant_per_method[mutated_method][mutant_name2]:
                                        print mutant_name2, 'has', mutant_name, 'as duplicate... Deleting ', mutant_name, '\'s list.'
                                        del dup_muts_per_mutant_per_method[mutated_method][mutant_name]
                                        break
                                    
                                    continue
                                
                                print '***********'
                                print 'Comparing mut_file1: ', os.path.join(root1, mutated_class_name + '.class')
                                print '         with file2: ', os.path.join(root2, mutated_class_name + '.class')
                                print '***********'
                                if _mydiffFiles(os.path.join(root1, mutated_class_name + '.class'), os.path.join(root2, mutated_class_name + '.class')) == 0:
                                    print '    Found duplicated mutant'
                                    dup_muts_per_mutant_per_method[mutated_method][mutant_name].append(mutant_name2)
                    
                    
                    
                    
            print '--------------------------------------------------1'
                
    print         
    print '******** Summary ********'
    
    for mutated_class in muts_per_class:
        print 'Mutants of class ', mutated_class
         
        for mutated_method in muts_per_class[mutated_class]:
            print '  Mutants of method ', mutated_method
            print '  Number of muts ', len(muts_per_class[mutated_class][mutated_method])
            
            muts_per_op = mutsPerOperator(muts_per_class[mutated_class][mutated_method])
             
            print '  Mutants: [duplicated]'
            duplicated_for_per_op_stats = []
            duplicated = 0
            for mut in dup_muts_per_class[mutated_class][mutated_method]:
                if dup_muts_per_class[mutated_class][mutated_method][mut]:
                    print '    ', mut, ': ', dup_muts_per_class[mutated_class][mutated_method][mut]
                    duplicated_for_per_op_stats.append(mut)
                    duplicated_for_per_op_stats.extend(dup_muts_per_class[mutated_class][mutated_method][mut])
                    duplicated += len(dup_muts_per_class[mutated_class][mutated_method][mut])
            
            
            dupes_per_op = mutsPerOperator(duplicated_for_per_op_stats)
            
            print 'Stats'
            printEquivsORDupsPercentagePerOperator(muts_per_op, dupes_per_op)
            
            if len(muts_per_class[mutated_class][mutated_method]) != 0:
                print 'Total number of Duplicated muts: %d (%.2f)' % (duplicated, (duplicated / float(len(muts_per_class[mutated_class][mutated_method]))))
            else:
                print 'Total number of Duplicated muts: %d ' % duplicated

    return muts_per_class, dup_muts_per_class



def findDups(experiment_dir, included_methods, equiv_muts_per_class=None):
    """
    Detect duplicated mutants with Trivial Equivalent Detection technique.
    
    This step must be performed after: a) the ``optimisation`` phase, i.e. after the 
    :func:`optimise`. The *experiment_dir* is the same as the one used in the 
    previous phase, and b) the detection phase has been complete (:func: `ted`), because 
    the equiv_muts_per_class argument is the dictionary return by ted. (This is in order
    not to consider the equivalent mutants in the duplicate detection phase.)
    
    Returns a dictionary that is structured in the following way:
    
    ``mutatedClasses -> mutated methods -> mutants -> duplicated_muts``
    """
    dup_muts_per_class = {}
    muts_per_class = {}
    
    optimised_classes_dir = os.path.join(experiment_dir, 'optimisations')

    for optimised_class in os.listdir(optimised_classes_dir):
        
        dup_muts_per_mutant_per_method = {}
        muts_num_per_method = {}
        
        dup_muts_per_class[optimised_class] = dup_muts_per_mutant_per_method
        muts_per_class[optimised_class] = muts_num_per_method
    
        print 'Working for optimised methods of ', optimised_class
        optimised_methods_dir = os.path.join(optimised_classes_dir, optimised_class)
        
        for optimised_method in os.listdir(optimised_methods_dir):
            print 'Working for optimised_method: ', optimised_method
            
            if 'optimised-original' in optimised_method:
                print 'skipping'
                continue
            
            if included_methods and not optimised_method in included_methods:
                print 'Optimised method %s not in the included ones' % optimised_method
                continue
            
            dup_muts_per_mutant_per_method[optimised_method] = {}
            muts_num_per_method[optimised_method] = []
            
            for root1, dirs1, files1 in os.walk(os.path.join(optimised_methods_dir, optimised_method)):
                
                print 'root1: ', root1
                print 'dirs1: ', dirs1
                # Note that files will always contain one class file (the optimised class). Thus, there is no problem using the files[0] expression.
                print 'files1: ', files1
                
                if files1:
                    mutant_and_package1 = root1.rsplit('optimised-', 1)[1].split('/', 1)
                    if len(mutant_and_package1) == 1: mutant_and_package1.append('')
                    print mutant_and_package1
                    
                    print '--------------------------------------------------'
                    print 'Working for mutant1: ', mutant_and_package1[0]
                    
                    muts_num_per_method[optimised_method].append(mutant_and_package1[0])
                    
                    if equiv_muts_per_class and mutant_and_package1[0] in equiv_muts_per_class[optimised_class][optimised_method]:
                        print 'Mutant is detected as equivalent. Continuing...'
                        continue                  
                    
                    dup_muts_per_mutant_per_method[optimised_method][mutant_and_package1[0]] = []
        
                    
                    # copied from above                     
                    for root2, dirs2, files2 in os.walk(os.path.join(optimised_methods_dir, optimised_method)):
                    
                        if files2:
                            mutant_and_package2 = root2.rsplit('optimised-', 1)[1].split('/', 1)
                            if len(mutant_and_package2) == 1: mutant_and_package2.append('')
                            print '  ', mutant_and_package2
                            
                            print '  Working for mutant2: ', mutant_and_package2[0]
                            
                            if mutant_and_package2[0] in dup_muts_per_mutant_per_method[optimised_method]:
                                print 'Already handled mutants... Continuing.'
                                
                                if mutant_and_package1[0] in dup_muts_per_mutant_per_method[optimised_method][mutant_and_package2[0]]:
                                    print mutant_and_package2[0], 'has', mutant_and_package1[0], 'as duplicate... Deleting ', mutant_and_package1[0], '\'s list.'
                                    del dup_muts_per_mutant_per_method[optimised_method][mutant_and_package1[0]]
                                    break
                                
                                continue
                            
                            
                            print '***********'
                            print 'Comparing mut_file1: ', os.path.join(root1, files1[0])
                            print '         with file2: ', os.path.join(root2, files2[0])
                            print '***********'
                            if _mydiffFiles(os.path.join(root1, files1[0]), os.path.join(root2, files2[0])) == 0:
                                print '    Found duplicated mutant'
                                dup_muts_per_mutant_per_method[optimised_method][mutant_and_package1[0]].append(mutant_and_package2[0])
                        
#                         print '--------------------------------------------------2'
                    
                
                print '--------------------------------------------------1'
    
    print         
    print '******** Summary ********'
     
    for mutated_class in muts_per_class:
        print 'Mutants of class ', mutated_class
         
        for mutated_method in muts_per_class[mutated_class]:
            print '  Mutants of method ', mutated_method
            print '  Number of muts ', len(muts_per_class[mutated_class][mutated_method])
            
            muts_per_op = mutsPerOperator(muts_per_class[mutated_class][mutated_method])
             
            print '  Mutants: [duplicated]'
            duplicated_for_per_op_stats = []
            duplicated = 0
            for mut in dup_muts_per_class[mutated_class][mutated_method]:
                if dup_muts_per_class[mutated_class][mutated_method][mut]:
                    print '    ', mut, ': ', dup_muts_per_class[mutated_class][mutated_method][mut]
                    duplicated_for_per_op_stats.append(mut)
                    duplicated_for_per_op_stats.extend(dup_muts_per_class[mutated_class][mutated_method][mut])
                    duplicated += len(dup_muts_per_class[mutated_class][mutated_method][mut])
            
            
            dupes_per_op = mutsPerOperator(duplicated_for_per_op_stats)
            
            print 'Stats'
            printEquivsORDupsPercentagePerOperator(muts_per_op, dupes_per_op)
            
            if len(muts_per_class[mutated_class][mutated_method]) != 0:
                print 'Total number of Duplicated muts: %d (%.2f)' % (duplicated, (duplicated / float(len(muts_per_class[mutated_class][mutated_method]))))
            else:
                print 'Total number of Duplicated muts: %d ' % duplicated

    return muts_per_class, dup_muts_per_class


def printEquivsORDupsPercentagePerOperator(muts_per_op, dupes_per_op, genProportions = True):
    """
    Pretty-prints the mutants in DUPES_PER_OP per operator, along with their proportion with respect to the
    corresponding ones in MUTS_PER_OP. Note that it can also be used for equivalent mutants (not only
    duplicated ones, as the second argument suggests)
    
    Note that in order to produce the aforementioned proportions the GENPROPORTIONS parameter must be true.
    """
    for key in sorted(dupes_per_op):
        value = ('%d (%.2f)') % (dupes_per_op[key], (dupes_per_op[key] / float(muts_per_op.get(key,1))))
        
        if not genProportions: 
            value = str(dupes_per_op[key])
        
        print ('%' + str(len(key) + len(value)) + 's |') % key,
    print
    total = 0
    
    for key in sorted(dupes_per_op):
        total += dupes_per_op[key]
        value = ('%d (%.2f)') % (dupes_per_op[key], (dupes_per_op[key] / float(muts_per_op.get(key,1))))
        
        if not genProportions: 
            value = str(dupes_per_op[key])
        
        print ('%' + str(len(key) + len(value)) + 's |') % value,
    
    print
    print '  Total muts handled: ', total
    print


def dupesPerOperatorInDict(muts_per_class, dupes_per_class):
    """
    This method takes as input the two directories returned by the 
    :func: `findDups`.
    """
    
    print
    print ' ** ALL MUTS ** '
    muts_per_operator = mutsPerOperatorInDict(muts_per_class)
    dupes_per_operator = {}
    total_dups = 0
    total_muts = 0
    
    for mutated_class in dupes_per_class:
        
        for mutated_method in dupes_per_class[mutated_class]:
            total_muts += len(muts_per_class[mutated_class][mutated_method])
            
            for mut in dupes_per_class[mutated_class][mutated_method]:
                if dupes_per_class[mutated_class][mutated_method][mut]:
                    mut_op = mut.split('_',1)[0]
                    dupes_per_operator[mut_op] = dupes_per_operator.get(mut_op, 0) + 1
                    total_dups += len(dupes_per_class[mutated_class][mutated_method][mut])
                    
                    for dup in dupes_per_class[mutated_class][mutated_method][mut]:
                        mut_op = dup.split('_',1)[0]
                        dupes_per_operator[mut_op] = dupes_per_operator.get(mut_op, 0) + 1
    
    
    print ' ** DUP MUTS ** '
    printEquivsORDupsPercentagePerOperator(muts_per_operator, dupes_per_operator)
    print
    print 'Total number of Duplicated muts: %d (%.2f)' % (total_dups, (total_dups / float(total_muts)))
#     print 'Total number of Duplicated muts: %d ' % total_dups
    print 'Total muts: ', total_muts
















