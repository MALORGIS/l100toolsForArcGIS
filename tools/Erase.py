# -*- coding: UTF-8 -*-
import arcpy
import os

#ツール定義
class Erase(object):
  def __init__(self):
    self.label = _("Erase")
    self.description = _("Creates a feature class by overlaying the Input Features with the polygons of the Erase Features. Only those portions of the input features falling outside the erase features outside boundaries are copied to the output feature class.")

    self.category = _("TransformationShapes")
    self.canRunInBackground = False

  def getParameterInfo(self):
    param0 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="in_features",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param1 = arcpy.Parameter(
               displayName=_("Erase Features"),
               name="erase_features",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param2 = arcpy.Parameter(
        displayName=_("Output Features"),
        name="out_features",
        datatype="DEFeatureClass",
        parameterType="Required",
        direction="Output")

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
    eraseFeatures = parameters[1].valueAsText
    outFeatures = parameters[2].valueAsText

    #inDesc = arcpy.Describe(inFeatures)
    #if (inDesc.dataType == "FeatureLayer"):
    #  inDesc = inDesc.featureClass
      
    #dirName, fcName = os.path.split(outFeatures)
    dirName, fcName = os.path.split(outFeatures)
    
    #create output
    #arcpy.CreateFeatureclass_management(dirName, fcName, inDesc.shapeType.upper(), inFeatures, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", inDesc.spatialReference)
    arcpy.CopyFeatures_management(inFeatures, outFeatures)

    arcpy.MakeFeatureLayer_management(outFeatures, fcName)


    with arcpy.da.SearchCursor(eraseFeatures, "SHAPE@") as cursor:
      for row in cursor:
        arcpy.SelectLayerByLocation_management(fcName, 'intersect', row[0])
        with arcpy.da.UpdateCursor(fcName, "SHAPE@") as upcursor:
          for uprow in upcursor:
            uprow[0] = uprow[0].difference(row[0])
            upcursor.updateRow(uprow)

      arcpy.SelectLayerByAttribute_management(fcName, "CLEAR_SELECTION")

      

    
