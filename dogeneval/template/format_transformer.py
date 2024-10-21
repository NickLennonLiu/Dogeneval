import pandas as pd
import json, re, os, sys, time, datetime, random

file = "templates_v3.json"

df = pd.read_json(file)

df.to_excel("templates_v3.xlsx", index=False)
df.to_parquet("templates_v3.parquet", index=False)
df.to_csv("templates_v3.csv", index=False)