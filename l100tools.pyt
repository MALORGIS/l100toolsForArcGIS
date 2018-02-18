# -*- coding: UTF-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/tools')

import _SetupGetText

from AddAreaField import AddAreaField
from AddExtentField import AddExtentField
from AddGeometryHashField import AddGeometryHashField
from AddLengthField import AddLengthField
from AddPointCountField import AddPointCountField
from AddXYField import AddXYField
from Erase import Erase
from ExtractFeatureAttachments import ExtractFeatureAttachments
from FeatureVerticesToPoints import FeatureVerticesToPoints
from FillDoughnut import FillDoughnut
from MinimumBoundingGeometry import MinimumBoundingGeometry
from PointToPolygon import PointToPolygon
from PointToPolyline import PointToPolyline
from PolygonToPoint import PolygonToPoint
from PolygonToPolyline import PolygonToPolyline
from PolylineToCrossPoint import PolylineToCrossPoint
from PolylineToPolygon import PolylineToPolygon
from RandomPoints import RandomPoints
from RasterCellValueToPoint import RasterCellValueToPoint
from SpatiliteDelaunayTriangulation import SpatiliteDelaunayTriangulation
from SpatiliteNear import SpatiliteNear
from SpatiliteVoronojDiagram import SpatiliteVoronojDiagram
from SpiderDiagrams import SpiderDiagrams
from TableLayerToJSON import TableLayerToJSON


class Toolbox(object):
  #コンストラクタ : ツールボックスの名称ツールの設定
  def __init__(self):
    self.label = "100 Line Tools"
    self.alias = "l100tools"

    #TO:ツール増加時は配列に加える。
    self.tools = [ AddAreaField,AddExtentField,AddGeometryHashField,AddLengthField,AddPointCountField,AddXYField,Erase,ExtractFeatureAttachments,FeatureVerticesToPoints,FillDoughnut,MinimumBoundingGeometry,PointToPolygon,PointToPolyline,PolygonToPoint,PolygonToPolyline,PolylineToCrossPoint,PolylineToPolygon,RandomPoints,RasterCellValueToPoint,SpatiliteDelaunayTriangulation,SpatiliteNear,SpatiliteVoronojDiagram,SpiderDiagrams,TableLayerToJSON ]