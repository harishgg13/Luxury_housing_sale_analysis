#importing necessary library
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

#----------------------------------------------------------------------------------------------------------------------------------
# Establishing Connection
engine = create_engine("mysql+pymysql://root:12345678@localhost:3306/Capstone_project_2")

#----------------------------------------------------------------------------------------------------------------------------------

pd.set_option("display.max_columns", None)
#extracting data
data_path="/Users/ggharish13/Data Science/Capstone Project/Luxury Housing sales/Luxury_Housing_Bangalore.csv"
data_original=pd.read_csv(data_path) #101000 rows X 18 Columns
data=pd.DataFrame(data_original)
# print(data) # to check the datas. index 1 of buyer_comments has Nan
# print(data.info()) 

# from above info
# Buyer_Comments has NULL Values. handle with tofill with "no comments" object ✅
# Ticket_Price_Cr has object values. correct it using lstrip and rstrip and remove rs symbol and cr text and change it to float ✅
# try to Fill Nan Values in unit_size 
# try to Fill Nan Values in ticket_price ✅
# try to Fill Nan Values in amentiy_score ✅
# Purchase_Quarter to date format ✅

#----------------------------------------------------------------------------------------------------------------------------------

# Data Cleaning
# 1. Filling the Nan values of Buyer_Comments
data["Buyer_Comments"]=data["Buyer_Comments"].fillna("No Commects")
# print(data) # to check the Buyer_comments is filled. check index 1 to conform
# print(data.info()) 

#--------------------------------------------------------------------------------------------------------------------------------

# 2.1 Cleaning Ticket_Price_Cr. Correcting the object values to float values
# print(data["Ticket_Price_Cr"]) # check the Ticket_Price_Cr values
data["Ticket_Price_Cr"]=data["Ticket_Price_Cr"].str.lstrip("₹")
data["Ticket_Price_Cr"]=data["Ticket_Price_Cr"].str.rstrip(" Cr")

# 2.1 converting it to float
data["Ticket_Price_Cr"]=data["Ticket_Price_Cr"].astype(float)
# print(data["Ticket_Price_Cr"])
# print(data.info()) 


#--------------------------------------------------------------------------------------------------------------------------------

#identified outliers in Ticket_Price_Cr (above 50 cr)
'''fig1=plt.hist(data["Ticket_Price_Cr"])
plt.show()'''

#identified outliers in Unit_Size_Sqft (0 to 1000)
'''fig1=plt.hist(data["Unit_Size_Sqft"])
plt.show()

fig1=plt.hist(data["Amenity_Score"])
plt.show()'''

#--------------------------------------------------------------------------------------------------------------------------------

# 2 Cleaning Purchase_Quarter. purchase quarter has date formate value. spliting that column in to purchase year and quarter for better analye
data.insert(9,"Purchase_Year",None)
data["Purchase_Quarter"]=pd.to_datetime(data["Purchase_Quarter"])
data["Purchase_Year"]=data["Purchase_Quarter"].dt.year
data["Purchase_Quarter"]=data["Purchase_Quarter"].dt.month


data.insert(9,"Purchase_Yr_Q",None)
data["Purchase_Yr_Q"]=data["Purchase_Year"].astype(str)+"-Q"+data["Purchase_Quarter"].astype(str)
# print(data)
# print(data.info()) 

#--------------------------------------------------------------------------------------------------------------------------------
# data=data.dropna(axis=0) #removing null values is bad idea, because, we left over with only 73751 rows
# print(data)

#--------------------------------------------------------------------------------------------------------------------------------
# 3. try to Fill Nan Values in amentiy_score
data["Micro_Market"]=data["Micro_Market"].str.capitalize() #cleaning duplicates

# print(data["Amenity_Score"]) #1st index is empty. 
Avg_amenity=data.groupby(["Micro_Market","Developer_Name"])["Amenity_Score"].mean().reset_index().rename(columns={"Amenity_Score": "avgAmenity"})
data=data.merge(Avg_amenity,on=["Micro_Market","Developer_Name"],how="left")
data["Amenity_Score"]=data.apply(
    lambda row: row["avgAmenity"]
                if pd.isna(row["Amenity_Score"]) else row["Amenity_Score"],
    axis=1
)
data=data.drop(columns="avgAmenity")
# print(data["Amenity_Score"]) #1st index is empty.  check is it filled
# print(data.info())

#--------------------------------------------------------------------------------------------------------------------------------
# 4. deleting the rows that has less than 0 or null in both sqft and ticket price.

# data_drop = data[((data["Ticket_Price_Cr"].isna())|(data["Ticket_Price_Cr"] < 0)) & ((data["Unit_Size_Sqft"].isna())|(data["Unit_Size_Sqft"] < 0))]
# data_drop.to_csv("data_drop.csv") # double checking the condition worked right or not by seeing the tabular csv file in excel

data = data.drop(data[((data["Ticket_Price_Cr"].isna())|(data["Ticket_Price_Cr"] < 0)) & ((data["Unit_Size_Sqft"].isna())|(data["Unit_Size_Sqft"] < 0))].index)

# print(data.info())

#--------------------------------------------------------------------------------------------------------------------------------


# 5. try to Fill Nan Values in ticket_price refernce index 26,40,43,51,53

#finding average of price of house in particular area and particular developer.
group_data1 = (data.groupby(["Micro_Market", "Developer_Name"]).agg(median_Ticket_Price_Cr=("Ticket_Price_Cr", "median"),
            median_Unit_Size_Sqft=("Unit_Size_Sqft", "median")).reset_index())
#merging the data with all above particular combination in big data
data = data.merge(group_data1, on=["Micro_Market","Developer_Name"], how="left")

#finding average price per sqft
data["price_per_sqft"]=data["median_Ticket_Price_Cr"]/data["median_Unit_Size_Sqft"]

# for pricing the house, the Connectivity_Score, Amenity_Score and Locality_Infra_Score are important. to take all in consider, we get average of all three
data["weight_score"]=(data["Amenity_Score"]+data["Locality_Infra_Score"]+data["Connectivity_Score"])/3

#finding average of weight_score in particular area and particular developer. for computing with average_sqft with, to get, price per sqft considering weight. 
# note, if we compute it with weight score, it will be biased. 
# it will look like, (Avg_Ticket_Price_Cr/weight_score) *weight_score will result the same Avg_Ticket_Price_Cr. so we find average.
group_data2 = data.groupby(["Micro_Market", "Developer_Name"])["weight_score"].mean().reset_index().rename(columns={"weight_score":"average_weight_score"})
data = data.merge(group_data2, on=["Micro_Market","Developer_Name"], how="left")

#findind price per weight.
data["price_per_weight"]=data["price_per_sqft"]/data["average_weight_score"]

# to find the price to house, price_per_weight  * weight_score * Unit_Size_Sqft
data["Ticket_Price_Cr"]=data.apply(
    lambda row: (row["price_per_weight"]*row["weight_score"])*row["Unit_Size_Sqft"]
                if (pd.isna(row["Ticket_Price_Cr"]) or row["Ticket_Price_Cr"]<0) else row["Ticket_Price_Cr"],axis=1)

#--------------------------------------------------------------------------------------------------------------------------------
# 6. try to Fill Nan Values in unit_size refer index 17,18,24,33

data["Unit_Size_Sqft"]=data.apply(
    lambda row: row["Ticket_Price_Cr"]/(row["price_per_weight"]*row["weight_score"])
                if (pd.isna(row["Unit_Size_Sqft"]) or row["Unit_Size_Sqft"]<0) else row["Unit_Size_Sqft"],axis=1)

data=data.drop(columns=["median_Ticket_Price_Cr","median_Unit_Size_Sqft","price_per_sqft",
                        "weight_score","average_weight_score","price_per_weight"])

#--------------------------------------------------------------------------------------------------------------------------------
#7. dopping the null value rows.

data=data.dropna().reset_index(drop=True)
data["price_per_sqft_thousands"]=round((data["Ticket_Price_Cr"]/data["Unit_Size_Sqft"])*10000000,2)
cleaned_data=data.copy()
# print(cleaned_data)
cleaned_data.to_csv("LHS.csv")
#--------------------------------------------------------------------------------------------------------------------------------

# fig=plt.hist(x=cleaned_data["Unit_Size_Sqft"],color="green")
# plt.show()

# fig=plt.hist(x=cleaned_data["Ticket_Price_Cr"],color="red")
# plt.show()

#--------------------------------------------------------------------------------------------------------------------------------

# print(data[data["Unit_Size_Sqft"]>50000])
# there ar more 1010 data that will look like outliers, but logically right. 50,000 for 100cr. so they are not outliers. 
# some of people might purchased it. we can say it as, datas are not fallen in same group.

#----------------------------------------------------------------------------------------------------------------------------------
# inserting the table to SQL database.
# cleaned_data.to_sql("LHS",engine,index=False)

# shortdata=cleaned_data.head(100)
# shortdata.to_csv("shortData.csv")