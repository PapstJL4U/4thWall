"""This is the main entrance to the 4thwalling python project. This project reads
a bunch of hqt(formated text files) files, which contain all dialog of the 
Harley Quinn solo series. Afterward it makes a bunch of statistical analysis to 
guess how much 4th wall breaking happens"""

import os, re

dir_path = os.path.dirname(os.path.abspath(__file__))
issue_path = os.path.join(dir_path, "issues")

"""
examples
 '#writers', '#publisher' 
 It is a hashtag followed  by a 1+ repetition of [a-zA-Z0-9_] and a ' '(space) at the end
"""
reHeader = re.compile('^\#\w+')
reRoles = '^\w+\:'
header_info = {'title':'',
                'publisher':'',
                'people':'',
                'shortcuts':''
                }

def strippy( stripme):
    """use this to clear strings of unnecessary whitespaces and newlines"""
    return stripme.lstrip(' ').rstrip(' \n')

def stripDots( stripme):
    """strips a line of '.'"""
    return stripme.lstrip('.').rstrip('.')

def stripSpecial( stripme):
    """strips a string of special characters like '!, '?', etc"""
    return stripme.lstrip('-?!,').rstrip('?!-,')

def readHeader( file):
    """reads the header of the .hqt file. Header information consists of '#<information>' tag followed by the information
    currently only a small amount of generic information is supported. All non supported information is ignored
    the last header tag should always be '#begin' to indicate the end"""
    for hentry in file.readlines():
        #print(hentry)
        match = re.match(reHeader, hentry)
        if match == None:
            print("in continue clause")
            continue

        if match.group(0) == "#begin":
            print("in break clause")
            return True

        if match.group(0) == "#title":
            #print("in title clause")
            header_info['title'] = strippy(hentry[len(match.group(0)):])

        if match.group(0) == "#publisher":
            header_info['publisher'] = strippy(hentry[len(match.group(0)):])

        if match.group(0) == "#peoples":
            dicPersons = {}
            for person in hentry[len(match.group(0)):].split(';'):
                strippy(person)
                dicPersons[strippy(person.split(':')[0])] = list(map(strippy, person.split(':')[1].split(',')))
            header_info['people'] = dicPersons

        if match.group(0) == "#shortcuts":
            dicShortcuts = {}
            for shortcut in hentry[len(match.group(0)):].split(';'):
                strippy(shortcut)
                dicShortcuts[strippy(shortcut.split(':')[0])] = strippy(shortcut.split(':')[1])
            header_info['shortcuts'] = dicShortcuts

def easyGlobalDialog( file):
    """returns a global dictionary with all words and the amount of usages 'word':'integer'"""
    globalDic = {}
    for line in file.readlines():
        if line.startswith('#') or line == "\n":
            continue
        text = strippy(line.split(':')[1])
        for word in text.split(' '):
            word = stripSpecial(stripDots(word)).lower()
            if word not in globalDic.keys():
                globalDic[word] = 1
            else:
                globalDic[word] += 1
    globalDic.pop("")
    return globalDic


if __name__ == "__main__":
    print(dir_path)
    print(issue_path)
    try:
        file = open(os.path.join(issue_path, "Harley Quinn 1.hqt"), mode='r')
        readHeader(file)
        print(header_info)
        file.seek(0)
        globalDictionary = easyGlobalDialog(file)
        print(globalDictionary)
    except:
        raise
    finally:
        file.close()
