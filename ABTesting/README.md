# Mobile Game A/B Testing

## Project Overview
This project uses **Python** to evaluate user behaviour in a mobile gaming environment.
I analyzed 90 000 player logs and identified how game progression mechanics influence long-term engagement.

## Methodology
* **Data Source** User-level logs provided via Kagglehub
* **Data Cleaning** Identified and removed extreme outliers
* **Statistical Approach** Employed **Bootstrap Analysis** with 1000 iterations to simulate 7-day retention outcomes and determine statistical significance.

## Key Result
| Metric | Gate 30 (Control) | Gate 40 (Variant) | Winner |  
| **1-Day Retention** | 44.82% | 44.23% | **Gate 30** |  
| **7-Day Retention** | 19.02% | 18.20%| **Gate 30** |

## BootStrap Probability
The simulation shows a 99.9% Probability that Gate 30 maintains a higher long-term retention than Gate 40

## Business Recommendation
Maintain the gate at Level 30 to retain more players
