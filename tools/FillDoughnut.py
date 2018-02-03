# -*- coding: UTF-8 -*-

import arcpy
import os

class FillDoughnut(object):

  def __init__(self):

    self.label = _("Fill Doughnut")
    self.description = _("Create a polygon that fills the hole of the donut polygon.")

    self.category = _("TransformationShapes")
    self.canRunInBackground = False

  def getParameterInfo(self):
    param0 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="in_features",
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
  #ライセンスが存在するか(このツールに必要なライセンス)
  def isLicensed(self):        
    return True
  #パラメータ更新時の挙動記述
  def updateParameters(self, parameters):
    return
  #メッセージ更新時の挙動記述
  def updateMessages(self, parameters):
    return
  #実行実体処理
  def execute(self, parameters, messages):
    inFeatures = parameters[0].valueAsText
    outFeatures = parameters[1].valueAsText

    dirName, fcName = os.path.split(outFeatures)
    inDesc = arcpy.Describe(inFeatures)

    #messages.addMessage(inDesc.dataType)
    if (inDesc.dataType == "FeatureLayer"):
      inDesc = inDesc.featureClass

    arcpy.CreateFeatureclass_management(dirName, fcName, "POLYGON", inFeatures, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", inDesc.spatialReference)
    
    fields = arcpy.ListFields(outFeatures)
    #fieldList = ["SHAPE@"]
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
          lst = []
          # inner polygon is not part..
          for part in row[-1]:
            # trick getPart is not hole split
            lst.append(arcpy.Polygon(part).getPart(0))
          
          insertRow = row[:-1] + (arcpy.Polygon(arcpy.Array(lst)),)
          inCursor.insertRow(insertRow)

