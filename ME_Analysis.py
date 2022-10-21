# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:36:19 2022

@author: therobe7
"""

#import packages
from RanProg import merge2
import PySimpleGUI as sg
from pathlib import Path
import pandas as pd
import os
from GeochemPlots import GenGraphTrace as plot

#get the path of the current user
UserName = os.path.expanduser('~')
pathDL = UserName + r'\Downloads'

#set up GUI for selecting ME and LOI data
#ui messages
sNote1 = """It is suggested that you add a column to separate
the data by location, called \'location\', otherwise
the data will be treated as if it were all from the
same location"""
sNote2 = """Upload csv from containing ME from XRF"""
sNote3 = """Upload excel sheet containing LOI informaiton"""
# Open dialog window that allows you to choose the file:
event, sPath = sg.Window(
    'Select HAWK .csv',
    [[sg.Text(sNote1)],
        [sg.Text(sNote2)],
        [sg.Input('C:/Users/therobe7/OneDrive/SRC_and_Research/XRF/Sevvy ME (10Aug).csv'),\
         sg.FileBrowse()],
        [sg.Text(sNote3)],
        [sg.Input('C:/Users/therobe7/OneDrive/SRC_and_Research/XRF/LOI.excel'),\
         sg.FileBrowse()],
        [sg.OK(), sg.Cancel()]]
    ).read(close=True)

# Converts path to work on all operating systems
sMyPath1 = Path(sPath[0])
sMyPath2 = Path(sPath[1])

df1 = pd.read_csv(sMyPath1)
df2 = pd.read_excel(sMyPath2)

#merge data
dfm = merge2(df1, df2, 'Sample','N')

#Check sample, export those samples to downloads as csv
dfm['Total'] = dfm.sum(axis=0,skipna=True) + dfm['LOI meas']
dfCheck = dfm.where(dfm['Total']).gt(98.5)
dfCheck.to_csv(pathDL + r'\CheckSamples.csv')

#TODO: preform stats and append to bottom

#TODO: normalize, export data to downloads as csv

#TODO: Plot TAS

#Plot Date-total
plot(dfm,'location','Date','Total','Date','Total wt%','Date-Total')

#plot total/LOI
plot(dfm,'location','LOI','Total','Loss on Ignition','Total (wt%)','Total vs LOI')

#plot Fe/Ti
plot(dfm,'location','TiO2','Fe2O3','TiO2 (wt%)','Fe2O3 (wt%)','Iron vs Titanium')