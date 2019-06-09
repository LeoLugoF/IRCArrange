import sys
import os
import re

#########################################################################
#                              IRCArrange                               #
# Made by:  Leonardo Israel Lugo Fuentes (LeoLugoF)                     #                 
# Date:     08/June/2019                                                #
#                                                                       #
# This program reads gaussian output files with .log or .out termation. #
# It orders the irc from reactant to products; or inverse if needed.    #
# The new IRC is written in a .xyz with all structures with the same    #
# name of the old file + "NewIrc.xyz".                                  #
# The .xyz is design for Chemcraft.                                     #
#                                                                       #
# Command line:[python3] [*.py] [*.log/*.out] [NONE/-r]                 #
# Example 1:    python OrderIRC.py YourFile.log                         #
# Example 2:    python OrderIRC.py YourFile.out -r                      #
#                                                                       #
# The first example will order the irc the default way.                 #
# The second example will order the irc the inverse way.                #
#########################################################################

#Global variables
DictLines = {}
Reversed = False
FilePath = ""

def ReadFile(FilePath):
    """Reads the irc output file"""
    file = open(FilePath,"r+")
    lines = file.readlines()
    file.close()
    Continue = False
    First = True
    LineNumber = -1
    Doubled = False
    NumberOfNewPath = 0
    for line in lines:
        if "SCF" in line and "Done" in line:
            List = line.split(" ")
            for number in List:
                try:
                    ESCF = float(number)
                    break
                except:
                    pass            
            DictLines[LineNumber] = "\n"+str(ESCF)+"\n" + DictLines[LineNumber]
        if "Number" in line and "X" in line and "Y" in line and "Z" in line and "Type" in line or Continue is True:
            if "------" in line:
                if Doubled is False:
                    Continue = True
                    Doubled = True
                else:
                    Doubled = False
                    Continue = False
                continue
            if "Number" in line:
                Continue = True
                LineNumber += 1
                continue
            List = line.split(" ")
            NewList = [s.strip() for s in List if s is not " " and s is not '']
            NewList.pop(0)
            NewList.pop(1)
            string = "\t".join(NewList) +"\n"
            try:
                DictLines[LineNumber] += string
            except:
                DictLines[LineNumber] = string
        if "Begining" in line and "calculation" in line and "path" in line and "of" in line:
            NumberOfNewPath = LineNumber
    #This line corrects a bug in the program
    del DictLines[len(DictLines)-1]
    
    OrderIRC(NumberOfNewPath+1)

    

def OrderIRC(PathNum):
    """Orders the reaction path"""
    NewIndex = -1
    for OldIndex in range(PathNum,len(DictLines)):
        DictLines[NewIndex] = DictLines[OldIndex]
        NewIndex -= 1
        del DictLines[OldIndex]

def WriteNewIRC(FilePath):
    """Writes correctly the irc in a .xyz file"""
    fwrite = open(FilePath.split(".")[0] + "NewIRC.xyz","w")
    #If a irc reversed is asked, reverse will equal True
    for key in sorted(DictLines,reverse=Reversed):
        fwrite.writelines(DictLines[key])
    fwrite.close()

for arg in sys.argv:
    """Checks all the arguments giving in the command line."""
    if ".py" in arg:
        pass
    if ".out" in arg or ".log" in arg or ".OUT" in arg or ".LOG" in arg: 
        FilePath = os.getcwd() + "\\" + arg
    if "-r" in arg:
        Reversed = True

if(FilePath == ""):
    """If no extra arguments are giving in the command line, the file path is asked."""
    FilePath = input("Please insert the file path: ")
    
ReadFile(FilePath)
WriteNewIRC(FilePath)
