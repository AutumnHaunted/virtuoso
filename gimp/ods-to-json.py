import os
from pyexcel_ods import get_data
import json

try:
    
    print("Converting...")
    
    data = get_data("cards.ods")
    print("Successfully opened \"cards.ods\".")
    
    with open("cards.json", "w") as x:
        json.dump(data, x)
        print("Successfully output data to \"cards.json\".")
    
    input("Process completed successfully.")
    
except:
    input("Process failed.")