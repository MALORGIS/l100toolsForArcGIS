# -*- coding: UTF-8 -*-

#import sys,os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/tools')

import tools._SetupGetText

from tools.AddAreaField import AddAreaField
from tools.AddExtentField import AddExtentField
from tools.AddGeometryHashField import AddGeometryHashField
from tools.AddLengthField import AddLengthField
from tools.AddPointCountField import AddPointCountField
from tools.AddXYField import AddXYField
from tools.Erase import Erase
from tools.ExtractFeatureAttachments import ExtractFeatureAttachments
from tools.FeatureToWKTCSV import FeatureToWKTCSV
from tools.FeatureVerticesToPoints import FeatureVerticesToPoints
from tools.FillDoughnut import FillDoughnut
from tools.MinimumBoundingGeometry import MinimumBoundingGeometry
from tools.PointToPolygon import PointToPolygon
from tools.PointToPolyline import PointToPolyline
from tools.PolygonToPoint import PolygonToPoint
from tools.PolygonToPolyline import PolygonToPolyline
from tools.PolylineToCrossPoint import PolylineToCrossPoint
from tools.PolylineToPolygon import PolylineToPolygon
from tools.RandomPoints import RandomPoints
from tools.RasterCellValueToPoint import RasterCellValueToPoint
from tools.ShiftFeature import ShiftFeature
from tools.SpatiliteDelaunayTriangulation import SpatiliteDelaunayTriangulation
from tools.SpatiliteHexagonalGrid import SpatiliteHexagonalGrid
from tools.SpatiliteNear import SpatiliteNear
from tools.SpatiliteVoronojDiagram import SpatiliteVoronojDiagram
from tools.SpiderDiagrams import SpiderDiagrams
from tools.TableLayerToJSON import TableLayerToJSON
from tools.TableToCircle import TableToCircle
from tools.TableToRectangle import TableToRectangle


class Toolbox(object):
  #コンストラクタ : ツールボックスの名称ツールの設定
  def __init__(self):
    self.label = "100 Line Tools"
    self.alias = "l100tools"

    #TO:ツール増加時は配列に加える。
    self.tools = [ AddAreaField,AddExtentField,AddGeometryHashField,AddLengthField,AddPointCountField,AddXYField,Erase,ExtractFeatureAttachments,FeatureToWKTCSV,FeatureVerticesToPoints,FillDoughnut,MinimumBoundingGeometry,PointToPolygon,PointToPolyline,PolygonToPoint,PolygonToPolyline,PolylineToCrossPoint,PolylineToPolygon,RandomPoints,RasterCellValueToPoint,ShiftFeature,SpatiliteDelaunayTriangulation,SpatiliteHexagonalGrid,SpatiliteNear,SpatiliteVoronojDiagram,SpiderDiagrams,TableLayerToJSON,TableToCircle,TableToRectangle ]