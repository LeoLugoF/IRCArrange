import sys
import os
import re
import platform

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
OSplit = "\\"
if platform.system() == "Linux":
    OSplit = "/"
DictAtomicN = { "1":"H","2":"He","3":"Li","4":"Be","5":"B","6":"C","7":"N","8":"O","9":"F","10":"Ne","11":"Na","12":"Mg","13":"Al","14":"Si","15":"P","16":"S","17":"Cl","18":"Ar","19":"K","20":"Ca","21":"Sc","22":"Ti","23":"V","24":"Cr","25":"Mn","26":"Fe","27":"Co","28":"Ni","29":"Cu","30":"Zn","31":"Ga","32":"Ge","33":"As","34":"Se","35":"Br","36":"Kr","37":"Rb","38":"Sr","49":"In","50":"Sn","51":"Sb","52":"Te","53":"I" }

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
            NAtoms = str(len(DictLines[LineNumber].split("\n"))-1)
            DictLines[LineNumber] = "\n" + NAtoms +  "\n"+str(ESCF)+"\n" + DictLines[LineNumber]
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
            NewList[0] = DictAtomicN[NewList[0]]
            string = "\t ".join(NewList) +"\n"
            try:
                DictLines[LineNumber] += string
            except:
                DictLines[LineNumber] = string
        if "Begi" in line and "calculation" in line and "path" in line and "of" in line:
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
        FilePath = os.getcwd() + OSplit + arg
    if "-r" in arg:
        Reversed = True

if(FilePath == ""):
    """If no extra arguments are giving in the command line, the file path is asked."""
    FilePath = input("Please insert the file path: ")
    
ReadFile(FilePath)
WriteNewIRC(FilePath)
