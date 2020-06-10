#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################
### Imports

###########################################################
def hospEntry(Pat, IC):
    """Checks whether a patient is accepted on the IC or not"""
    if IC.tot < IC.cap:
        if Pat.age < 60:
            if Pat.cor or Pat.oth:
                return True
        elif not (Pat.cor and Pat.oth):
            return True
    return False

def procIC(Pat, IC):
    """Processes a patients status on the IC:
        -if the patient has entered the IC at all
        -how many days since entrance
    """
    if type(Pat.ic) == int and Pat.ic >= 0:
        print(Pat.ic)
        Pat.ic += 1
    if type(Pat.ic) == bool and Pat.ic == False:
        if hospEntry(Pat, IC):
            print("Made it to the IC man")
            Pat.ic= 1
            IC.tot += 1
            if Pat.cor:
                IC.corPat += 1
            elif Pat.oth:
                IC.othPat += 1
            return True
        else:
            print("This is a dead man")
            return False

class Patient:
    
    def __init__(self, age, oth, cor, ic):
        self.age = age #Int
        self.oth = oth #Bool
        self.cor = cor #Bool
        self.ic = ic #Bool -> Int if accepted on IC
    
class IC:
    
    def __init__(self, cap, corPat, othPat, order):
        self.cap = cap #Int
        self.corPat = corPat #Int
        self.othPat = othPat #Int
        self.tot = self.corPat + self.othPat #Int
        self.order = order #Int
        
    def prIC(self):
        print("Cap:", self.cap, "Tot:", self.tot, "Cor:", self.corPat, "Oth:", self.othPat)
        
    def orderBeds(self, iDay):
        if (self.cap + self.order - self.tot) <= 5:
            self.order += 5
        print("Day", iDay + 1, ", Order is", self.order)
        if iDay == 6:
            print("Order", self.order, "beds")
            self.order = 0
        
def procDay(IC, vP, vN, iDay):
    """Processes a day with new patients entering"""
    IC.prIC()
    for i in vP:
        procIC(i, IC)
    for i in vN:
        if procIC(i, IC):
            vP.append(i)
    IC.prIC()
    IC.orderBeds(iDay)
    return vP

def procWeek(IC, vE, vN):
    """Processes a full week with new patients entering daily"""
    for i in range(len(vN)):
        vE = procDay(IC, vE, vN[i], i)
    return vE
    
### main
def main():  
    vE = []
    UMC = IC(629, 500, 120, 0)
    pat = Patient(35, False, True, False)
    pet = Patient(65, True, False, False)
    pot = Patient(28, True, True, False)
    pit = Patient(72, True, True, False)
    put = Patient(55, False, True, False)
    pyt = Patient(43, False, True, False)
    pbt = Patient(25, True, False, False)
    vA = [pat]
    vD = [pet]
    vF = [pot]
    vB = [pit]
    vG = [put]
    vC = [pyt]
    vH = [pbt]
    vN = [vA, vB, vC, vD, vF, vG, vH]
    procWeek(UMC, vE, vN)
###########################################################
### start main
if __name__ == "__main__":
    main()
