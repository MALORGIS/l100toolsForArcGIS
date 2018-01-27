# -*- coding: UTF-8 -*-

import arcpy
import os

#フィーチャの頂点 → ポイント
class FeatureVerticesToPoints(object):

  def __init__(self):

    self.label = "Feature Vertices To Points"
    self.description = "Creates a feature class containing points generated from specified vertices or locations of the input features."

    self.category = "TransformationShapes"
    self.canRunInBackground = False

  def getParameterInfo(self):
    param0 = arcpy.Parameter(
               displayName="Input Features",
               name="in_layer",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param0.filter.list = ["Polyline", "Polygon"]
    
    param1 = arcpy.Parameter(
        displayName="Output Features",
        name="out_features",
        datatype="DEFeatureClass",
        parameterType="Required",
        #parameterType="Derived",
        direction="Output")

    #param1.parameterDependencies = [param0.name]
    #param1.schema.clone = True

    param2 = arcpy.Parameter(
        displayName="Input value",
        name="in_value",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

    param2.filter.type = "ValueList"
    param2.filter.list = ["ALL",
                          "MID",
                          "START",
                          "END",
                          "BOTH_ENDS"]
    param2.value = "ALL"
    
    params = [param0, param1, param2]

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
    verticesType = parameters[2].valueAsText
    
    #messages.addMessage(verticesType)
    #messages.addMessage(outFeatures)

    dirName, fcName = os.path.split(outFeatures)
    inDesc = arcpy.Describe(inFeatures)

    #messages.addMessage(inDesc.dataType)
    if (inDesc.dataType == "FeatureLayer"):
      inDesc = inDesc.featureClass

    arcpy.CreateFeatureclass_management(dirName, fcName, "POINT", inFeatures, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", inDesc.spatialReference)
    
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
          for part in row[-1]:
            if (verticesType=="START" or verticesType=="BOTH_ENDS"):
              # = arcpy.Polyline(arcpy.Array(part)).firstPoint
              insertRow = row[:-1] + (part[0],)             
              inCursor.insertRow(insertRow)
              #messages.addMessage("始点")
            if (verticesType=="END" or verticesType=="BOTH_ENDS"):
              #insertRow[0] = arcpy.Polyline(arcpy.Array(part)).lastPoint
              insertRow = row[:-1] + (part[ len(part) - 1],)
              inCursor.insertRow(insertRow)
              #messages.addMessage("終点")
            if (verticesType=="MID"):
              insertRow = row[:-1] + (arcpy.Polyline(arcpy.Array(part)).positionAlongLine(0.5, True),)
              inCursor.insertRow(insertRow)
              #messages.addMessage("中間点")
            if (verticesType=="ALL"):
              #messages.addMessage("全部")
              for pnt in part:
                insertRow = row[:-1] + (pnt,)
                #messages.addMessage( str(pnt.X) + " " + str(pnt.Y) )
                
                inCursor.insertRow( insertRow )
          # step count
          arcpy.SetProgressorPosition()
