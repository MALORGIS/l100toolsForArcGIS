# -*- coding: UTF-8 -*-

import arcpy
import os

#ツール定義
class PolygonToPolyline(object):

  def __init__(self):
    self.label = _("Polygon To Polyline")
    self.description = _("Creates a Polyline feature class from specified Polygon features.")

    self.category = _("TransformationShapes")
    self.canRunInBackground = False

  def getParameterInfo(self):
    param0 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="in_layer",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param0.filter.list = ["Polygon"]

    param1 = arcpy.Parameter(
        displayName=_("Output Features"),
        name="out_features",
        datatype="DEFeatureClass",
        parameterType="Required",
        #parameterType="Derived",
        direction="Output")

    params = [param0, param1]
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

    inDesc = arcpy.Describe(inFeatures)
    if (inDesc.dataType == "FeatureLayer"):
      inDesc = inDesc.featureClass
      

    dirName, fcName = os.path.split(outFeatures)

    #create output
    arcpy.CreateFeatureclass_management(dirName, fcName, "POLYLINE", inFeatures, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", inDesc.spatialReference)

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
            insertRow = row[:-1] + (row[-1].boundary (),)
            inCursor.insertRow( insertRow )
          #step count
          arcpy.SetProgressorPosition()
