# -*- coding: UTF-8 -*-

import arcpy

import os


class PolygonToPoint(object):

  def __init__(self):
    self.label = "Polygon To Point"
    self.description = "Creates a Point feature class from specified Polygon features."

    self.category = "TransformationShapes"
    self.canRunInBackground = False

  def getParameterInfo(self):
    param0 = arcpy.Parameter(
               displayName="Input Features",
               name="in_layer",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param0.filter.list = ["Polygon"]

    param1 = arcpy.Parameter(
        displayName="Output Features",
        name="out_features",
        datatype="DEFeatureClass",
        parameterType="Required",
        #parameterType="Derived",
        direction="Output")


    param2 = arcpy.Parameter(
        displayName="Input value",
        name="in_value",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

    param2.filter.type = "ValueList"
    param2.filter.list = ["TrueCentroid",
                          "LabelPoint",
                          "Centroid"]
    param2.value = "TrueCentroid"

    params = [param0, param1, param2]
    return params

  def isLicensed(self):
    return True

  def updateParameters(self, parameters):
    return
  
  def updateMessages(self, parameters):
    return
  
  def execute(self, parameters, messages):
    
    inFeatures = parameters[0].valueAsText
    outFeatures = parameters[1].valueAsText
    pointType = parameters[2].valueAsText

    inDesc = arcpy.Describe(inFeatures)
    if (inDesc.dataType == "FeatureLayer"):
      inDesc = inDesc.featureClass
      

    dirName, fcName = os.path.split(outFeatures)

    #create output
    arcpy.CreateFeatureclass_management(dirName, fcName, "POINT", inFeatures, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", inDesc.spatialReference)

    fields = arcpy.ListFields(outFeatures)
    fieldList = []
    
    for field in fields:
      #messages.addMessage("{0} is a type of {1} with a length of {2}"
      #   .format(field.name, field.type, field.length))
      if (field.type != "OID" or field.type != "Geometry" ):
        fieldList.append(field.name)
    fieldList.append("SHAPE@")

    # for Progress step count
    result = arcpy.GetCount_management(inFeatures)
    count = int(result.getOutput(0))
    arcpy.SetProgressor("step", "Inserting ...", 0, count, 1)

    with arcpy.da.InsertCursor(outFeatures, fieldList) as inCursor:
      with arcpy.da.SearchCursor(inFeatures, fieldList) as cursor:
        for row in cursor:
          if (isinstance(row[-1] , arcpy.Polygon)):
            if (pointType == "LabelPoint"):
              insertRow = row[:-1] + (row[-1].labelPoint ,)
            elif (pointType == "Centroid"):
              insertRow = row[:-1] + (row[-1].centroid ,)
            else:
              insertRow = row[:-1] + (row[-1].trueCentroid ,)
              
            inCursor.insertRow( insertRow )
          #step count
          arcpy.SetProgressorPosition()
