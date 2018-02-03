

$names = [System.Collections.Generic.List[String]]::new()

Get-ChildItem -Include *.py -Exclude _*.py,test.py -Recurse | ForEach-Object {
  $names.Add( [IO.Path]::GetFileNameWithoutExtension($_) )
}

$sb = [System.Text.StringBuilder]::new()
ForEach( $name in $names) {
  $sb.AppendLine([String]::Format("from {0} import {0}", $name))
}

[System.IO.File]::WriteAllText("l100tools.pyt", 
[String]::Format(@"
# -*- coding: UTF-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/tools')

import _SetupGetText

{0}

class Toolbox(object):
  #コンストラクタ : ツールボックスの名称ツールの設定
  def __init__(self):
    self.label = "l100tools"
    self.alias = "100 Line Tools"

    #TO:ツール増加時は配列に加える。
    self.tools = [ {1} ]
"@, $sb.ToString(), [String]::Join(",", $names.ToArray())), [System.Text.Encoding]::UTF8);
