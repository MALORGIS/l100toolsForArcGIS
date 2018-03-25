# -*- coding: UTF-8 -*-

import arcpy
import sqlite3

import os
import sys
import shutil

from contextlib import closing

from tools._tempSqlite import _tempSqlite

#ツール定義
class SpatiliteVoronojDiagram(object):

  def __init__(self):
    self.label = _("Point To Voronoi Diagram")
    self.description = _("Creates a Voronoi polygon feature class from specified point features.")

    self.category = _("SpatiaLite")
    self.canRunInBackground = False

  def getParameterInfo(self):

    param0 = arcpy.Parameter(
               displayName=_("Input Features"),
               name="in_layer",
               datatype="GPFeatureLayer",
               parameterType="Required",
               direction="Input")

    param0.filter.list = ["Point"]#, "Multipoint"]

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
    outName = r'pointfc'
    outDirName, outFcName = os.path.split(outFeatures)

    pydir = os.path.dirname(os.path.abspath(__file__))
    sqliteExe = os.path.join(pydir, 'mod_spatialite-4.3.0a-win-amd64/sqlite3.exe')
    if (not os.path.exists(sqliteExe)):
      messages.addErrorMessage('need mod_spatalite. see _download_mod_spatilite.ps1 and download it.')
      return
      
    
    with _tempSqlite(None) as tmpLite:
      print(tmpLite.temp_dir)
      
      arcpy.env.workspace = tmpLite.sqliteFile
      arcpy.CopyFeatures_management(inFeatures, outName)
    
      # ArcGIS does not have a unlock function. I cannot be unlock sqlite.
      shutil.copyfile(tmpLite.sqliteFile, os.path.join(tmpLite.temp_dir, 'calc2.sqlite'))
      arcpy.Delete_management(tmpLite.sqliteFile)
      tmpLite.sqliteFile = os.path.join(tmpLite.temp_dir, 'calc2.sqlite')
      
      fields = arcpy.ListFields(inFeatures)
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
          f.write("""
SELECT load_extension('mod_spatialite');
CREATE VIRTUAL TABLE ElementaryGeometries USING VirtualElementary();

CREATE TABLE test (id INTEGER PRIMARY KEY);
""")    
          # verson check 400x ? Desktop
          installDir = os.path.join(arcpy.GetInstallInfo()["InstallDir"], "bin")
          sys.path.append(installDir)
          conn.enable_load_extension(True)
    
          conn.execute("SELECT load_extension('spatialite400x');")
          
          for row in conn.execute("SELECT ST_SRID(shape) FROM pointfc limit 1;"):
            srid = row[0]
    
          f.write("SELECT AddGeometryColumn('test', 'geom', " + str(srid) + ",'MULTIPOLYGON', 'XY');")
          f.write("\r\n")
          f.write("INSERT INTO test SELECT 1, VoronojDiagram(GUnion(SHAPE)) geom FROM pointfc;")
          f.write("\r\n")
          
          isFirstTime = True
          f.write('CREATE TABLE joined(')
    
          print(shpFieldName)
    
          cols = []
          for row in conn.execute("PRAGMA table_info('pointfc');"):
            if (isFirstTime):
              isFirstTime = False
            elif (row[1].upper() != shpFieldName.upper()):
              f.write(",")
            #check attribute
            if (row[1].upper() == shpFieldName.upper()):
              continue
            elif (row[1].upper() == oidFieldName.upper()):
              f.write(row[1] + ' ' + row[2] + ' PRIMARY KEY')
            else:
              f.write(row[1] + ' ' + row[2])
              cols.append(row[1])
          
          f.write(');')
          f.write("\r\n")
          f.write("SELECT AddGeometryColumn('joined', 'geom', " + str(srid) + ", 'POLYGON', 'XY');")
          f.write("\r\n")
          f.write("INSERT INTO joined ")
          f.write("SELECT e.item_no, o." + ", o.".join(cols) + ", e.geometry geom ")
          f.write("FROM ")
          f.write(" ElementaryGeometries e ")
          f.write("LEFT OUTER JOIN ")
          f.write(" pointfc o ")
          f.write("ON ")
          f.write(" ST_Intersects(e.geometry, o.shape) = 1 ")
          f.write("WHERE ")
          f.write(" db_prefix = 'main' AND f_table_name = 'test' ")
          f.write(" AND f_geometry_column = 'geom' AND origin_rowid = 1;")
    
        conn.close()
    
      res = tmpLite.excuteSql() 
    
      p = res['process']
      stdout_data = res['stdout']
      stderr_data = res['stderr']
    
      if (p.returncode != 0):
        messages.addErrorMessage(stderr_data)
      
      #else:
      #  print(stdout_data)
      arcpy.FeatureClassToFeatureClass_conversion(in_features= os.path.join(tmpLite.sqliteFile ,"main.joined"), 
                                                out_path=outDirName, 
                                                out_name=outFcName)
