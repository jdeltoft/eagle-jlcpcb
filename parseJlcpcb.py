#!/usr/bin/env python3

from zipfile import ZipFile
import math
import re
import sys
import os
import argparse
import pandas as pd

filesToChoose = set()

if len(sys.argv) == 2:
    eagleFilename = sys.argv[1]
else:
  print("\n\nUSAGE: parseJlcpcb camfile.zip\n\n")
  sys.exit()

try:
  eagleZip = ZipFile(eagleFilename)
  eagleFiles = eagleZip.namelist()
  for f in eagleFiles:
    match = re.search("\\.csv$", f)
    if match:
      ##print(f'file: {f}')
      filesToChoose.add(f)
except Exception as e:
  print(f'\n\nFailed reading zip file. {e}\n\n')
  sys.exit()

def processCpl(cpl):
  df = pd.read_csv(cpl, header=None)

  df.insert(3, 'D', 'T')
  df = df.drop(df.columns[5], axis=1)
  df = df.drop(df.columns[5], axis=1)
  header_row = ['Designator','Mid X','Mid Y','Layer','Rotation']
  df = df.set_axis(header_row, axis=1)

  df.to_excel('processedCpl.xlsx', index=False)

def processBom(bom):
  df = pd.read_csv(bom, header=None)

  values_col = df.pop(df.columns[1])
  designator_col = df.pop(df.columns[3])
  footprint_col = df.pop(df.columns[2])

  df.insert(0, 'Value', values_col)
  df.insert(1, 'Designator', designator_col)
  df.insert(2, 'Footprint', footprint_col)
  df.insert(3, 'JLCPCB Part #（optional', '')

  for i in range(31):
    df = df.drop(df.columns[4], axis=1)

  # replace footprint for capacitors and resistors to 0603
  df['Footprint'] = df['Footprint'].replace(r'^RESC.*', '"0603"', regex=True)
  df['Footprint'] = df['Footprint'].replace(r'^CAPC.*', '"0603"', regex=True)

  df.to_excel('processedBom.xlsx', index=False)


for f in filesToChoose:
  ## could add a cmd line option for doing the back board instead of front
  match = re.search("PnP.*front\\.csv$", f)
  if match:
    ## Must extract file from zip and then process
    cplFile = eagleZip.open(f)
    processCpl(cplFile)

  match = re.search("BOM.*\\.csv$", f)
  if match:
    ## Must extract file from zip and then process
    bomFile = eagleZip.open(f)
    processBom(bomFile)





