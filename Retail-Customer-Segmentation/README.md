# Retail-Customer-Segmentation

## Project Overview
This is a self-initiated data analytics project which uses the [Online Retail II](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset) dataset from Kaggle.


## Project Motivation
* I am using this project to refine my proficiency in Python(NumPy & Pandas)
* My goal is to move beyond basic data cleaning and leveraging my analytical mindset to explore and identify insights and patterns in retail behaviour.
* By analyzing 525,461 transactions, I aim to gather high-value insights that can help to drive business decisions.

## Key Findings
* **Revenue:** Identified that **432** Whale customers (top 10%) are responsible for **59.87%** of the total revenue.
* **Impact:** The **Top 10 Super-Whales** alone contributed up to **17.75%** of all revenue, which indicates a high dependency on wholesale accounts.
* **Churn Risk:** Flagged **130 "Slipping Whales"** who had a high historical value but have not purchased in over **180 days**.
* **Targeted Recovery:** To facilitate win-back campaigns, the top 5 products bought by at-risk segments were identified.

## Methodology
* **Data Integrity:** Cleaned a dataset of **525,461 rows**, handled cancellations (C-prefix invoices), and removed missing Customer IDs.
* **RFM Modeling:** Engineered features for **Recency**, **Frequency**, and **Monetary** value to build a customer feature store.
* **Custom Segmentation:** Rather than using pre-made templates, NumPy Select was used to apply logic to create unique behavioral profiles.
* **Statistical Analysis:** To distinguish retail behavior from high-volume B2B transactions, quantiles and outlier detection were employed.

## Business Insights & Strategic Direction

* **VIP Retention Program:** With **432 "Whales"** generating **60%** of revenue, the business should implement a dedicated **Loyalty Tier**. Focus on direct relationship management for these accounts to protect the core revenue stream.
* **B2B Strategy:** The **Top 10 Super-Whales** drive **17.75%** of all sales. This might suggest a significant wholesale/B2B component. I recommend developing a separate **Wholesale Portal** or volume-based pricing to encourage larger bulk orders.
* **Re-activation Campaign:** We have identified **130 "Slipping Whales"** with high historical value. Since we know their top products, the business should launch a **Personalized Email Campaign** offering a "We Miss You" discount on those specific items.
* **Lead Conversion:** For the **"Dead Leads"** (single-purchase customers), the data suggests they are not returning on their own. The business should analyze if the cost of acquiring these customers exceeds their value and consider reallocating that budget toward the **"Upcoming"** segment.
