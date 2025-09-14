# Luxury Housing Sales Data Cleaning  

## 📌 Project Overview

The Luxury Housing Sales Data Cleaning Project focuses on preparing real-estate transaction data from Bangalore for analysis and decision-making. The dataset contains over 100,000 rows and 18 columns.

Raw real-estate data is often messy and inconsistent, containing missing values, formatting errors, and potential outliers. This project applies systematic data cleaning techniques to ensure accuracy, consistency, and usability of the dataset for further analytics, visualization, and reporting in Power BI.

------------------------------------------------------------------------

## 🎯 Objectives

- **Used Python to do data extraction, cleaning and pushing the datas to database**

- **Database Connection**: Connects to MySQL using SQLAlchemy.  

- **Data Extraction**: Reads CSV file (`Luxury_Housing_Bangalore.csv`) into a Pandas DataFrame.  

- **Data Cleaning Steps**:  

   (a) Fills missing values in `Buyer_Comments` with `"No Comments"`.  
   (b) Cleans and converts `Ticket_Price_Cr` from string (₹ XX Cr) to float.  
   (c) Converts `Purchase_Quarter` to proper datetime format and extracts:  
   (d) Handles missing values in `Amenity_Score` by replacing them with the developer + micro-market average.  
   (e) Removes invalid rows where both `Ticket_Price_Cr` and `Unit_Size_Sqft` are missing or negative.  
   (f) Fills missing/invalid `Ticket_Price_Cr` using weighted price estimation.  
   (g) Fills missing/invalid `Unit_Size_Sqft` using reverse-calculation from price. 
   (h) Standardize inconsistent text fields like Micro_Market.
   (i) Drops remaining null values.  
   (j) Creates derived column `price_per_sqft_thousands`.  

Prepare the cleaned dataset for storage in a **SQL database** for use in **Power BI dashboards**.

------------------------------------------------------------------------

## 🛠 Tech Stack

Python – Data cleaning, preprocessing, feature engineering

Pandas & NumPy – Data manipulation and handling missing values

Matplotlib – Data visualization (basic histograms and outlier detection)

SQLAlchemy + MySQL – Database connection and storage of cleaned data

Power BI – Interactive dashboards, visualization, and trend analysis

------------------------------------------------------------------------

## 📊 Power BI Visualizations

The cleaned dataset is analyzed in Power BI through the following key dashboards:

Market Trends – Quarter-wise booking trends across micro-markets (Line Chart).

Builder Performance – Total & average ticket sales by builder (Bar/Table).

Amenity Impact – Correlation between amenity score and booking success (Scatter Plot).

Booking Conversion – Conversion rates by micro-market (Stacked Column).

Configuration Demand – Popular housing configurations (Pie/Donut).

Sales Channel Efficiency – Bookings by sales channel (100% Stacked Column).

Quarterly Builder Contribution – Builder dominance each quarter (Matrix Table).

Possession Status – Effect of possession status on buyer type & booking (Clustered Column).

Geographical Insights – Project concentration across Bangalore (Map).

Top Performers – Top 5 builders by revenue & bookings (KPI Cards).

------------------------------------------------------------------------

## 🛠️ Requirements  
Install dependencies before running the script:  
```bash
pip install pandas matplotlib sqlalchemy pymysql
```  

------------------------------------------------------------------------

## ▶️ Usage  
1. Update the `data_path` variable with the location of your dataset.  
2. Update database credentials in:  
   ```python
   engine = create_engine("mysql+pymysql://root:'yourpassword'@localhost:3306/Capstone_project_2")
   ```  
3. Run the script:  
   ```bash
   python DataCleaning.py
   ```  
4. Find cleaned dataset in `LHS.csv`.  

------------------------------------------------------------------------

## 📊 Notes  
- Outliers in `Ticket_Price_Cr` (>50 Cr) and `Unit_Size_Sqft` (>1000 sqft or very high values) were identified but **not removed**, since they could be valid cases.  
- The script allows exporting cleaned data to SQL or CSV.  
- Visualizations (histograms) are available but commented out for optional use.  

------------------------------------------------------------------------

## 🎓 Skills & Learning Outcomes

By working on this project, the following skills were applied and strengthened:

Handling large real-estate datasets (100K+ rows) efficiently

Performing data cleaning & preprocessing (missing values, text-to-numeric conversion, outlier handling)

Feature engineering for analytics (e.g., price per sqft, purchase quarter/year)

SQL integration for storing cleaned datasets in relational databases

Designing Power BI dashboards for:

Market trends & builder performance

Amenity impact on bookings

------------------------------------------------------------------------

## 👨‍💻 Author

**G G Harish**
- 📧 Email: <harishgg03@gmail.com>
- 💼 LinkedIn: [harishgg13](https://www.linkedin.com/in/ggharish13)

Conversion rates & sales efficiency

Geographical project insights

Building an end-to-end pipeline from raw data → cleaned dataset → visualization

---
