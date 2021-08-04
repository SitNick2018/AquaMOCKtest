#!/usr/bin/python
"""
server tests
"""
__author__ = 'Tim'

import os
import sys
import flask
import clientInterface
from optparse import OptionParser

def test1():
    """
    test Get function
    :return:
    """
    
    print"\n ******************************** \n"
    print"test1 is started-  Get function test"
    print"\n ******************************** \n"
    clientInterface.clientInterface().RestGet()
    print"\n -------------------------------- \n"
    print"test1 passed"
    print"\n -------------------------------- \n"
    


def test2():
    """
    test POST function
    :return:
    """
    
    print"\n ******************************** \n"
    print"test2 is started-  POST function test"
    print"\n ******************************** \n"
    res = clientInterface.clientInterface().RestPost()
    clientInterface.clientInterface().RestGet(taskid=res["task_id"])
    print"\n -------------------------------- \n"
    print"test2 passed"
    print"\n -------------------------------- \n"
    


def test3():
    """
    test Multiple POST function
    :return:
    """
    
    print"\n ******************************** \n"
    print"test3 is started-  MULTIPLE POST  test"
    print"\n ******************************** \n"
    clientInterface.clientInterface().MultiplePost()
    print"\n -------------------------------- \n"
    print"test3 passed"
    print"\n -------------------------------- \n"
    

def test4():
    """
    test MODIFY function test- several entries
    :return:
    """
    
    print"\n ******************************** \n"
    print"test4 is started-  MODIFY function test- several entries"
    print"\n ******************************** \n"
    clientInterface.clientInterface().MultiplePost()
    clientInterface.clientInterface().Modify()
    print"\n -------------------------------- \n"
    print"test4 passed"
    print"\n -------------------------------- \n"
    

def test5():
    """
    test MODIFY function test - one predefined entry
    :return:
    """
    
    print"\n ******************************** \n"
    print"test5 is started-  MODIFY function test - one predefined entry"
    print"\n ******************************** \n"

    clientInterface.clientInterface().Modify(id=clientInterface.setup().GetRandomEntryId())
    print"\n -------------------------------- \n"
    print"test5 passed"
    print"\n -------------------------------- \n"
    

def test6():
    """
    test MODIFY function test - all entries
    :return:
    """
    
    print"\n ******************************** \n"
    print"test6 is started-  MODIFY function test - all entries"
    print"\n ******************************** \n"
    clientInterface.clientInterface().MultiplePost()
    clientInterface.clientInterface().Modify(maxEnToCh=-1)
    print"\n -------------------------------- \n"
    print"test6 passed"
    print"\n -------------------------------- \n"
    

def test7():
    """
    test DELETE function test - one predefined entry
    :return:
    """
    
    print"\n ******************************** \n"
    print"test7 is started-  DELETE function test - one predefined entry"
    print"\n ******************************** \n"

    clientInterface.clientInterface().Delete(id=clientInterface.setup().GetRandomEntryId())
    print"\n -------------------------------- \n"
    print"test7 passed"
    print"\n -------------------------------- \n"
    

def test8():
    """
    test DELETE function test - delete all entries
    :return:
    """
    
    print"\n ******************************** \n"
    print"test8 is started-  DELETE function test - delete all entries"
    print"\n ******************************** \n"
    clientInterface.clientInterface().MultiplePost()
    clientInterface.clientInterface().Delete(maxEnToCh=-1)
    print"\n -------------------------------- \n"
    print"test8 passed"
    print"\n -------------------------------- \n"


def GetInput():
    """
    This function creates option parser from user input and return options object and list of args

    :returns: tuple: 1st: options object according to user input, 2nd: list of program arguments
    :rtype: tuple
    """
    usage = '%prog <test num to run : test1 = 1 , test2 = 2 etc. > can use several numbers: 1 2 3 .. \n' \
            'to run all tests in test suite at once please leave empty'
    parser = OptionParser(usage=usage)
    args = parser.parse_args()
    return args
    

def main():
    clientInterface.setup().StartServer()  # (path='')
    clientInterface.setup().IsServerUp()
    args = GetInput()
    testsNumsToRun = map(int, args[1])
    testSuite = [test1,
                test2,
                test3,
                test4,
                test5,
                test6,
                test7,
                test8]
    for testNum in testsNumsToRun:
        if testNum > 8:
            print"\n ERROR with wrong test num {0}. Please put integers in range 1 to {1} include \n".\
                format(testNum, len(testSuite))
            sys.exit(1)
    if len(args[1]) < 1:
        testsToRun = testSuite

    else:
        testsToRun= [testSuite[i-1] for i in testsNumsToRun]
    print testsToRun
    try:
        for test in testsToRun:
            test()
        print '\n Tests suite passed with success \n'
    except Exception as e:
        print e
    finally:
        clientInterface.teardown().ShutdownServer()


if __name__ == '__main__':
   main()


