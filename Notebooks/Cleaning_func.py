import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import glob

def imp_and_apnd(folder):
    filenames =  glob.glob(f'{folder}/*.xml')
    record_list = []
    data2 = pd.DataFrame()
    count=0
    for filename in filenames:
        count +=1
        tree = ET.parse(filename)
        root = tree.getroot()
        record_list = [x.attrib for x in root.iter('Record')] 
        data = pd.DataFrame(record_list)
        data['Person']= count
        data2 = data2.append(data)
    data2.reset_index(inplace=True)

    return data2

def date_cleaning (data, col):
    data[col]= data[col].apply(lambda row: str(row).split('+')[0])
    data[col] = pd.to_datetime(data[col], format="%Y-%m-%d %H:%M:%S", utc=True) 
    return data

def date_2022 (data):
    data = data[data['creationDate'].dt.year == 2022]
    return data

def type_cleaning(data, col):
    data[col] = data[col].str.replace('HKQuantityTypeIdentifier', '')
    data[col] = data[col].str.replace('HKDataType', '')
    data[col] = data[col].str.replace('HKCategoryTypeIdentifier', '')
    data[col] = data[col].str.replace('HKCategory', '')
    return data

def dropping_col (dataframe, col):
    dataframe.drop(col, inplace = True, axis= 1)
    return dataframe

def sleep_cleaning (data):
    sleep = data[data['type']== 'SleepAnalysis']
    data.drop(data[data['type']== 'SleepAnalysis'].index, inplace = True)
    mediciones_2 = data['type'].unique()
    return data, sleep

def measured_var (dataframe, col):
    var_med = dataframe[col].unique()
    return var_med

def to_num (dataframe,col):
    dataframe['value_2'] = dataframe.apply(lambda row: pd.to_numeric(row[col], errors = 'coerce'), axis = 1)
    no_num_val = dataframe[dataframe['value_2'].isnull()]['type'].unique()    
    return dataframe, no_num_val