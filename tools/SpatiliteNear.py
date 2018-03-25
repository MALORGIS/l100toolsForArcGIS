# -*- coding: UTF-8 -*-

import arcpy
import sqlite3

import os
import sys
import shutil

from contextlib import closing

from tools._tempSqlite import _tempSqlite

#ツール定義
class SpatiliteNear(object):

  def __init__(self):
    self.label = _("Near Line(self/target)")
    self.description = _("Creates a polyline feature class from specified feature layer.")

    self.category = _("SpatiaLite")
    self.canRunInBackground = False

  def getParameterInfo(self):

    param0 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="src_features",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param0.filter.list = ["Point", "Multipoint", "Polyline", "Polygon"]

    param1 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="dst_features",
               datatype="GPFeatureLayer",
               parameterType="Optional",
               direction="Input")
    
    param1.filter.list = ["Point", "Multipoint", "Polyline", "Polygon"]

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
    srcFeatures = parameters[0].valueAsText
    dstFeatures = parameters[1].valueAsText
    outFeatures = parameters[2].valueAsText
    outName = r'srcfc'
    dstOutName = r'dstfc'
    outDirName, outFcName = os.path.split(outFeatures)

    pydir = os.path.dirname(os.path.abspath(__file__))
    sqliteExe = os.path.join(pydir, 'mod_spatialite-4.3.0a-win-amd64/sqlite3.exe')
    if (not os.path.exists(sqliteExe)):
      messages.addErrorMessage('need mod_spatalite. see _download_mod_spatilite.ps1 and download it.')
      return

    with _tempSqlite(None) as tmpLite:
      print(tmpLite.temp_dir)
      
      arcpy.env.workspace = tmpLite.sqliteFile
      arcpy.CopyFeatures_management(srcFeatures, outName)
      if (dstFeatures):
        arcpy.CopyFeatures_management(dstFeatures, dstOutName)
    
      # ArcGIS does not have a unlock function. I cannot be unlock sqlite.
      shutil.copyfile(tmpLite.sqliteFile, os.path.join(tmpLite.temp_dir, 'calc2.sqlite'))
      arcpy.Delete_management(tmpLite.sqliteFile)
      tmpLite.sqliteFile = os.path.join(tmpLite.temp_dir, 'calc2.sqlite')
      
      fields = arcpy.ListFields(srcFeatures)
      oidFieldName = None
      shpFieldName = None
      for field in fields:
        if (field.type == "OID"):
          oidFieldName = field.name
        elif (field.type == "Geometry" ):
          shpFieldName = field.name
    
      srid=0
      with closing(sqlite3.connect(tmpLite.sqliteFile)) as conn:
        with open(tmpLite.sqlFile,'w') as f:    
          # verson check 400x ? Desktop
          installDir = os.path.join(arcpy.GetInstallInfo()["InstallDir"], "bin")
          sys.path.append(installDir)
          conn.enable_load_extension(True)
    
          conn.execute("SELECT load_extension('spatialite400x');")

          for row in conn.execute("SELECT ST_SRID(shape) FROM srcfc limit 1;"): 
            srid = row[0]
            
          addWhere = ""
          if (dstFeatures):
            for row in conn.execute("SELECT ST_SRID(shape) FROM dstfc limit 1;"):
              if (srid != row[0]):
                message.addWarningMessage(_("FeatureClass has a different SRID."))
          else:
            addWhere = " AND s.OBJECTID <> d.OBJECTID "
            dstOutName = outName

          f.write("""
SELECT load_extension('mod_spatialite');

CREATE TABLE NearTable (
 OID INTEGER PRIMARY KEY,
 NEARID INTEGER,
 DISTANCE REAL
);

SELECT AddGeometryColumn('NearTable', 'shape', """ + str(srid) + """,'LINESTRING', 'XY');

INSERT INTO NearTable 
SELECT
 src.OBJECTID OID,
 dst.OBJECTID NEARID,
 ST_Distance(src.SHAPE, dst.SHAPE) DISTANCE,
 ST_ShortestLine(src.SHAPE, dst.SHAPE) SHAPE
FROM
 srcfc src
CROSS JOIN
 """ + dstOutName + """ dst
WHERE
 dst.OBJECTID = (SELECT s.OBJECTID
    FROM """ + dstOutName + """ AS s
    CROSS JOIN srcfc d
    WHERE src.OBJECTID = d.OBJECTID """ + addWhere + """ 
    ORDER BY ST_Distance(d.Shape, s.Shape)
    LIMIT 1
 )
;""")
    
        conn.close()
    
      res = tmpLite.excuteSql() 
      
      p = res['process']
      stdout_data = res['stdout']
      stderr_data = res['stderr']
    
      if (p.returncode != 0):
        print(stderr_data)
      #else:
      #  print(stdout_data)
      
      arcpy.FeatureClassToFeatureClass_conversion(in_features= os.path.join(tmpLite.sqliteFile ,"main.NearTable"), 
                                                out_path=outDirName, 
                                                out_name=outFcName)
    
