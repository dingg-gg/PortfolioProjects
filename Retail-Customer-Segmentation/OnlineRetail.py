import pandas as pd
import numpy as np


file_name = 'online_retail_II.xlsx'
df = pd.read_excel(file_name)

originalrows = len(df)
print(df.head())

df = df.dropna(subset=['Customer ID'])

df['Revenue'] = df['Quantity'] * df['Price']

# Keep only rows where Invoice does NOT contain 'C'
df = df[~df['Invoice'].astype(str).str.contains('C', na=False)]

# Only keep transactions with positive price and quantity
df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

print(df.head())

print(f"Original rows: {originalrows}") # Estimate for the 2009-2010 sheet
print(f"Cleaned rows: {len(df)}")
print(f"Total Unique Customers: {df['Customer ID'].nunique()}")

# To calculate how recent was their last purchase 

# Set 'today' to be the day after the latest purchase in the data
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Group by Customer ID and calculate RFM metrics
rfm = df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Recency
    'Invoice': 'nunique',                                   # Frequency
    'Revenue': 'sum'                                        # Monetary
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']
# We keep those with postive money values
rfm = rfm[rfm['Monetary'] > 0]

print("\n--- RFM Feature Store ---")
print(rfm.head())
print(f"\nTotal Customers Summarized: {len(rfm)}")

# We want to identify customers based on different profile groups, like whales, used to be whales, upcoming and window shoppers

conditions = [
    (rfm['Monetary'] > rfm['Monetary'].quantile(0.9)), # Whales
    (rfm['Recency'] > 180) & (rfm['Monetary'] > rfm['Monetary'].median()), # Whales that stopped(Slipping Whales)
    (rfm['Recency'] < 30) & (rfm['Frequency'] > 5), # Upcoming Customers
    (rfm['Frequency'] == 1) & (rfm['Recency'] > 200) # Dead Leads
]

choices = ['Whale', 'Slipping Whales', 'Upcoming', 'Dead Lead']

rfm['Custom_Segment'] = np.select(conditions, choices, default='Standard Customer')

print(rfm['Custom_Segment'].value_counts())


# After profiling, we should calculate how much percentage of the revenues do each group share overall

segment_analysis = rfm.groupby('Custom_Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'sum', 'count']
}).round(2)

# Calculate the Revenue Share
total_revenue = rfm['Monetary'].sum()
segment_analysis['Revenue_Share_%'] = (segment_analysis[('Monetary', 'sum')] / total_revenue * 100).round(2)

print(segment_analysis)

# The whales are spending a lot of moeny around 60% of the revenue, we should check for outliers or see who are the bigger spenders

# Sort by Monetary to find the biggest spenders
top_10_whales = rfm.sort_values(by='Monetary', ascending=False).head(10)

print(" The Top 10 Super-Whales")
print(top_10_whales)

# Calculate the percentage of total revenue from just the Top 10
top_10_revenue = top_10_whales['Monetary'].sum()
total_revenue = rfm['Monetary'].sum()
percentage = (top_10_revenue / total_revenue) * 100

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Top 10 Revenue: ${top_10_revenue:,.2f}")
print(f"The Top 10 customers contribute {percentage:.2f}% of all revenue.")

# Join the segment info back to the original df to see where the whales come from
top_countries = df[df['Customer ID'].isin(top_10_whales.index)]['Country'].unique()
print(top_countries)

# We want to find out what were the slipping whales buying so we can campaign to win them back
# Get IDs for Slipping Whales
slipping_ids = rfm[rfm['Custom_Segment'] == 'Slipping Whales'].index

# Find their most purchased items
top_items_slipping = df[df['Customer ID'].isin(slipping_ids)]['Description'].value_counts().head(5)
print("\n--- Top Products for Slipping Whales ---")
print(top_items_slipping)
