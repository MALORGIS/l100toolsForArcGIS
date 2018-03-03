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
from TableToRectangle import TableToRectangle


tools = [AddAreaField(),AddExtentField(),AddGeometryHashField(),AddLengthField(),AddPointCountField(),AddXYField(),Erase(),ExtractFeatureAttachments(),FeatureVerticesToPoints(),FillDoughnut(),MinimumBoundingGeometry(),PointToPolygon(),PointToPolyline(),PolygonToPoint(),PolygonToPolyline(),PolylineToCrossPoint(),PolylineToPolygon(),RandomPoints(),RasterCellValueToPoint(),SpatiliteDelaunayTriangulation(),SpatiliteNear(),SpatiliteVoronojDiagram(),SpiderDiagrams(),TableLayerToJSON(),TableToRectangle()]

tooldict = {}
for tool in tools:
  #print tool.label
  #print tool.category
  if tool.category not in tooldict:
    tooldict[tool.category] = []
  tooldict[tool.category].append(tool.label)

for cat in tooldict.keys():
  print cat
  for tool in tooldict[cat]:
    print "  -" + tool

