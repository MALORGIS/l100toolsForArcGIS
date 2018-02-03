# -*- coding: UTF-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/tools')

import _SetupGetText

from FeatureVerticesToPoints import FeatureVerticesToPoints
from PointToPolygon import PointToPolygon
from PointToPolyline import PointToPolyline
from PolylineToPolygon import PolylineToPolygon
from PolygonToPolyline import PolygonToPolyline
from PolygonToPoint import PolygonToPoint
from RandomPoints import RandomPoints
from SpiderDiagrams import SpiderDiagrams
from MinimumBoundingGeometry import MinimumBoundingGeometry


#横断線作成ツールボックス
# Python ツールボックスのツール動作のカスタマイズ
# see : http://resources.arcgis.com/ja/help/main/10.2/index.html#//00150000002m000000
class Toolbox(object):
  #コンストラクタ : ツールボックスの名称ツールの設定
  def __init__(self):
    self.label = "l100tools"
    self.alias = "100 Line Tools"

    #TO:ツール増加時は配列に加える。
    self.tools = [FeatureVerticesToPoints,
                  PointToPolygon,
                  PointToPolyline, 
                  PolygonToPolyline,
                  PolygonToPoint,
                  PolylineToPolygon,
                  RandomPoints,
                  SpiderDiagrams,
                  MinimumBoundingGeometry]

