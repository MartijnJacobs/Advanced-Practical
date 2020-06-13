# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:22:12 2020

@author: ehess
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import gamma
import numpy.random as rnd


def LogNormalMLE(vX):
    iN = len(vX)
    
    dNum = 0
    for i in range(iN):
        if vX[i] != 0:    
            dNum += np.log(vX[i])
            
    dMu = dNum/iN
    
    dNum = 0
    for i in range(iN):
        if vX[i] != 0:
            dNum += (np.log(vX[i]) - dMu)**2
    dSigma = dNum/iN
    
    return dMu, dSigma
        
def LogNormalPDF(dMu, dSigma, iN):

    vLogNormal = np.empty(iN)
    for i in range(iN):
        vLogNormal[i] = (i * dSigma * np.sqrt(2 * np.pi))**-1 * np.exp(-(np.log(i)- dMu)**2/2*dSigma**2)
    return vLogNormal

def GammaPDF(dAlpha, dBeta, iN):
    
    vGamma = np.empty(iN)
    
    for i in range(iN):
        vGamma[i] = dBeta**dAlpha * i **(dAlpha-1) * np.exp(-dBeta*i) / gamma(dAlpha)
    return vGamma

def ExpRANDOM(dRate):
    return -np.log(rnd.rand())/dRate     

def main(): 
    #initialization
    
    #import data
    url = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data-geo/data-national/RIVM_NL_national.csv'
    url2 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data-ic/data-nice/NICE_IC_wide_latest.csv'
    
    df = pd.read_csv(url, error_bad_lines=False)
    dfAantal = df.loc[df["Type"] == "Totaal", "Aantal"]
    dfAantalCumulatief = df.loc[df["Type"] == "Totaal", "AantalCumulatief"]
    dfZiekenhuis = df.loc[df["Type"] == "Ziekenhuisopname", "Aantal"]
    
    vAantal = dfAantal.values
    vAantalCumulatief = dfAantalCumulatief.values
    vZiekenhuis = dfZiekenhuis.values
    
    df2 = pd.read_csv(url2, error_bad_lines=False)
    dfICToename = df2.loc[:, "ToenameOpnamen"]
    dfICCum = df2.loc[:, "CumulatiefOpnamen"]
    
    vICToename = dfICToename.values
    vICCum = dfICCum.values
    
    #estimated values
    iN = 17414806 #population
    iN2 = 0.055 * iN #population infected in Netherlands estimated
    dBeta = 0.6 #infection rate
    iDays = 150 
    iDaysLog = 100
    dP = 0.003 #percentage of IC from total people infected
    dCompare = 0.05 #percentage of infected people that have also been tested
    
    dLambda = 0.167 #incubatietijd van coronavirus 1/days
    dGammaMild = 0.125 #duur van herstel voor milde gevallen 1/days
    dGammaHard = 0.0556 #duur van herstel voor zware gevallen 1/days
    
    #SEIRS Model
    vS = np.empty(iDays)
    vI = np.empty(iDays)
    vE = np.empty(iDays)
    vHos = np.empty(iDays)
    vHosCum = np.empty(iDays)
    vdI = np.empty(iDays)
    vCompare = np.empty(iDays)
    vS[0] = iN2
    vI[0] = 6
    vE[0] = 1
    
    for i in range(len(vS)-1):
        vS[i+1] = vS[i] + (-dBeta * vI[i] * vS[i])/iN2 #hoeveelheid mensen die besmet kunnen raken
        vE[i+1] = vE[i] + ( dBeta * vI[i] * vS[i])/iN2 - dLambda * vE[i] #hoeveelheid mensen die zijn besmet maar nog niet ziek
        vI[i+1] = vI[i] + dLambda * vE[i] - dP * dGammaHard * vI[i] - (1-dP) * dGammaMild * vI[i] #hoeveelheid zieke mensen
        
        vdI[i+1] = dLambda * vE[i] #dagelijkse nieuwe hoeveelheid geinfecteerde mensen
        vHos[i+1] = dP * vdI[i+1] #percentage van alle covid gevallen die in het ziekenhuis zijn beland
        vHosCum[i+1] = vHosCum[i] + dP * vdI[i+1] #zelfe maar dan cumulatief
        vCompare[i+1] = dCompare * vdI[i+1] #hoeveelheid van alle gevallen die zijn getest
             
    vHos[0] = 0
    
    #Subtract start of model
    vHosAlter = vHos[45:150]
    vHosCumAlter = vHosCum[45:150] 
    
    #Estimated lognormal 
    #(dMu, dSigma) = LogNormalMLE(vICToename) #deze waarden lijken niet te kloppen
    vLogNormal = LogNormalPDF(3.5,3,iDaysLog)
    vICDist = 25000 * vLogNormal
    
    #plots
    plt.plot(vHosAlter)
    plt.plot(vICToename)
    plt.title("hoeveelheid opgenome mensen per dag op IC met benadering met SEIR model")
    plt.show()
    
    plt.plot(vHosCumAlter)
    plt.plot(vICCum)
    plt.title("totale hoeveelheid opgenome mensen op IC met benadering met SEIR model")
    plt.show()
    

    plt.plot(vICDist)
    plt.plot(vICToename)
    plt.title("Benadering IC opnames met Lognormale verdeling met mu = 3.5 en sigma = 3")
    plt.show()
    
    #Estimated average stay on IC
    vGamma = GammaPDF(19, 1, 40)
    plt.plot(vGamma)
    plt.title("verblijfsduur IC met gemiddelde van 18")
    plt.show()
    
    vGamma2 = GammaPDF(8, 1, 40)
    plt.plot(vGamma2)
    plt.title("verblijfsduur IC met gemiddelde van 7")
    plt.show()
    
    #draw random number
    dTime = 0
    iDay = 0
    vPatients = np.zeros(100)
    while iDay != 99:
        if dTime < 1440:
            dRandom = ExpRANDOM(vICDist[iDay]/1440)
            if dRandom < 1440:
                dTime += dRandom
                vPatients[iDay] += 1
            else:
                dTime = 0
                iDay +=1
                
        else:
            dTime = dTime-1440
            iDay +=1
            dRandom = ExpRANDOM(vICDist[iDay]/1440)
            dTime += dRandom
            vPatients[iDay] += 1
        
        print(dTime)
        
    print(iDay)
    print(vPatients)
    plt.plot(vPatients)
    plt.plot(vICToename)
    plt.show()
    
    
    

    
################ now call the main ############
if __name__== '__main__':
    main()
