# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 21:53:58 2022

@author: Sebastian
"""

import requests
import io
import pandas as pd
import numpy as np

# create useable dataframe from googlesheets
file1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTpz57xEbxfHuOaBl99AW58UduL3dAs8GcaKJXDyUcbKbJO30ZmX-iHCHOppoZyRqY1-4zCI8WhGEnk/pub?gid=0&single=true&output=csv'
file2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR2scw5v8zB1aw7zYr_r_w2z63SCgzpk2SC6FVfySdi6Ix6gFw41eTDV8hiN9_Yym2R9GFw0SPZrMus/pub?gid=0&single=true&output=csv'
file3 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRu9WsztNS1xpS8JtTN6QOxGdZaWk8E0kCFOjVx_NB0VSDw38_Isf1B9maA7NW03ysUOjaLwV8JkXa7/pub?gid=0&single=true&output=csv'

response1 = requests.get(file1)
assert response1.status_code == 200, 'Wrong status code'
print(response1.content)

df_file1 =  pd.read_csv(io.StringIO(response1.content.decode('utf-8')))

response2 = requests.get(file2)
assert response2.status_code == 200, 'Wrong status code'
print(response2.content)

df_file2 =  pd.read_csv(io.StringIO(response2.content.decode('utf-8')))

response3 = requests.get(file3)
assert response3.status_code == 200, 'Wrong status code'
print(response3.content)

df_file3 =  pd.read_csv(io.StringIO(response3.content.decode('utf-8')))

del response1
del response2
del response3

# Prepping file 1 for combining
df_file1['Slug 1'] = df_file1['Slug 1'].fillna('')
df_file1['Slug 2'] = df_file1['Slug 2'].fillna('')
df_file1['Slug 3'] = df_file1['Slug 3'].fillna('')
df_file1['Slug 4'] = df_file1['Slug 4'].fillna('')
df_file1['Slug 5'] = df_file1['Slug 5'].fillna('')
df_file1['Slug'] = df_file1['Slug 1'] + df_file1['Slug 2'] + df_file1['Slug 3'] + df_file1['Slug 4'] + df_file1['Slug 5']

df_file1.drop(columns={'Slug 1','Slug 2','Slug 3','Slug 4','Slug 5',},inplace=True)

mapping_file1 = {'Attribution':'attribution',
                 'Ref_No':'reference',
                 'dup_lead':'f1_dup_lead',
                 'Bounty':'f1_bounty',
                 'New Date':'date',
                 'Widget Type':'f1_widget_type',
                 'Device':'device',
                 'Slug':'slug',
                 'PPC Channel':'ppc_channel'}

df_file1.rename(columns=mapping_file1, inplace=True)

# Prepping file 2 for combining
mapping_file2 = {'Attribution':'attribution',
                 'Reference':'reference',
                 'Call / Form':'f2_call_form',
                 'Submission Web Page':'slug',
                 'New Date':'date',
                 'Status':'f2_status',
                 'Status Reason':'f2_status_reason',
                 'Booked Sale (Y/N)':'f2_booked_sale',
                 'Date of Sale':'f2_date_of_sale',
                 'Explanations':'f2_explanations',
                 'Qualified?':'qualified',
                 'PPC Channel':'ppc_channel'}

df_file2.rename(columns=mapping_file2, inplace=True)

# Prepping file 3 for combining
df_file3['qualified'] = [1 if x == 'Y' else 0 for x in df_file3['Qualified']]

df_file3.drop(columns={'Qualified'}, inplace=True)

mapping_file3 = {'Attribution':'attribution',
                 'Date':'date',
                 'DateRecd':'f3_datetime',
                 'Channel':'f3_channel',
                 'LeadId':'f3_leadid',
                 'Brand':'f3_brand',
                 'Booked Date':'f3_booked_date',
                 'DeviceType':'device',
                 'VendorParms':'reference',
                 'Count':'f3_count',
                 'PPC Channel':'ppc_channel'}

df_file3.rename(columns=mapping_file3, inplace=True)


df = pd.concat([df_file1, df_file2], sort=False)
df_final = pd.concat([df, df_file3], sort=False)

df_final.to_csv('combined_files.csv')
