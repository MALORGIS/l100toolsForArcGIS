# -*- coding: UTF-8 -*-

import arcpy

import sys
import codecs

#ツール定義
class SetFieldAliasFromTable(object):

  def __init__(self):
    self.label = _("Set Field Alias from Table")
    self.description = _("Set field alias from table.")

    self.category = _("DataManagement")
    self.canRunInBackground = False

  def getParameterInfo(self):

    param0 = arcpy.Parameter(
               displayName=_("Input Table"),
               name="in_table",
               datatype="GPTableView",
               parameterType="Required",
               direction="Input")

    param1 = arcpy.Parameter(
        displayName="Output Table",
        name="out_table",
        datatype="GPTableView",
        parameterType="Derived",
        direction="Output")

    param1.parameterDependencies = [param0.name]
    param1.schema.clone = True

    param2 = arcpy.Parameter(
               displayName=_("FieldInfo Table"),
               name="fieldInfoTable",
               datatype="GPTableView",
               parameterType="Required",
               direction="Input")

    param3 = arcpy.Parameter(
        displayName=_("FieldNameField"),
        name="fieldNameField",
        datatype="Field",
        parameterType="Required",
        direction="Input")

    param3.filter.list = ['Text']
    param3.parameterDependencies = [param2.name]

    param4 = arcpy.Parameter(
        displayName=_("FieldAliasField"),
        name="fieldAliasField",
        datatype="Field",
        parameterType="Required",
        direction="Input")

    param4.filter.list = ['Text']
    param4.parameterDependencies = [param2.name]
    
    params = [param0, param1, param2, param3, param4]
    return params

  
  def isLicensed(self):        
    return True

  def updateParameters(self, parameters):
    return
  
  def updateMessages(self, parameters):
    return
  
  def execute(self, parameters, messages):
    inTable = parameters[0].valueAsText
    nameAliasTable = parameters[2].valueAsText
    nameFiled = parameters[3].valueAsText
    aliasFiled = parameters[4].valueAsText
   
    fields = arcpy.ListFields(inTable)

    #enc = sys.stdin.encoding
#    messages.addMessage(enc)

    fieldDict = {}

    with arcpy.da.SearchCursor(nameAliasTable, [nameFiled,aliasFiled]) as cursor:
      for row in cursor:
        fieldDict[row[0]]=row[1]
        
    for field in fields:
      if field.name in fieldDict:
        arcpy.AlterField_management(inTable, field.name, new_field_alias=fieldDict[field.name])
        
