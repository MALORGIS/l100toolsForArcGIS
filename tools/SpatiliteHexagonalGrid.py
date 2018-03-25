# -*- coding: UTF-8 -*-

import arcpy
import sqlite3

import os
import sys
import shutil

from contextlib import closing

from tools._tempSqlite import _tempSqlite

#ツール定義
class SpatiliteHexagonalGrid(object):

  def __init__(self):
    self.label = _("Hexgonal Grid")
    self.description = _("Creates a hexagonal grid polygon feature class from the specified feature layer extent.")

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
               displayName=_("Hexagonal Grid Size"),
               name="size",
               datatype="GPDouble",
               parameterType="Required",
               direction="Input")

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
    size = parameters[1].valueAsText
    outFeatures = parameters[2].valueAsText
    
    outDirName, outFcName = os.path.split(outFeatures)


    inDesc = arcpy.Describe(inFeatures)
    
    sr = inDesc.spatialReference
    ext = inDesc.extent

    wktExtent = "POLYGON (({} {}, {} {}, {} {}, {} {}, {} {}))".format( ext.XMin, ext.YMin,
                     ext.XMin, ext.YMax,
                     ext.XMax, ext.YMax,
                     ext.XMax, ext.YMin, ext.XMin, ext.YMin)

    pydir = os.path.dirname(os.path.abspath(__file__))
    sqliteExe = os.path.join(pydir, 'mod_spatialite-4.3.0a-win-amd64/sqlite3.exe')
    if (not os.path.exists(sqliteExe)):
      messages.addErrorMessage('need mod_spatalite. see _download_mod_spatilite.ps1 and download it.')
      return


    with _tempSqlite(None) as tmpLite:
      print(tmpLite.temp_dir)
      
      with open(tmpLite.sqlFile,'w') as f:    
        # verson check 400x ? Desktop
        installDir = os.path.join(arcpy.GetInstallInfo()["InstallDir"], "bin")
        sys.path.append(installDir)

        f.write("""
SELECT load_extension('mod_spatialite');
CREATE VIRTUAL TABLE ElementaryGeometries USING VirtualElementary();

CREATE TABLE tmp_hgrid (id INTEGER PRIMARY KEY);
SELECT AddGeometryColumn('tmp_hgrid', 'geom', 0, 'MULTIPOLYGON', 'XY');

INSERT INTO tmp_hgrid
SELECT
  1,
  ST_HexagonalGrid(  
   ST_GeomFromText('""" + wktExtent + """'), """ + size + """);

CREATE TABLE hgrid (id INTEGER PRIMARY KEY);
SELECT AddGeometryColumn('hgrid', 'geom', 0, 'POLYGON', 'XY');

INSERT INTO hgrid 
SELECT
  e.item_no,
  e.geometry
FROM
 ElementaryGeometries e 
WHERE
 e.db_prefix = 'main' AND 
 e.f_table_name = 'tmp_hgrid' AND
 e.f_geometry_column = 'geom' AND
 e.origin_rowid = 1
;
""")
      
      res = tmpLite.excuteSql() 
      
      p = res['process']
      stdout_data = res['stdout']
      stderr_data = res['stderr']
    
      if (p.returncode != 0):
        print(stderr_data)
      
      arcpy.FeatureClassToFeatureClass_conversion(in_features= os.path.join(tmpLite.sqliteFile ,"main.hgrid"), 
                                                out_path=outDirName, 
                                                out_name=outFcName)

      arcpy.DefineProjection_management(outFeatures, sr)
    
