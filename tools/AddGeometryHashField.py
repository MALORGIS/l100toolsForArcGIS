# -*- coding: UTF-8 -*-
import arcpy
import os
import hashlib

class AddGeometryHashField(object):
  def __init__(self):
    self.label = _("Add Geometry Hash Field")
    self.description = _("Adds a WKB SHA256 Hash field to a feature layer.")

    self.category = _("Fields")
    self.canRunInBackground = False

  def getParameterInfo(self):
    param0 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="in_features",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")
    param0.filter.list = ["Point","Multipoint","Polyline","Polygon"]


    param1 = arcpy.Parameter(
        displayName=_("Output Features"),
        name="out_features",
        datatype="GPFeatureLayer",
        parameterType="Derived",
        direction="Output")

    params = [param0, param1]
    return params

  def isLicensed(self):
    return True

  def updateParameters(self, parameters):
     
    
    return
  
  def updateMessages(self, parameters):
    inFeatures = parameters[0].valueAsText
    if (inFeatures):
      inDesc = arcpy.Describe(inFeatures)
      if (inDesc.dataType == "FeatureLayer"):
        inDesc = inDesc.featureClass
      # message clear ( check fieldname )
      parameters[0].clearMessage()
      fields = arcpy.ListFields(inFeatures)
      for field in fields:
        if (field.name.upper() == "HASH"):
          parameters[0].setWarningMessage(_("The value of the [HASH] field will be overwritten."))
          break

    
    return
  
  def execute(self, parameters, messages):
    
    inFeatures = parameters[0].valueAsText

    fields = arcpy.ListFields(inFeatures)
    fieldList = []
    
    for field in fields:     
      fieldList.append(field.name)

    if (not "HASH" in fieldList):
      arcpy.AddField_management(inFeatures, "HASH", "TEXT", field_length=65)

    with arcpy.da.UpdateCursor(inFeatures, ["SHAPE@WKB", "HASH"]) as cursor:
      for row in cursor:
        row[1] = hashlib.sha256(row[0]).hexdigest()
        cursor.updateRow(row) 

