# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 00:11:19 2020

@author: ehess
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################
### Imports

import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
#import seir

###########################################################
class Person:
    
    def __init__(self, age, time):
        self.age = age #Int
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
            if np.random.rand() > 0.1176:
                return True
            else:
                return False
        elif self.agegroup == 4:
            if np.random.rand() > 0.0857:
                return True
            else:
                return False
        elif self.agegroup == 5:
            if np.random.rand() > 0.15:
                return True
            else:
                return False
        elif self.agegroup == 6:
            if np.random.rand() > 0.0741:
                return True
            else:
                return False
        elif self.agegroup == 7:
            if np.random.rand() > 0.125:
                return True
            else:
                return False
        elif self.agegroup == 8:
            if np.random.rand() > 0.0916:
                return True
            else:
                return False
        elif self.agegroup == 9:
            if np.random.rand() > 0.206:
                return True
            else:
                return False
        elif self.agegroup == 10:
            if np.random.rand() > 0.226:
                return True
            else:
                return False
        elif self.agegroup == 11:
            if np.random.rand() > 0.3666:
                return True
            else:
                return False
        elif self.agegroup == 12:
            if np.random.rand() > 0.4148:
                return True
            else:
                return False
        elif self.agegroup == 13:
            if np.random.rand() > 0.5292:
                return True
            else:
                return False
        elif self.agegroup == 14:
            if np.random.rand() > 0.6774:
                return True
            else:
                return False
        elif self.agegroup == 15:
            if np.random.rand() > 0.6:
                return True
            else:
                return False
        
class Event:
    def __init__(self, time = 0, typ = '', agegroup = 0, survival=True):
        self.info = (time, typ, agegroup, survival) #Bool, arr or dep
        
    def getTime (self):
        return self.info[0]

    def getType( self ):
        return self.info[1]
    
    def getAgeGroup(self):
        return self.info[2]
    
    def getSurvival(self):
        return self.info[3]
    

        
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
    
def returnAge():
    vAgeGroups = np.arange(1, 16)
    pk = (0.0041, 0.0026, 0.0053, 0.0111, 0.0147, 0.0201, 0.0580, 0.0838, 0.1279, 0.1532, 0.1830, 0.1949, 0.1123, 0.02369, 0.00531)
    ageDist = stats.rv_discrete(name='ageDist', values = (vAgeGroups, pk))
    return ageDist.rvs()       
                
def procArr(dLambda, iBeds, L, dTime, iPatients):
    """Processes the arrival of a person"""
    dNewArr = ExpRANDOM(dLambda)
    eva = Event(dTime + dNewArr, 'arr')
    L.addE(eva)
        
    if iPatients < iBeds: #check if there is space on intensive care
        pat = Patient(returnAge())
        age = pat.getAgeGroup()
        bSur = pat.Survival()
        #print(bSur)
        if bSur == True:
            #dStay = ExpRANDOM(1/19.59)
            #dStay = ExpRANDOM(1/22.5)
            dStay = np.random.lognormal(2.9, 0.7)
        else:
            dStay = ExpRANDOM(1/13.96)
            #dStay = ExpRANDOM(1/21.2)
            #dStay = np.random.lognormal(2.3, 0.7)
        #dStay = np.random.lognormal(2.7, 0.8) #if so, then determine how long the patient will stay
        evb = Event(dTime + dStay, 'dep', age, bSur) #create a new event
        L.addE(evb) #and add it to the event list
        return 1
    else:
        return 0    
        
def procDep(vAgeGroups, Event):
    """Processes the departure of a patient"""
    #pat = Patient(returnAge())
    age = Event.getAgeGroup()
    bSur = Event.getSurvival()
    vAgeGroups = vAgeGroups.append(age)
    #bSur = pat.Survival()
    if not bSur:
        return 1, age
    else:
        return 0, age

def ExpRANDOM(dRate):
    return -np.log(rnd.rand())/dRate     
            
def simRun(vLambda, iBeds, vPatients, vDeaths, vRej, vRD):
    dTime = 0 #starting time
    iPatients = 0 #starting amount of patients
    iDeaths = 0
    iDay = 0 #starting day
    iRej = 0
    iRD = 0
    vAgeGroups = []
    vAgeD = []
    L = Elist()
    evt = Event(ExpRANDOM(vLambda[0]), 'arr', 0, True) # first arrival is someone with corona
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
        vRej[iDay] = iRej
        vRD[iDay] = iRD
        
        """Two possibilities: it is an arrival or a departure"""
        if dType == 'arr': 
            N = procArr(dLambda, iBeds, L, dTime, iPatients)
            iPatients += N
            iRej += 1 - N
            if N == 0:
                r = (np.random.choice(2, p = [0.02, 0.98]))
                iDeaths += r
                iRD += r
        else:
            r, age = procDep(vAgeGroups, evt)
            iDeaths += r
            if r == 1:
                vAgeD.append(age)
            iPatients -= 1 
           
        
    vPatients[-1] = vPatients[-2]
    vDeaths[-1] = vDeaths[-2]
    vRej[-1] = vRej[-2]
    vRD[-1] = vRD[-2]
    
    return vPatients, vDeaths, vAgeGroups, vRej, vRD, vAgeD

def Simulations(iN, iDays, dP, dLambda, dGammaMild, dGammaHard, iBeds, iSimRuns):
    
    vPatientsCum = np.zeros(101)
    vDeathsCum = np.zeros(101)
    vRej = np.zeros(101)
    vRD = np.zeros(101)
    vAgeGroupsCum = [] 
    vAgeDCum = []
    for i in range(iSimRuns):
        vLambda = SEIRmodel(iN, iDays, dP, dLambda, dGammaMild, dGammaHard)
        (vPatients, vDeaths, vAgeGroups, vRej, vRD, vAgeD) = simRun(vLambda, iBeds, np.zeros(101), np.zeros(101), vRej, vRD)
        
        vPatientsCum += vPatients
        #print(vPatientsCum)
        #print(vPatients)
        vDeathsCum += vDeaths
        vAgeGroupsCum.extend(vAgeGroups)
        vAgeDCum.extend(vAgeD)
        
    vPatients = vPatientsCum / iSimRuns
    vDeaths = vDeathsCum / iSimRuns
    vRej = vRej / iSimRuns
    vRD = vRD / iSimRuns
    return (vPatients, vDeaths, vRej, vAgeGroups, vRD, vAgeD)    
    
def barToLine(vA):
    vB = np.zeros(max(vA))
    for i in vA:
        vB[i - 1] += 1
    return vB

def calcMortality(vNum, vDen):
    vA = np.zeros(len(vNum))
    for i in range(len(vNum)):
        vA[i] = vNum[i]/vDen[i]
    return vA

def occupy(iBeds, vPatients):
    vA = np.zeros(len(vPatients))
    for i in range(len(vPatients)):
        vA[i] = vPatients[i] / iBeds
    return vA

def printMortality(vA, vB):
    for i in range(len(vA)):
        print(str(round(100*vA[i], 3)) + "% of age group", i + 1, "died, based on", int(vB[i]), "patients.")
    
def main(): 
    url2 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data-ic/data-nice/NICE_IC_wide_latest.csv'
    df2 = pd.read_csv(url2, error_bad_lines=False)
    dfICdata = df2.loc[:, "TotaalOpnamen"]
    vICdata = dfICdata.values
    
    iSimRuns = 1
    iBeds = 1410
    vPatients = np.zeros(101)
    
    iN = 17414806 #population
    iN = 0.06 * iN #population infected in Netherlands estimated
    iDays = 110 
    dP = 0.003 #percentage of IC from total people infected
    
    dLambda = 0.167 #incubatietijd van coronavirus 1/days
    dGammaMild = 0.125 #duur van herstel voor milde gevallen 1/days
    dGammaHard = 0.0556 #duur van herstel voor zware gevallen 1/days
    
    (vPatients, vDeaths, vRej, vAgeGroups, vRD, vAgeD) = Simulations(iN, iDays, dP, dLambda, dGammaMild, dGammaHard, iBeds, iSimRuns)
    plt.plot(vPatients, label='Simulated patients') #our simulation
    plt.plot(vICdata, label='Given data') #real data
    plt.plot(vDeaths, label='Deaths')
    plt.plot(vRej, label='Rejected patients')
    plt.hlines(iBeds, 0, 100, label='Beds')
    plt.title('Number of patients over time')
    ax = plt.subplot(111)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    
    print(str(int(vRej[100])) + " people were rejected, of which " + str(int(vRD[100])) + " people died.")
    print(str(len(vAgeGroups)) + " people left the IC, of which " + str(len(vAgeD)) + " dead.") 
    print("Which comes down to a total deathcount of " + str(int(vDeaths[100])) + ".")
    
    plt.hist(vAgeGroups, bins=15, label='Patients')
    plt.hist(vAgeD, bins=15, label='Deaths')
    plt.title('Patients & Deaths per age group')
    ax = plt.subplot(111)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    
    vOcc = occupy(iBeds, vPatients)
    plt.plot(vOcc)
    plt.title('Percentage of beds being occupied')
    plt.show()
    
    vBarsDep = barToLine(vAgeGroups)
    vBarsDea = barToLine(vAgeD)
    vMort = calcMortality(vBarsDea, vBarsDep)
    printMortality(vMort, vBarsDep)

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
###########################################################
### start main
if __name__ == "__main__":
    main()