#!/usr/bin/python3
#Written by Raikin, June 2016
#Changed March 2017

import csv
import configparser
import re
import sys

PATH_TO_CHARS = ""
PATH_TO_DYNASTIES = ""
PATH_TO_TITLES = ""

CHARFILE = ""
DYNFILE = ""

TITLEDEF = ""

def applytitle(id, title):
    title_starts = TITLEDEF
    titlepath = PATH_TO_TITLES
    
    print(id)
    print(title)
    
    try:
        if len(title) == 1:
            event = "\n\tholder = " + id
            newcontent = title_starts + " = {" + event + "\n}\n"
             
            with open(titlepath + title[0] + ".txt", "r") as f:
                content = f.read()
                x = content.find(title_starts)
                
            if x == -1:
                with open(titlepath + title + ".txt", "a") as f:
                    f.write(newcontent)
            else:
                with open(titlepath + title + ".txt", "w") as f:
                    re.sub(title_starts + r' = {\n\t.+\n}\n', newcontent, content)
                    f.write(content)
                    
        elif len(title) == 2:
                titlename = title[0]
                date = title[1]
                
                event = "\n\tholder = " + id
                newcontent = date + " = {" + event + "\n}\n"
                
                
                with open(titlepath + titlename + ".txt", "r") as f:
                    content = f.read()
                    x = content.find(date)

                if x == -1:
                    with open(titlepath + titlename + ".txt", "a") as f:
                        f.write(newcontent)
                else:
                    with open(titlepath + titlename + ".txt", "w") as f:
                        pattern = date + r' = {\n\t.+\n}\n'
                        content = re.sub(pattern, newcontent, content)
                        f.write(content)
        else:
            with open("log.txt", mode="a", encoding="utf8") as log:
                log.write("Could not set title {} for character {}\n".format(title, id))
                
    except:
        with open("log.txt", mode="a", encoding="utf8") as log:
                log.write("There is no title {} for character {}\n".format(title, id))

def readCSV(csvfile):
    with open(csvfile) as f:
        personlist = []
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            personlist.append(row)
    return personlist
            
def writePersons(persons):
    charfile = "{}\{}".format(PATH_TO_CHARS, CHARFILE)
    dynastyfile = "{}\{}".format(PATH_TO_DYNASTIES, DYNFILE)
    with open(charfile, mode='w', encoding="utf8") as chars, open(dynastyfile, mode='w', encoding='utf8') as dyn:
        
        with open("log.txt", mode="w", encoding="utf8") as log:
            log.write("Start writing characters...\n")
        
        dynastydict = {}
        dynastycounter = 1
        for person in persons:
            
            with open("log.txt", mode="a", encoding="utf8") as log:
                log.write("Writing character {} {} with id {}\n".format(person["name"],person["dynasty"],person["id"]))
        
            chars.write('%s = {\n\tname = \"%s\"'%(person["id"],person["name"]))
            
            if person["female"] == 'yes':
                chars.write("\n\tfemale = yes")
                
            chars.write("\n\treligion = %s \n\tculture = %s"%(person["religion"],person["culture"]))
            
            if len(person["dynasty"]) >= 1:
                if person["dynasty"] not in dynastydict:
                    dynastydict[person["dynasty"]] = (dynastycounter,person["culture"])
                    dyn.write("%s = {\n\tname = \"%s\""%(dynastycounter,person["dynasty"]))
                    dyn.write("\n\tculture = %s"%(person["culture"]))
                    dyn.write("\n\tused_for_random = no\n}\n\n")
                    dynastycounter += 1
                chars.write("\n\tdynasty = %s"%(dynastydict[person["dynasty"]][0]))
                
                
            if len(person["father"]) >= 1:
                chars.write("\n\tfather = %s"%(person["father"]))
                
            if len(person["mother"]) >= 1:
                chars.write("\n\tmother = %s"%(person["mother"]))
                
            if len(person["traits"]) >= 1:
                traits = person["traits"].split()
                for trait in traits:
                    chars.write("\n\tadd_trait = %s"%(trait))
                    
            if len(person["martial"]) >= 1:
                chars.write("\n\tmartial = %s"%(person["martial"]))
                
            if len(person["diplo"]) >= 1:
                chars.write("\n\tdiplomacy = %s"%(person["diplo"]))
            
            if len(person["intrigue"]) >= 1:
                chars.write("\n\tintrigue = %s"%(person["intrigue"]))
            
            if len(person["steward"]) >= 1:
                chars.write("\n\tstewardship = %s"%(person["steward"]))
            
            if len(person["learning"]) >= 1:
                chars.write("\n\tlearning = %s"%(person["learning"]))
                
            if len(person["health"]) >= 1:
                chars.write("\n\thealth = %s"%(person["health"]))
                
            if len(person["fertility"]) >= 1:
                chars.write("\n\tfertility = %s"%(person["fertility"]))
                
            if len(person["dna"]) >= 1:
                chars.write("\n\dna = %s"%(person["dna"]))
                
            if len(person["properties"]) >= 1:
                chars.write("\n\tproperties = %s"%(person["properties"]))
                
            if person["occluded"] == 'yes':
                chars.write("\n\toccluded = %s"%(person["occluded"]))
                
            chars.write("\n\t%s = {birth=yes}"%(person["birth"]))
            
            if len(person["other events"]) >= 1:
                events = person["other events"].split(', ')
                for event in events:
                    chars.write("\n\t" + event)
            
            chars.write("\n\t%s = {death=yes}"%(person["death"]))
            
            if len(person["comments"]) >= 1:
                comments = person["comments"].split()
                for comment in comments:
                    chars.write("\n\t#" + comment)
            
            chars.write("\n}\n\n")
            
            if len(person["titles"]) >= 1:
                titles = person["titles"].split()
                for title in titles:
                    title = title.split(":")
                    applytitle(person["id"], title)
            
def main():
    global PATH_TO_CHARS
    global PATH_TO_DYNASTIES
    global PATH_TO_TITLES
    global CHARFILE
    global DYNFILE
    global TITLEDEF
    
    # get the paths from the config file
    config = configparser.ConfigParser()
    config.read('chargenerator.ini')
    
    mod_path = config["PATH"]["ModDirectory"]
    
    PATH_TO_CHARS = mod_path + "\history\characters"
    PATH_TO_DYNASTIES = mod_path + "\common\dynasties"
    PATH_TO_TITLES = mod_path + "\history\\titles\\"
    
    CHARFILE = config["OUTPUT"]["Chars"]
    DYNFILE = config["OUTPUT"]["Dynasties"]
    
    TITLEDEF = config["OUTPUT"]["TitleDefault"]
    
    personlist = readCSV(PATH_TO_CHARS + "\\" + config["INPUT"]["Chars"])
    
    writePersons(personlist)

    print("Done writing!")
    

if __name__ == '__main__':
    main()