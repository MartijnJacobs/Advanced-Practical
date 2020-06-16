#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################
### Imports

###########################################################
class Person:
    
    def __init__(self, age, oth, cor, time):
        self.age = age #Int
        self.oth = oth #Bool
        self.cor = cor #Bool
        self.time = time #Float, time of arrival on certain day
        
class Patient:
    
    def __init__(self, life, time, day, ic):
        self.life = life #Bool, die or survive
        self.time = time #Float
        self.day = day #Int
        self.ic = ic #Int
        
class Event:
    
    def __init__(self, typ, pat):
        self.typ = typ #Bool, arr or dep
        self.pat = pat #Patient or Person
        self.time = self.pat.time #Float
        
class Elist:
    
    def __init__(self, elist = []):
        self.elist = elist #Array of Events
        
    def addE(self, evt):
        if len(self.elist) == 0:
            self.elist = [evt]
        else:
            te = evt.time
            if te > self.elist[-1].time:
                self.elist.append(evt)
            else:
                evstar = next(ev for ev in self.elist if ev.time > te)
                evid = self.elist.index(evstar)
                self.elist.insert(evid, evt)   
                
    def getFirstEvent(self):
        evt = self.elist.pop(0)
        return evt

    def deleteEvent(self, i):
        evt = next(ev for ev in self.elist if ev.getIdnr()== i)
        self.elist.remove(evt)
    
class IC:
    
    def __init__(self, cap, othPat, corPat, order):
        self.cap = cap #Int
        self.othPat = othPat #Array of Patients
        self.corPat = corPat #Array of Patients
        self.tot = len(self.corPat) + len(self.othPat) #Int
        self.order = order #Int

    def prIC(self):
        print("    Cap:", self.cap, "Tot:", self.tot, "Cor:", self.corPat, "Oth:", self.othPat)

def checkArr(Per, IC, iCap):
    """Checks whether an arriving person is accepted on the IC or not"""
    if iCap < IC.cap:
        if Per.age < 60:
            if Per.cor or Per.oth:
                return True
        elif Per.cor:
            if not Per.oth:
                return True
        elif Per.oth:
            if not Per.cor:
                return True
    return False
    
def procIC(elist, IC, iDay):
    """Processes the daily status of all patients on the IC:
        -Checks if their departure is today
        -Adds a day to their stay on the IC
        """
    for i in range(len(IC.corPat)):
        if IC.corPat[i].day == iDay:
            eN = Event(False, IC.corPat[i])
            elist.addE(eN)
            IC.corPat.pop(i)
        else:
            IC.corPat[i].day += 1
    for i in range(len(IC.othPat)):
        if IC.othPat[i].day == iDay:
            eN = Event(False, IC.othPat[i])
            elist.addE(eN)
            IC.othPat.pop(i)
        else:
            IC.othPat[i].day += 1

def procDep(pat):
    """Processes the departure of a patient"""
    sL = "alive"
    sD = "dead"
    sP = " "
    if pat.life:
        sP = sL
    else:
        sP = sD
    print("At", pat.time, "hours today, a patient left the IC", sP)    
            
def procDay(elist, IC, iM, iDay):
    """Processes a full day on the IC:
        -Checks the current patients
        -Adds departures to the EL
        -Goes through the full EL with arriving persons
        """
    iCap = IC.tot
    procIC(elist, IC, iDay)
    for i in range(len(elist.elist)):
        if len(elist.elist) > 0:
            eN = elist.getFirstEvent()
            if not eN.typ:
                iCap += 1
                procDep(eN.pat)
            else:
                if checkArr(eN.pat, IC, iCap):
                    iCap -= 1
                    pA = Patient(True, i, 3, 0) #Generate time in system
                    if eN.pat.cor:
                        IC.corPat.append(pA)
                    else:
                        IC.othPat.append(pA)
                    procArr(eN.pat, True)
                else:
                    procArr(eN.pat, False)
                
def procArr(per, bol):
    """Processes the arrival of a person"""
    sC = "corona"
    sO = "something unspecified"
    sP = " "
    if per.cor:
        sP = sC
    else:
        sP = sO
    if bol:
        print("At", per.time, "hours today, a patient entered the IC with", sP)
    else:
        print("At", per.time, "hours today, a person with", sP, "was rejected from the IC")
            
### main
def main(): 
    iM = 24
    
    iD = 150
    vE = []
    par = Patient(True, 15, 1, 1)
    UMC = IC(7, [par], [], 0)
    pat = Person(35, False, True, 14)
    pit = Person(72, True, True, 18)
    pyt = Person(43, False, True, 16)
    pet = Person(65, True, False, 20)
    eA = Event(True, pat)
    eB = Event(True, pit)
    eC = Event(True, pyt)
    eD = Event(True, pet)
    LA = Elist([eA, eB, eD])
    LA.addE(eC)
    procDay(LA, UMC, iM, 1)
    """
    pot = Person(28, True, True, False)
    put = Person(55, False, True, False)
    pbt = Person(25, True, False, False)
    vF = [pot]
    vG = [put]
    vH = [pbt]
    vN = [vA, vB, vC, vD, vF, vG, vH]
    procWeek(UMC, vE, vN)
    
    #LA.prEL()
    """
###########################################################
### start main
if __name__ == "__main__":
    main()
