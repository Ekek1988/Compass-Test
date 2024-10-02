# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 21:43:42 2024

@author: lank1
"""

from difflib import SequenceMatcher
import pandas as pd


# Load database CSV
file_path = 'C:\Test_Compass\Code Assessment - Find Duplicates Input - SampleCodecsv (1) (1).csv'
df = pd.read_csv(file_path)

# Print the DataFrame and its columns to verify structure
print("DataFrame columns:", df.columns)
print("First few rows of the DataFrame:")
print(df.head())  #First lines to see data
print(df.info())  #Information of database


# Helper function to calculate match score between two strings
def similarity_score(str1, str2):
    if pd.isna(str1) or pd.isna(str2):
        return 0  # Return 0 if either string is NaN
    return SequenceMatcher(None, str(str1), str(str2)).ratio()

# Function to find duplicates based on defined matching criteria
def find_potential_duplicates(df):
    potential_matches = []
    
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            # Compare records
            contact1 = df.iloc[i]
            contact2 = df.iloc[j]
            
            # Calculate scores for each field
            name_score = similarity_score(contact1['name'], contact2['name'])
            last_name_score = similarity_score(contact1['name1'], contact2['name1'])
            email_score = similarity_score(contact1['email'], contact2['email'])
            zip_score = similarity_score(str(contact1['postalZip']), str(contact2['postalZip']))
            address_score = similarity_score(contact1['address'], contact2['address'])
            
            # Define the overall accuracy score based on weighted fields
            total_score = (email_score * 0.4 + name_score * 0.2 + last_name_score * 0.2 + zip_score * 0.1 + address_score * 0.1)

            # Categorize the match accuracy
            if total_score > 0.85:
                match_accuracy = "High"
            elif total_score > 0.6:
                match_accuracy = "Medium"
            else:
                match_accuracy = "Low"

            # Add the match to potential matches list if above a threshold
            if total_score > 0.5:
                potential_matches.append({
                    'Source ContactID': contact1['contactID'],
                    'Match ContactID': contact2['contactID'],
                    'Accuracy': match_accuracy
                })
    
    return pd.DataFrame(potential_matches)

# Apply the function to the dataset
potential_matches_df = find_potential_duplicates(df)
potential_matches_df
