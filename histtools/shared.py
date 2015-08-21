# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 09:27:49 2015

Style dictionaries from database

@author: bbatt
"""

#Subtypes used in geodatabase
subtypes = {
0: "Barn", 
1: "Cemetery",
2: "Church",
3: "Commercial",
4: "Gas Station",
5: "House",
6: "Other",
7: "Outbuilding",
8: "School",
}

#Eligibility for domains
eligdict = {
"E": "Eligible",
"NE": "Not Eligible",
"L": "Listed",
"PE": "Recommended Eligible",
"U":"Unknown"
}

#Style domains, shared by all subtypes
styledict = {
'COL' : 'Colonial Revival',
'CRF' : 'Craftsman',
'ECR' : 'Early Classical Revival',
'EVR' : 'English Vernacular Revival',
'FE' : 'Federal',
'FR' : 'Federal Revival',
'FV' : 'Folk Victorian',
'FVR' : 'French Vernacular Revival',
'GE' : 'Georgian',
'GOV' : 'Gothic Revival',
'GRV' : 'Greek Revival',
'HVE' : 'High Victorian Eclectic',
'INT' : 'International ',
'IRR' : 'Italian Renaissance Revival',
'ITA' : 'Italianate',
'MR' : 'Mediterranean Revival',
'NR' : 'Neoclassical Revival',
'NS' : 'No Style',
'PR' : 'Prairie',
'QA' : 'Queen Anne',
'SE' : 'Second Empire',
'SCR' : 'Spanish Colonial Revival',
'ST' : 'Stick'
}