# -*- coding: UTF-8 -*-

import arcpy

import os

class SpiderDiagrams(object):

  def __init__(self):
    self.label = "Spider Diagrams"
    self.description = "Creates a SpiderDiagrams Polyline feature class from specified point features."

    self.category = "TransformationShapes"
    self.canRunInBackground = False

  def getParameterInfo(self):

    param0 = arcpy.Parameter(
               displayName="To Features",
               name="in_layer",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param0.filter.list = ["Point"]#, "Multipoint"]

    param1 = arcpy.Parameter(
        displayName="IDField",
        name="idfield",
        datatype="Field",
        parameterType="Required",
        direction="Input")

    param1.filter.list = ['Short', 'Long', 'Text', 'OID']
    param1.parameterDependencies = [param0.name]

    param2 = arcpy.Parameter(
               displayName="From Features",
               name="from_layer",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param2.filter.list = ["Point"]

    param3 = arcpy.Parameter(
        displayName="LinkField",
        name="linkfield",
        datatype="Field",
        parameterType="Optional",
        direction="Input")

    param3.filter.list = ['Short', 'Long', 'Text', 'OID']
    param3.parameterDependencies = [param2.name]

    param4 = arcpy.Parameter(
        displayName="Output Features",
        name="out_features",
        datatype="DEFeatureClass",
        parameterType="Required",
        #parameterType="Derived",
        direction="Output")

    params = [param0, param1, param2, param3, param4]
    return params

  
  def isLicensed(self):        
    return True

  def updateParameters(self, parameters):
    return
  
  def updateMessages(self, parameters):
    return
  
  def execute(self, parameters, messages):

    toFeatures = parameters[0].valueAsText
    fromFeatures = parameters[2].valueAsText
    
    idField = parameters[1].valueAsText
    linkField = parameters[3].valueAsText
    
    outFeatures = parameters[4].valueAsText

    inDesc = arcpy.Describe(toFeatures)
    if (inDesc.dataType == "FeatureLayer"):
      inDesc = inDesc.featureClass
      
    dirName, fcName = os.path.split(outFeatures)

    #create output
    arcpy.CreateFeatureclass_management(dirName, fcName, "POLYLINE", toFeatures, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", inDesc.spatialReference)

    fields = arcpy.ListFields(fromFeatures)
    lfield = None
    for field in fields:
      if (field.name == linkField):
        lfield = field

    fields = arcpy.ListFields(toFeatures)
    fieldList = []

    idFieldIndex = 0
    tmpIndex = 0
    for field in fields:
      if (field.name == idField):
        idFieldIndex = tmpIndex
      tmpIndex += 1
      
      if (field.type != "OID" or field.type != "Geometry" ):
        fieldList.append(field.name)
    fieldList.append("SHAPE@")
    
    with arcpy.da.InsertCursor(outFeatures,fieldList) as inCursor:
      with arcpy.da.SearchCursor(toFeatures, fieldList) as toCursor:
        for row in toCursor:

          if (not isinstance(row[-1] , arcpy.PointGeometry)):
            continue

          where = linkField + " = '" + str(row[idFieldIndex]) + "'"
          if (lfield.type != 'String'):
            where = linkField + " = " + str(row[idFieldIndex])
          #messages.addMessage(where)
          
          with arcpy.da.SearchCursor(fromFeatures, [linkField, "SHAPE@"], where, inDesc.spatialReference) as fromCursor:
            for fromRow in fromCursor:
              if (isinstance(fromRow[-1] , arcpy.PointGeometry)):
                insertRow = row[:-1] + (arcpy.Polyline(arcpy.Array([fromRow[-1].centroid, row[-1].centroid])),)
                inCursor.insertRow(insertRow)



