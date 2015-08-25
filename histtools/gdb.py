# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 08:34:31 2015

History Geodatabase Tools

Suite of tools for working with environmental database
and ArcGIS Collector

@author: bbatt
"""

import os
import arcpy
from operator import itemgetter

from shared import domains, eligdict, styledict, subtypes

def generate_domains(gdb, domain_dict, xlsx):
    #Pull domain values from pre-formatted xlsx
    for dom in domain_dict.viewkeys():
        try:
            domTable = os.path.join(xlsx, dom + "$")
            codeField = "Code"
            descField = "Name"
            domDesc = domain_dict.get(dom)         
            # Process: Create a domain from an existing table
            arcpy.TableToDomain_management(domTable, codeField, descField, 
                                     gdb, dom, domDesc, "REPLACE")         
        except Exception, e:
            print e.message

def create_history_gdb(location):
    #xlsx that contains all required domains
    xlsx = os.path.join(os.path.dirname(__file__), 
                        "../templates/HistoryDomainsGA.xlsx")
    gdbname = "HistorySurvey.gdb"
    if arcpy.Exists(os.path.join(location, gdbname)):
        arcpy.Delete_management(os.path.join(location, gdbname))
    arcpy.CreateFileGDB_management(location, gdbname)
    gdb = os.path.join(location, gdbname)    
    generate_domains(gdb, domains, xlsx)
    return gdb
    
def create_structures_fc(gdb):
    """
    Create Historic Structures feature class
    """
    arcpy.env.workspace = gdb
    fc = "HistoricStructures"
    spatref = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")
    if arcpy.Exists(fc):
        arcpy.Delete_management(os.path.join(gdb, fc))
    has_m = "DISABLED"
    has_z = "DISABLED"
    req = "NON_REQUIRED"
    # Execute CreateFeatureclass
    arcpy.CreateFeatureclass_management(gdb, fc, "POINT", "", 
                                        has_m, has_z, spatref)
    arcpy.AddField_management(fc, "ResourceID", "LONG", "", "", "", 
                              "Resource ID", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "PropName", "TEXT", "", "", 100, 
                              "Resource Name", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "StrucType", "LONG", "", "", "", 
                              "Structure Type", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "BldType", "TEXT", "", "", 3, 
                              "Building Type", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "StyleType", "TEXT", "", "", 3, 
                              "Architectural Style", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "Eligibility", "TEXT", "", "", 3, 
                              "Eligibility Status", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "ConstYr", "LONG", "", "", "", 
                              "Construction Year", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "Address", "TEXT", "", "", 200, "Address", 
                              "NULLABLE", req,"")
    arcpy.AddField_management(fc, "Notes", "TEXT", "", "", 200, "Notes", 
                              "NULLABLE", req,"")
    arcpy.AddGlobalIDs_management(fc)
    arcpy.AddField_management(fc, "EPProject", "TEXT", "", "", 20, 
                              "EPEI Project ID", "NULLABLE", req,"")
    arcpy.SetSubtypeField_management(fc, "StrucType")
    for item in subtypes.items():
        arcpy.AddSubtype_management(fc, item[0], item[1])
    arcpy.SetDefaultSubtype_management(fc, 5)
    for item in subtypes.items():    
        arcpy.AssignDomainToField_management(fc, "BldType", item[1], item[0])
    subs = ['0', '1', '2', '3', '4', '6' ,'7' ,'8']
    arcpy.AssignDomainToField_management(fc, "StyleType", "Styles", subs)
    arcpy.AssignDomainToField_management(fc, "Eligibility", "Eligibility", subs)
    arcpy.AssignDefaultToField_management(fc,"Eligibility", "U", subs)
    arcpy.AssignDefaultToField_management(fc,"StyleType", "NS", subs)
    arcpy.AssignDefaultToField_management(fc,"BldType", "OT", subs)
    arcpy.AssignDefaultToField_management(fc, "BldType", "NAT", '5')
    return os.path.join(gdb, fc)

def create_districts_fc(gdb):
    """
    Create historic districts feature class
    """
    arcpy.env.workspace = gdb
    fc = "HistoricBoundary"
    spatref = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")
    if arcpy.Exists(fc):
        arcpy.Delete_management(os.path.join(gdb, fc))
    has_m = "DISABLED"
    has_z = "DISABLED"
    req = "NON_REQUIRED"
    # Execute CreateFeatureclass
    arcpy.CreateFeatureclass_management(gdb, fc, "POLYGON", "", 
                                        has_m, has_z, spatref)
    arcpy.AddField_management(fc, "ResourceID", "LONG", "", "", "", 
                              "Resource ID", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "PropName", "TEXT", "", "", 100, 
                              "Resource Name", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "StrucType", "LONG", "", "", "", 
                              "Structure Type", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "BldType", "TEXT", "", "", 3, 
                              "Building Type", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "StyleType", "TEXT", "", "", 3, 
                              "Architectural Style", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "Eligibility", "TEXT", "", "", 3, 
                              "Eligibility Status", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "ConstYr", "LONG", "", "", "", 
                              "Construction Year", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "Address", "TEXT", "", "", 200, "Address", 
                              "NULLABLE", req,"")
    arcpy.AddField_management(fc, "Notes", "TEXT", "", "", 200, "Notes", 
                              "NULLABLE", req,"")
    arcpy.AddGlobalIDs_management(fc)
    arcpy.AddField_management(fc, "EPProject", "TEXT", "", "", 20, 
                              "EPEI Project ID", "NULLABLE", req,"")
    arcpy.SetSubtypeField_management(fc,"StrucType")
    for item in subtypes.items():
        arcpy.AddSubtype_management(fc,item[0], item[1])
    arcpy.SetDefaultSubtype_management(fc,5)
    for item in subtypes.items():    
        arcpy.AssignDomainToField_management(fc, "BldType", item[1], item[0])
    subs = ['0', '1', '2', '3', '4', '6' ,'7' ,'8']
    arcpy.AssignDomainToField_management(fc, "StyleType", "Styles", subs)
    arcpy.AssignDomainToField_management(fc, "Eligibility", "Eligibility", subs)
    arcpy.AssignDefaultToField_management(fc,"Eligibility","U", subs)
    arcpy.AssignDefaultToField_management(fc,"StyleType","NS", subs)
    arcpy.AssignDefaultToField_management(fc,"BldType","OT", subs)
    arcpy.AssignDefaultToField_management(fc, "BldType", "NAT", '5')
    return os.path.join(gdb, fc)

def create_gap_format(gdb, geomtype, fc, crs):
    """
    Create custom format from original feature class template
    """    
    arcpy.env.workspace = gdb
    if crs.upper() == "EAST":
        #NAD_1983_StatePlane_Georgia_East_FIPS_1001_Feet WKID
        spatrefname = 2239
    elif crs.upper() == "WEST":
        #NAD_1983_StatePlane_Georgia_West_FIPS_1002_Feet WKID
        spatrefname = 2240
    spatref = arcpy.SpatialReference(spatrefname)
    if arcpy.Exists(fc):
        arcpy.Delete_management(fc)    
    has_m = "DISABLED"
    has_z = "DISABLED"
    req = "NON_REQUIRED"
    arcpy.CreateFeatureclass_management(gdb, fc, geomtype, "", 
                                        has_m, has_z, spatref)
    arcpy.AddField_management(fc, "ResourceID", "LONG", "", "", "", 
                              "Resource ID", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "PropName", "TEXT", "", "", 100, 
                              "Resource Name", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "Address", "TEXT", "", "", 200, "Address", 
                              "NULLABLE", req,"")
    arcpy.AddField_management(fc, "POINT_X", "DOUBLE", "", "", "", 
                              "Easting", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "POINT_Y", "DOUBLE", "", "", "", 
                              "Northing", "NULLABLE", req,"")
    arcpy.AddField_management(fc, "BldType", "TEXT", "", "", 50, 
                              "Building Type", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "StyleType", "TEXT", "", "", 50, 
                              "Architectural Style", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "Eligibility", "TEXT", "", "", 50, 
                              "Eligibility Status", "NON_NULLABLE", req,"")
    arcpy.AddField_management(fc, "Notes", "TEXT", "", "", 200, "Notes", 
                              "NULLABLE", req,"")
    return os.path.join(gdb, fc)

def append_to_gap_feature(inputfc, outputfc, sql):
    """
    Append features to custom fc
    """
    #Get spatial reference of output feature class to ensure cursor settings
    outcrs = arcpy.Describe(outputfc).spatialReference  
    flds = ["SHAPE@XY", "ResourceID", "PropName", "Address", "StrucType",
            "BldType", "StyleType", "Eligibility", "Notes", "EPProject"]
    #Fields not carried over to output
    exclude = ["StrucType", "EPProject"]
    insertflds = [fld for fld in flds if not fld in exclude]
    inputcursor = arcpy.da.SearchCursor(inputfc, flds, sql, outcrs)
    outputcursor = arcpy.da.InsertCursor(outputfc, insertflds)
    resindex = flds.index("ResourceID")
    projindex = flds.index("EPProject")
    #sort by project number and resource ID
    for row in sorted(inputcursor, key=itemgetter(projindex, resindex)):
        shape = row[flds.index("SHAPE@XY")]
        resid = row[resindex]
        propname = row[flds.index("PropName")]
        address = row[flds.index("Address")]
        notes = row[flds.index("Notes")]
        #get domain codes from input layer (index by name, in case flds changes)
        structcode = row[flds.index("StrucType")]
        bldgcode = row[flds.index("BldType")]
        stylecode = row[flds.index("StyleType")]
        eligcode = row[flds.index("Eligibility")]
        #translate domain codes to descriptions
        bldg = get_dom_desc(inputfc, "BldType", structcode, bldgcode)
        style = get_dom_desc(inputfc, "StyleType", structcode, stylecode)
        eligibility = get_dom_desc(inputfc, "Eligibility", structcode, eligcode)
        #build insert row, order is important
        toinsert = (shape, resid, propname, address, 
                    bldg, style, eligibility, notes)
        outputcursor.insertRow(toinsert)
    del outputcursor
    del inputcursor

def get_dom_desc(fc, field_name, subtype_code, codedvalue):
    """
    Get domain description for a given subtype code
    """
    subtypes = arcpy.da.ListSubtypes(fc)
    for stcode, stdict in subtypes.items():
        if stcode == subtype_code:        
            for stkey in stdict.iterkeys():
                if stkey == "FieldValues":
                    fields = stdict[stkey]
                    for field, fieldvalues in fields.iteritems():
                        if field == field_name:
                            domcodes = fieldvalues[1].codedValues
                            result = domcodes[codedvalue]
    return result

def sort_by_easting(fc, fld, sql):
    """
    Assign resource id based on easting
    
    params:
    fc - feature class
    fld - fld to sort
    """    
    flds = [fld, "SHAPE@X"]
    rows = arcpy.da.SearchCursor(fc, flds. sql)
    #sort cursor
    sort = sorted(rows, key=itemgetter(1))
    #create incremental ids (fld) on sorted cursor
    dsort = [(x, i[1]) for x, i in enumerate(sort, 1)]
    ws = os.path.dirname(fc)
    #update fld with new id
    with arcpy.da.Editor(ws) as edit:
        update = arcpy.da.UpdateCursor(fc, flds)
        for row in update:
            for item in dsort:
                if row[1] == item[1]:
                    row[0] = item[0]
                    update.updateRow(row)
                    
if __name__ == "__main__":
    pass
