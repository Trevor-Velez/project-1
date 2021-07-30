import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def clean_crime_data(crime, file):
    # Read in our CSV File
    dataframe = pd.read_csv(file)
    
    # Create a new dataframe with only Brazil values
    dataframe = dataframe.loc[(dataframe["Unnamed: 2"] == "Brazil"), :]
    
    # Renaming the columns to be more usable
    dataframe = dataframe.rename(columns = {
        "Unnamed: 0": "Region",
        "Unnamed: 1": "Sub-Region",
        "Unnamed: 2": "Country",
        "2013": "2013 Count",
        "2013.1": "2013 Rate",
        "2014": "2014 Count",
        "2014.1": "2014 Rate",
        "2015": "2015 Count",
        "2015.1": "2015 Rate",
        "2016": "2016 Count",
        "2016.1": "2016 Rate",
        "2017": "2017 Count",
        "2017.1": "2017 Rate"})
    
    # Creating a new dataframe where the rows are the years
    # Since dataframe is only 1 row right now, we use iloc on row 0 and the specify the column name
    final_dataframe = pd.DataFrame({
        "Year": ["2013", "2014", "2015", "2016", "2017"],
        
        f"{crime} Count": [dataframe.iloc[0]["2013 Count"],
                       dataframe.iloc[0]["2014 Count"],
                       dataframe.iloc[0]["2015 Count"],
                       dataframe.iloc[0]["2016 Count"], 
                       dataframe.iloc[0]["2017 Count"] ],
        
        f"{crime} Rate": [dataframe.iloc[0]["2013 Rate"],
                      dataframe.iloc[0]["2014 Rate"],
                      dataframe.iloc[0]["2015 Rate"], 
                      dataframe.iloc[0]["2016 Rate"], 
                      dataframe.iloc[0]["2017 Rate"]]})
    
    # The data right now is in strings and I need it as numbers to plot
    # I created a list from the count column and then took out all of the commas
    count_list = final_dataframe[f"{crime} Count"].tolist()
    final_dataframe[f"{crime} Count"].replace({count_list[0]: count_list[0].replace(',', ''),
                                               count_list[1]: count_list[1].replace(',', ''),
                                               count_list[2]: count_list[2].replace(',', ''),
                                               count_list[3]: count_list[3].replace(',', ''),
                                               count_list[4]: count_list[4].replace(',', '')}, inplace=True)
    
    # Then I made the values in Count and Rate into numeric values
    final_dataframe[[f"{crime} Count", f"{crime} Rate"]] = final_dataframe[[f"{crime} Count", f"{crime} Rate"]].apply(pd.to_numeric)
    
    return final_dataframe.set_index("Year")



def clean_homicide_data(crime, file):
    dataframe = pd.read_csv(file)
    
    dataframe = dataframe.loc[(dataframe["Territory"] == "Brazil"), :]
    
    dataframe = dataframe.loc[
        (dataframe["Year"] == 2013) |
        (dataframe["Year"] == 2014) |
        (dataframe["Year"] == 2015) | 
        (dataframe["Year"] == 2016) |
        (dataframe["Year"] == 2017), :]
    
    
    final_dataframe = pd.DataFrame({
    "Year": ["2013", "2014", "2015", "2016", "2017"],
        
    f"{crime} Count": [dataframe.iloc[0]["Value"],
                       dataframe.iloc[1]["Value"],
                       dataframe.iloc[2]["Value"],
                       dataframe.iloc[3]["Value"], 
                       dataframe.iloc[4]["Value"] ],
        
    f"{crime} Rate": [dataframe.iloc[5]["Value"],
                      dataframe.iloc[6]["Value"],
                      dataframe.iloc[7]["Value"], 
                      dataframe.iloc[8]["Value"], 
                      dataframe.iloc[9]["Value"]]})
    
    return final_dataframe.set_index("Year")
    
    
    
def clean_drug_data(crime, file):
    
    dataframe = pd.read_csv(file)
    
    dataframe = dataframe.loc[(dataframe["Country"] == "Brazil"), :]
    
    dataframe = dataframe.loc[
        (dataframe["Year"] == 2013) |
        (dataframe["Year"] == 2014) |
        (dataframe["Year"] == 2015) | 
        (dataframe["Year"] == 2016) |
        (dataframe["Year"] == 2017), :]
        
    grouped_dataframe = dataframe.groupby("Year").agg('sum')
    
    return grouped_dataframe


def read_Crime_Index(files):
    
    crime_index_df = pd.DataFrame(columns=["Year", "Country", "Crime Index"])
    
    year_list = ["2013", "2014","2015","2016","2017"]
    i = 0
    
    for x in files:
        dataframe = pd.read_csv(files[i])
        dataframe = dataframe.loc[(dataframe["Country"] == "Brazil") | (dataframe["Country"].str.contains("Rio de Janeiro"))]
        dataframe["Year"] = year_list[i]
        crime_index_df = crime_index_df.append(dataframe, ignore_index=True)
        i += 1
    
    crime_index_df = crime_index_df.set_index("Year")
    crime_index_df = crime_index_df[["Country","Crime Index"]]
    
    return crime_index_df