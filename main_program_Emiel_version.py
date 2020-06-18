#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################
### Imports

import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

###########################################################
class Person:
    
    def __init__(self, age, oth, cor, time):
        self.age = age #Int
        self.oth = oth #Bool
        self.cor = cor #Bool
        self.time = time #Float, time of arrival on certain day
        
class Patient:
    
    def __init__(self, agegroup):
        self.agegroup = agegroup
        
    def getAgeGroup(self):
        return self.agegroup
    
    def Survival(self):
        if self.agegroup == 1:
            if np.random.rand() > 0.1:
                return True
        elif self.agegroup == 2:
            if np.random.rand() > 0:
                return True
        elif self.agegroup == 3:
            if np.random.rand() > 0.154:
                return True
            else:
                return False
        elif self.agegroup == 4:
            if np.random.rand() > 0.111:
                return True
            else:
                return False
        elif self.agegroup == 5:
            if np.random.rand() > 0.1667:
                return True
            else:
                return False
        elif self.agegroup == 6:
            if np.random.rand() > 0.0612:
                return True
            else:
                return False
        elif self.agegroup == 7:
            if np.random.rand() > 0.141:
                return True
            else:
                return False
        elif self.agegroup == 8:
            if np.random.rand() > 0.112:
                return True
            else:
                return False
        elif self.agegroup == 9:
            if np.random.rand() > 0.2396:
                return True
            else:
                return False
        elif self.agegroup == 10:
            if np.random.rand() > 0.2667:
                return True
            else:
                return False
        elif self.agegroup == 11:
            if np.random.rand() > 0.3996:
                return True
            else:
                return False
        elif self.agegroup == 12:
            if np.random.rand() > 0.4654:
                return True
            else:
                return False
        elif self.agegroup == 13:
            if np.random.rand() > 0.5855:
                return True
            else:
                return False
        elif self.agegroup == 14:
            if np.random.rand() > 0.7241:
                return True
            else:
                return False
        elif self.agegroup == 15:
            if np.random.rand() > 0.6923:
                return True
            else:
                return False
        
class Event:
    def __init__(self, time = 0, typ = '', corona = False):
        self.info = (time, typ, corona) #Bool, arr or dep
        
    def getTime (self):
        return self.info[0]

    def getType( self ):
        return self.info[1]
    
    def Corona(self):
        return self.info[2]
        
class Elist:
    
    def __init__(self, elist = []):
        self.elist = elist #Array of Events
        
    def addE(self, evt):
        if len(self.elist) == 0:
            self.elist = [evt]
        else:
            te = evt.getTime()
            if te > self.elist[-1].getTime():
                self.elist.append(evt)
            else:
                evstar = next(ev for ev in self.elist if ev.getTime() > te)
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
    

def returnAge():
    vAgeGroups = np.arange(1, 16)
    pk = (0.0041, 0.0026, 0.0053, 0.0111, 0.0147, 0.0201, 0.0580, 0.0838, 0.1279, 0.1532, 0.1830, 0.1949, 0.1123, 0.02369, 0.00531)
    ageDist = stats.rv_discrete(name='ageDist', values = (vAgeGroups, pk))
    return ageDist.rvs()
    
    
def procDep(dTime, vAgeGroups):
    """Processes the departure of a patient"""
    sL = "alive"
    sD = "dead"
    sP = " "
    
    pat = Patient(returnAge())
    age = pat.getAgeGroup()
    vAgeGroups = vAgeGroups.append(age)
    bSur = pat.Survival()
    if bSur == True:
        sP = sL
    else:
        sP = sD
    #print("At", dTime, "hours today, a patient left the IC", sP) 
    
    if bSur == False:
        return 1
    else:
        return 0
            
                
def procArr(dLambda, iBeds, L, dTime, iPatients):
    """Processes the arrival of a person"""
    sC = "corona"
    sO = "something unspecified"
    sP = " "
    
    dNewArr = ExpRANDOM(dLambda)
    eva = Event(dTime + dNewArr, 'arr', True)
    L.addE(eva)
    
    if eva.Corona:
        sP = sC
    else:
        sP = sO
        
    if iPatients < iBeds: #check if there is space on intensive care
        dStay = np.random.lognormal(2.7, 0.8) #if so, then determine how long the patient will stay
        evb = Event(dTime + dStay, 'dep') #create a new event
        L.addE(evb) #and add it to the event list
        #print("At", dTime, "hours today, a patient entered the IC with", sP)
        return 1
    else:
        #print("At", dTime, "hours today, a person with", sP, "was rejected from the IC")
        return 0
        
def ExpRANDOM(dRate):
    return -np.log(rnd.rand())/dRate     
            
def simRun(vLambda, iBeds, vPatients, vDeaths):
    dTime = 0 #starting time
    iPatients = 0 #starting amount of patients
    iDeaths = 0
    iDay = 0 #starting day
    vAgeGroups = []
    L = Elist()
    evt = Event(ExpRANDOM(vLambda[0]), 'arr', True) # first arrival is someone with corona
    L.addE(evt)
    
    """Here the simulation is run for 100 days, so dTime gets added up until it is equal to 99"""
    while dTime < 99:
        dLambda = vLambda[iDay] #search for the lambda of the day
        evt = L.getFirstEvent() #search for the first event in the list
        dType = evt.getType() #find the type of event, either arrival or departure
        dTime = evt.getTime() #get the time of the event
        iDay = int(dTime) #check what day it is
        vPatients[iDay] = iPatients #set the current amount of patients on IC equal to the patients on the right day
        vDeaths[iDay] = iDeaths
        
        """Two possibilities: it is an arrival or a departure"""
        if dType == 'arr': 
            iPatients += procArr(dLambda, iBeds, L, dTime, iPatients)
        else:
            iDeaths += procDep(dTime, vAgeGroups)
            iPatients -= 1 
        
    vPatients[-1] = vPatients[-2]
    vDeaths[-1] = vDeaths[-2]
    
    return vPatients, vDeaths, vAgeGroups
    
def SEIRmodel(iN, iDays, dP, dLambda, dGammaMild, dGammaHard):
    
    #SEIRS Model
    vS = np.empty(iDays)
    vI = np.empty(iDays)
    vE = np.empty(iDays)
    vHos = np.empty(iDays)
    vdI = np.empty(iDays)
    vS[0] = iN
    vI[0] = 6
    vE[0] = 1
    
    fBeta = lambda x: 2.5 - 0.055 * x if (2.5 - 0.055 * x>0.4) else 0.25
    
    for i in range(len(vS)-1):
        vS[i+1] = vS[i] + (-fBeta(i) * vI[i] * vS[i])/iN #hoeveelheid mensen die besmet kunnen raken
        vE[i+1] = vE[i] + ( fBeta(i) * vI[i] * vS[i])/iN - dLambda * vE[i] #hoeveelheid mensen die zijn besmet maar nog niet ziek
        vI[i+1] = vI[i] + dLambda * vE[i] - dP * dGammaHard * vI[i] - (1-dP) * dGammaMild * vI[i] #hoeveelheid zieke mensen
        
        vdI[i+1] = dLambda * vE[i] #dagelijkse nieuwe hoeveelheid geinfecteerde mensen
        vHos[i+1] = dP * vdI[i+1] #percentage van alle covid gevallen die in het ziekenhuis zijn beland
             
    vHos[0] = 0
    
    #Subtract start of model
    vHosAlter = vHos[11:iDays]
    
    return vHosAlter


def Simulations(iN, iDays, dP, dLambda, dGammaMild, dGammaHard, iBeds, iSimRuns, vICdata):
    
    vPatientsCum = np.zeros(101)
    vDeathsCum = np.zeros(101)
    vAgeGroupsCum = []
    print(type(vAgeGroupsCum))
    
    for i in range(iSimRuns):
        vLambda = SEIRmodel(iN, iDays, dP, dLambda, dGammaMild, dGammaHard)
        (vPatients, vDeaths, vAgeGroups) = simRun(vLambda, iBeds, np.zeros(101), np.zeros(101))
        
        vPatientsCum += vPatients
        print(vPatientsCum)
        print(vPatients)
        vDeathsCum += vDeaths
        vAgeGroupsCum.extend(vAgeGroups)
        
    vPatients = vPatientsCum/iSimRuns
    vDeaths = vDeathsCum/iSimRuns
    
    plt.plot(vPatients) #our simulation
    plt.plot(vICdata) #real data
    plt.plot(vDeaths)
    plt.show()
    
    plt.hist(vAgeGroups, bins=15)
    plt.show()
    
    
    
def main(): 
    url2 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data-ic/data-nice/NICE_IC_wide_latest.csv'
    df2 = pd.read_csv(url2, error_bad_lines=False)
    dfICdata = df2.loc[:, "TotaalOpnamen"]
    vICdata = dfICdata.values
    
    iSimRuns = 10
    iBeds = 4000
    vPatients = np.zeros(101)
    
    iN = 17414806 #population
    iN = 0.06 * iN #population infected in Netherlands estimated
    iDays = 120 
    dP = 0.003 #percentage of IC from total people infected
    
    dLambda = 0.167 #incubatietijd van coronavirus 1/days
    dGammaMild = 0.125 #duur van herstel voor milde gevallen 1/days
    dGammaHard = 0.0556 #duur van herstel voor zware gevallen 1/days
    
    Simulations(iN, iDays, dP, dLambda, dGammaMild, dGammaHard, iBeds, iSimRuns, vICdata)

###########################################################
### start main
if __name__ == "__main__":
    main()
