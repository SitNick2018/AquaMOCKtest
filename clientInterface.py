#!/usr/bin/python
"""
This module implements client interface for server tests
"""

import os
import sys
import requests
import time
import random
import json
import threading


MAXTODOENTRIES = 5
MAX_ENTRIES_TO_CHANGE = 4
MAX_ENTRIES_TO_SHOW = 10
ENTRIES_TO_DELETE = 4
headers = {'Content-Type': 'application/json'}

class clientInterface(object):
    """"
    Provides to the user: interface for access the Server via REST and additional necessary functions

    """
    def __init__(self):
        pass

    def RestGet(self, url='http://localhost:5000/tasks', taskid=None,  entries=MAX_ENTRIES_TO_SHOW):
        if taskid:
            url = 'http://localhost:5000/tasks' + '/' + taskid
        try:
            response = requests.get(url, timeout=5)
            resc = response.content
            print"LIST OF TASKS_TO_DO, SHOWING ONLY FIRST {0} or less  {1}".\
                format('ALL' if entries is None else entries,
                       json.loads(resc)[:entries] if not taskid else json.loads(resc))
            response.raise_for_status()
            return resc
        except requests.exceptions.HTTPError as error:
            print(error)
            raise error

    def RestPost(self, url='http://localhost:5000/tasks'):
        try:
            response = requests.post(url, data=setup().JsonDataFiller(), headers=headers, timeout=5)
            print"LIST OF TASKS_TO_DO {0}".format(response.content)
            response.raise_for_status()
            return json.loads(response.content)
        except requests.exceptions.HTTPError as error:
            print(error)
            raise error

    def MultiplePost(self, url='http://localhost:5000/tasks', max_threads=MAXTODOENTRIES):
        try:
            for _ in range(max_threads):
                threading.Thread(target=clientInterface().RestPost(url=url))
        except Exception as e:
            print("Failure", e)
            raise e

    def Modify(self, url='http://localhost:5000/tasks', maxEnToCh=MAX_ENTRIES_TO_CHANGE, id=None):
        if maxEnToCh == -1:  # modify all
            maxEnToCh = len(json.loads(clientInterface().RestGet(url=url)))
        maxEnToCh = maxEnToCh if not id else 1
        for i in range(maxEnToCh):
            taskid = id if id else setup().GetTaskId(i)
            previousContent = json.loads(clientInterface().RestGet(url=url, taskid=taskid))
            contentToCheck = json.loads(setup().JsonDataFiller())
            requests.put(url=url + '/' + taskid, data=json.dumps(contentToCheck), headers=headers)
            newContent = json.loads(clientInterface().RestGet(url=url, taskid=taskid))
            try:
                print"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                print "This check below compares content after modify {0} with content before{1} ," \
                      "expected to be different".format(newContent, previousContent)
                assert newContent != previousContent
            except AssertionError as e:
                print"Assertion error raised, testing fails , expected different contents "
                sys.exit(e)
            else:
                print"\n Check1 succeeded"
            try:
                print"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                print "Next check below compares content after modify {0} with inserted updated new content {1} ," \
                      "expected to be the same".format(newContent, contentToCheck)
                assert newContent == contentToCheck
            except AssertionError as ee:
                print"Assertion error raised, testing fails , expected same content "
                sys.exit(ee)
            else:
                print"\n Check2 succeeded \n"
            print"\n Entry {0} modified successfully \n".format(taskid)

    def Delete(self, url='http://localhost:5000/tasks', maxEnToCh=ENTRIES_TO_DELETE, id=None):
        delAll = False
        if maxEnToCh == -1:  # delete all
            maxEnToCh = len(json.loads(clientInterface().RestGet(url=url)))
            delAll = True
        maxEnToCh = maxEnToCh if not id else 1
        content = json.loads(clientInterface().RestGet(url='http://localhost:5000/tasks', entries=0))
        for i in range(maxEnToCh):
            taskid = id if id else setup().GetTaskId(i, content=content)
            requests.delete(url=url + '/' + taskid)
            try:
                clientInterface().RestGet(url=url, taskid=taskid, entries=0)
            except requests.exceptions.HTTPError as error:
                print(error)
                print"Task with id {0} successfully deleted \n".format(taskid)
        if delAll:
            p = json.loads(clientInterface().RestGet(url=url))
            try:
                print"Check: if all entries were deleted"
                assert len(p) == 0
            except AssertionError as e:
                print"Assertion error raised, testing fails, expected all entries deleted"
                sys.exit(e)
            print"\n All {0} entries were successfully deleted".format(maxEnToCh)


class setup(object):
    """
    Provides to the user: additional necessary function for testing - "setup init"

    """
    def IsServerUp(self, url='http://localhost:5000/tasks', raisException=True, expectUp=True):
        if expectUp:
            print "Checking now if server is running"
        else:
            print"Checking now if server is turned OFF"
        try:
            response = requests.get(url, timeout=5)
            print'Server is running, got {0}'.format(response)
            response.raise_for_status()
        # Code here will only run if the request is successful
        except requests.exceptions.HTTPError as errh:
            print(errh)
            if raisException:
                raise errh
            else:
                return False
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            if raisException:
                raise errc
            else:
                return False
        except requests.exceptions.Timeout as errt:
            print(errt)
            if raisException:
                raise errt
            else:
                return False
        except requests.exceptions.RequestException as err:
            print(err)
            if raisException:
                raise err
            else:
                return False
        return True

    def StartServer(self, path='/opt/serverMOCK/todolist_mock_server', strtCmdOne='\n export FLASK_APP=server.py',
                    strtCmdTwo='\n flask run &'):
        if self.IsServerUp(raisException=False):
            print "server was running will not re-start"
            return
        cmd = path + strtCmdOne + strtCmdTwo
        print "starting server before test"
        print cmd
        try:
            p = os.system(cmd)
            print p
            assert not p
        except AssertionError as e:
            print"Assertion error raised, please check cmd to server start , error {0}".format(e)
        print"timer 5 sec for start server"
        time.sleep(5)
        print "server expected to start"

    def JsonDataFiller(self):
        b = [True, False]
        return json.dumps({"completed": random.choice(b), "task": "create my new task num {0} on server ".
                          format(random.choice(range(100000)))})

    def GetTaskId(self, i=0, content=None):
        tmpc = content or json.loads(clientInterface().RestGet(url='http://localhost:5000/tasks', entries=0))
        return tmpc[i]['id']

    def GetRandomEntryId(self):
        allentries = json.loads(clientInterface().RestGet(url='http://localhost:5000/tasks', entries=0))
        numOfEntries = len(allentries)
        randNUm = random.choice(range(numOfEntries))
        print allentries[randNUm]['id']
        return allentries[randNUm]['id']


class teardown(object):
    """
    Provides to the user: additional necessary function for testing -"teardown"

    """

    def ShutdownServer(self):
        print"Shutting server down"
        if setup().IsServerUp(raisException=False):
            print"kill server process"
            p = os.popen('lsof -i :5000').read().split()[10]
            print('pid', p)
            os.system('sudo kill -9 ' + p)
            if not setup().IsServerUp(raisException=False,  expectUp=False):
                print '\n SERVER SHUTDOWN SUCCEEDED'
        else:
            print"server is down"









