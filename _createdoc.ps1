$names = [System.Collections.Generic.List[String]]::new()

Get-ChildItem -Include *.py -Exclude _*.py,test.py -Recurse | ForEach-Object {
  $names.Add( [IO.Path]::GetFileNameWithoutExtension($_) )
}

$sb = [System.Text.StringBuilder]::new()
ForEach( $name in $names) {
  $sb.AppendLine([String]::Format("from {0} import {0}", $name))
}

[System.IO.File]::WriteAllText("_doc.py", 
[String]::Format(@"
# -*- coding: UTF-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/tools')

import _SetupGetText

{0}

tools = [{1}()]

tooldict = {{}}
for tool in tools:
  #print tool.label
  #print tool.category
  if tool.category not in tooldict:
    tooldict[tool.category] = []
  tooldict[tool.category].append(tool.label)

for cat in tooldict.keys():
  print((cat + "  ").decode('utf-8'))
  for tool in tooldict[cat]:
    print(("  -" + tool + "  ").decode('utf-8'))


"@, $sb.ToString(),[String]::Join("(),", $names.ToArray())), [System.Text.Encoding]::UTF8);