#Import Packages
import pandas as pd
import json
from kaggle.api.kaggle_api_extended import KaggleApi
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""Save Key API into JSON"""
data_token = {"username": "yourname", "key": "xxxxxxxxxxxx"}
file_json = r"C:\Users\.kaggle\kaggle.json"

with open(file_json, "w") as file:
    json.dump(data_token, file, indent=4)

"""Run download dataset using Kaggle Api"""
api = KaggleApi()
api.authenticate()

api.dataset_download_files("spscientist/students-performance-in-exams",path="data",unzip=True)

api = KaggleApi()
api.authenticate()

"""Load dataset from CSV format"""
df = pd.read_csv("data/StudentsPerformance.csv")
print(df.head()) #test to know if dataset already loaded

"""1. Cleaning Data And Formatting"""

def transform_gender(x):
    if x == "male":
        return "M"
    elif x == "female":
        return "F"
    else:
        return ""

def transform_ethnic(x):
    if "GROUP" in x.upper() :
        return x[-1]
    else:
        return ""

def transform_education(x):
    if x == "some high school":
        return 1
    elif x == "high school":
        return 2
    elif x == "some college":
        return 3
    elif x == "associate's degree":
        return 4
    elif x == "bachelor's degree":
        return 5
    elif x == "master's degree":
        return 6
    else:
        return 0

def transform_lunch(x):
    if x == "free/reduced":
        return "FREE"
    elif x == "standard":
        return "Standard"
    else:
        return ""

def transform_preparation(x):
    if x == "none":
        return "N"
    elif x == "completed":
        return "Y"
    else:
        return ""

df_copy = df.copy()

df_copy.rename(columns={"gender": "GENDER"}, inplace=True)
df_copy["GENDER"] = df["gender"].apply(transform_gender)
df_copy.rename(columns={"race/ethnicity": "ETHNICITY"}, inplace=True)
df_copy["ETHNICITY"] = df["race/ethnicity"].apply(transform_ethnic)
df_copy.rename(columns={"parental level of education": "EDUCATION"}, inplace=True)
df_copy["EDUCATION"] = df["parental level of education"].apply(transform_education)
df_copy.rename(columns={"lunch": "LUNCH"}, inplace=True)
df_copy["LUNCH"] = df["lunch"].apply(transform_lunch)
df_copy.rename(columns={"test preparation course": "PREPARATION COURSE"}, inplace=True)
df_copy["PREPARATION COURSE"] = df["test preparation course"].apply(transform_preparation)

# Check validity score
if df[(df['math score'] < 0) | (df['math score'] > 100)].empty:
    print("OK")
    df_copy.rename(columns={"math score": "MATH SCORE"}, inplace=True)
else:
    print("Math Score is not valid")

if df[(df['reading score'] < 0) | (df['reading score'] > 100)].empty:
    print("OK")
    df_copy.rename(columns={"reading score": "READING SCORE"}, inplace=True)
else:
    print("Reading Score is not valid")

if df[(df['writing score'] < 0) | (df['writing score'] > 100)].empty:
    print("OK")
    df_copy.rename(columns={"writing score": "WRITING SCORE"}, inplace=True)
else:
    print("Writing Score is not valid")

# Check duplicate
print("Sum of duplicated Data:", df_copy.duplicated().sum())

# Check Empty Value
df_copy.isnull().sum()

# Check data type
df_copy.info()

# Save into local directory
df_copy.to_excel("students_performance.xlsx", index=False)

