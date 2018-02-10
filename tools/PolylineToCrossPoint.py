# -*- coding: UTF-8 -*-

import arcpy

import os

#ツール定義
class PolylineToCrossPoint(object):

  def __init__(self):
    self.label = _("Polyline To CrossPoint")
    self.description = _("Creates a Point feature class from specified Polyline features.All cross Features are used and clear Selection.")

    self.category = _("TransformationShapes")
    self.canRunInBackground = False

  def getParameterInfo(self):

    param0 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="in_features",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param0.filter.list = ["Polyline"]

    param1 = arcpy.Parameter(
               displayName=_("Input Cross Features"),
               name="in_cross features",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param1.filter.list = ["Polyline"]

    param2 = arcpy.Parameter(
        displayName=_("Output Features"),
        name="out_features",
        datatype="DEFeatureClass",
        parameterType="Required",
        #parameterType="Derived",
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
    crossFeatures = parameters[1].valueAsText
    outFeatures = parameters[2].valueAsText

    inDesc = arcpy.Describe(inFeatures)
    if (inDesc.dataType == "FeatureLayer"):
      inDesc = inDesc.featureClass
      
    
    dirName, fcName = os.path.split(outFeatures)

    #create output
    arcpy.CreateFeatureclass_management(dirName, fcName, "POINT", None, "DISABLED", "DISABLED", inDesc.spatialReference)

    arcpy.AddField_management(outFeatures, "ref_ID", "LONG", 9, "", "", "refcode", "NULLABLE", "REQUIRED")
    arcpy.AddField_management(outFeatures, "cross_ID", "LONG", 9, "", "", "refcode", "NULLABLE", "REQUIRED")
    #tempName = inFeatures

    with arcpy.da.InsertCursor(outFeatures, ["ref_ID", "cross_ID", "SHAPE@"]) as inCursor:
      with arcpy.da.SearchCursor(inFeatures, ["OID@","SHAPE@"]) as cursor:
        for row in cursor:
          arcpy.SelectLayerByLocation_management(crossFeatures, 'intersect', row[-1])
          with arcpy.da.SearchCursor(crossFeatures, ["OID@","SHAPE@"]) as crosscursor:
            for crossrow in crosscursor:
              #1 —A zero-dimensional geometry (point or multipoint).
              pt = row[-1].intersect( crossrow[-1], 1 )
              if (isinstance(pt, arcpy.Multipoint)):
                for p in pt:
                  insPnt = arcpy.Point(p.X, p.Y)
                  inCursor.insertRow( (row[0], crossrow[0], arcpy.PointGeometry(insPnt),) )
              else:
                inCursor.insertRow( (row[0], crossrow[0], pt,) )
              
          arcpy.SelectLayerByAttribute_management(crossFeatures, "CLEAR_SELECTION")
