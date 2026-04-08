#
# Project: Sales Intelligence Analysis for Scale Model Cars
# System: macOS / VS Code
# Author: Mohammad Yazdani
#

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

##################################################################
#
# select_n_rows:
#
# Given a database connection and a SQL Select query,
# executes this query against the database and returns
# a list of rows retrieved.
#
def select_n_rows(dbConn, sql, parameters = None):
    if parameters is None:
        parameters = []

    dbCursor = dbConn.cursor()

    try:
        dbCursor.execute(sql, parameters)
        rows = dbCursor.fetchall()
        return rows
    except Exception as err:
        print("select_n_rows failed: " + str(err))
        return None
    finally:
        dbCursor.close()

##################################################################
#
# run_sql_file:
#
# Helper function to read a .sql file and execute it using
# the datatier logic.
#
def run_sql_file(dbConn, filename):
    try:
        with open(filename, 'r') as f:
            sql = f.read()
        return select_n_rows(dbConn, sql)
    except Exception as err:
        print("run_sql_file failed: " + str(err))
        return None

##################################################################
#
# main
#
dbConn = sqlite3.connect('stores.db')
sns.set_theme(style="whitegrid")

print("** Scale Model Cars: Sales Intelligence Analysis **")

try:
    # 1. Inventory Management Analysis
    print("\nExecuting Inventory Analysis (q1.sql)...")
    res1 = run_sql_file(dbConn, 'q1.sql')
    
    if res1:
        # Aligning with 5-column output from q1.sql
        df1 = pd.DataFrame(res1, columns=['Code', 'Product', 'Line', 'LowStockRatio', 'Revenue'])
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='LowStockRatio', y='Product', data=df1, palette='Oranges_r')
        plt.title('Inventory Priority: Top 10 High-Demand/Low-Stock Products', fontsize=14)
        plt.xlabel('Low Stock Ratio (Priority)')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('inventory_priority.png')
        print("  > inventory_priority.png successfully generated.")

    # 2. VIP Customer Analysis
    print("\nExecuting Customer Analysis (q2.sql)...")
    res2 = run_sql_file(dbConn, 'q2.sql')
    
    if res2:
        # Limit to top 10 rows and map columns
        top_10_customers = res2[:10]
        df2 = pd.DataFrame(top_10_customers, columns=['CustomerID', 'Profit'])
        df2['CustomerID'] = df2['CustomerID'].astype(str)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Profit', y='CustomerID', data=df2, palette='Greens_r')
        plt.title('Customer Concentration: Top 10 VIPs by Profit Contribution', fontsize=14)
        plt.xlabel('Total Profit ($)')
        plt.ylabel('Customer ID')
        plt.tight_layout()
        plt.savefig('top_vip_customers.png')
        print("  > top_vip_customers.png successfully generated.")

    # 3. Business Metric Output
    print("\nExecuting LTV Analysis (q3.sql)...")
    res3 = run_sql_file(dbConn, 'q3.sql')
    
    if res3:
        ltv = res3[0][0]
        print(f"\nGeneral Statistics:")
        print(f"  Average Customer LTV: ${ltv:,.2f}")

except Exception as e:
    print(f"Error during analysis: {e}")

finally:
    if dbConn:
        dbConn.close()
        print("\nAnalysis Complete. Database connection closed.")