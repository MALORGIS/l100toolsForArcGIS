# -*- coding: UTF-8 -*-

import arcpy
import subprocess

import os
import tempfile
import shutil

import locale

class _tempSqlite(object):
  
  def __init__(self, sqliteExe):
    self.temp_dir = None
    self.sqliteFile = None
    self.sqlFile = None
    self.exception = None
    
    if (not sqliteExe):
      dirNaem = os.path.dirname(os.path.abspath(__file__))
      sqliteExe = os.path.join(dirNaem, 'mod_spatialite-4.3.0a-win-amd64/sqlite3.exe')
    
    self.sqliteExe = sqliteExe

  def __enter__(self):
    # 一時ディレクトリを作成
    self.temp_dir = tempfile.mkdtemp()

    self.sqliteFile = os.path.join(self.temp_dir, 'calc.sqlite')
    self.sqlFile = os.path.join(self.temp_dir, 'exec.sql')

    arcpy.CreateSQLiteDatabase_management(self.sqliteFile, 'SPATIALITE')
    # with instance
    return self

  def __exit__(self, exc_type, exc_value, traceback):

    try:
      arcpy.Delete_management(self.sqliteFile)
      # 一時ディレクトリを削除
      shutil.rmtree(self.temp_dir)
      print("exit")
    
    except Exception as e:
      self.exception = e
    

  def excuteSql(self):
    cmdLine = '"' + self.sqliteExe + '" "' + self.sqliteFile + '" < "' + self.sqlFile + '"'
    #print(cmdLine)
    #print(type(cmdLine)) #cmdLine.decode('utf-8').encode(locale.getpreferredencoding(False))
    #print(locale.getpreferredencoding(False))
    #sqlite3
    p = subprocess.Popen(cmdLine ,#cmdLine.encode("SJIS"),
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)

    stdout_data, stderr_data = p.communicate()
    return { 'process':p, 'stdout':stdout_data, 'stderr':stderr_data}
