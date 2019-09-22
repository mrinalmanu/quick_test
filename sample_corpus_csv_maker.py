#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 23:14:26 2019

@author: mrinalmanu
"""

import xml.etree.ElementTree as ET
import pandas as pd 
from pandas.io.json import json_normalize

tree = ET.parse('/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/bibles/Achuar-NT.xml')
root = tree.getroot()

    
    #_______________________
    


df_cols = ["verse_id", "verse_text"]
rows = []
    
for node in root.iter('seg'):
    verse_id = node.attrib
    verse_text = node.text
    rows.append({"verse_id": verse_id, "verse_text": verse_text})

df = pd.DataFrame(rows, columns = df_cols)
df2 = json_normalize(df['verse_id'])
df['verse_id'] = df2['id']
# splitting the id column for better retrieval of entries
df['book'], df['name'], df['chapter'], df['verse'] = df['verse_id'].str.split('.', 3).str

df.to_csv(r'/home/mrinalmanu/Documents/corpuses/bible-corpus-1.2.1/bibles/data_frame.csv')
