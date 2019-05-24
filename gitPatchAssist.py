#!/usr/bin/env python3
'''
 * Created by Lucas Costa Cabral.
 * Email: lucascostacabra@gmail.com
 * Date: 3/5/19
'''

import subprocess
import pyperclip
import sys

def makeCommitLogFile(fp):
        with open(fp,"w") as aux:
                process = subprocess.Popen("git log", stdout=aux, shell=True)
                process.wait()
                aux.flush()

def getCommitShaList(fp,lastCommit):
        commit_list = list()
        with open(fp,"r") as aux:
                for line in aux:
                        if("commit" in line):
                            if(lastCommit in line):
                                break
                            else:
                                commit_list.append(line.strip("commit").strip('\n').strip(" "))
        return commit_list


def write_list_to_file(ls,fileName):
        with open(fileName,"w") as fil:
                for row in ls:
                        fil.write(str(row) + '\n')

def run(cmd):
        process = subprocess.Popen(cmd,shell=True)
        process.wait()

def removeFile(logPath):
        run("rm " + logPath)

def getHeadCommit():
    return subprocess.getoutput("git rev-parse CESAR/master")

def getBaseSha(commit):
        return commit[:6]

def getWorkBranch():
    return subprocess.getoutput("git symbolic-ref --short HEAD")

def getRemoteURL():
        return subprocess.getoutput("git config --get remote.origin.url")

def getCommitMessage(commit):
        with open("aux.txt","r") as aux:
                for line in aux:
                        if(commit in line):
                                line = aux.readline()
                                line = aux.readline()
                                line = aux.readline()
                                line = aux.readline()
                                return line

def makeTemplate(commit,message):
        return ('`' + getBaseSha(commit) + '`' + message).strip('\n')

def buildCommitMessagePatch(commitList):
        clipboard_message = str(len(commitList)) + " patches @" + '`'+  getRemoteURL() + "/tree/"+ getWorkBranch() + '`' +  '\n' 
        clipboard_message += ">>>" + '\n'
        for commit in commitList:
                formated_commit = makeTemplate(commit,getCommitMessage(commit))
                clipboard_message += formated_commit + '\n'
        
        print(clipboard_message)
        pyperclip.copy(clipboard_message)

def main():
    fileName ="aux.txt"
    makeCommitLogFile(fileName)
    l = getHeadCommit()
    commitList = getCommitShaList(fileName,l)
    buildCommitMessagePatch(commitList)
    removeFile(fileName)

if __name__ == '__main__':
    main()
