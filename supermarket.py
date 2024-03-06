import pandas as pd
from pandasql import sqldf
import matplotlib.pyplot as plt

# Data Analysis 

# Create a lambda function to execute SQL queries
sql = lambda q: sqldf(q, globals())

# Read the data from CSV files into Pandas DataFrames
df = pd.read_csv('data.csv')
df1 = pd.read_csv('data1.csv')
df2 = pd.read_csv('data2.csv')

# Query to filter data for Females with a rating greater than 8, sorted by rating, and limiting to 5 rows
data = sql('SELECT * FROM df WHERE Gender = "Female" AND Rating > 8.0 ORDER BY Rating DESC LIMIT 5')
print("Filtered Data for Females with Rating > 8.0:")
print(data.head())

# Group by Product Line and count the occurrences for Females
data_one = sql('SELECT "Product line", COUNT(*) as Count FROM df WHERE Gender = "Female" GROUP BY "Product line"')
print("\nGrouped by Product line for Females:")
print(data_one)

# Select payment information for Females
female_payment = sql('SELECT "Gender", "Payment" FROM df WHERE Gender = "Female"')
print("\nFemale Payment Information:")
print(female_payment)

# Select payment information for Males
male_payment = sql('SELECT "Gender", "Payment" FROM df WHERE Gender = "Male"')
print("\nMale Payment Information:")
print(male_payment)

# Combine payment information for Females and males using UNION ALL
combined_payment = sql('SELECT * FROM female_payment UNION ALL SELECT * FROM male_payment')
print("\nCombined Payment Information:")
print(combined_payment)

# Select specific columns (Branch, City, and Gender) from the original dataframe
new_table = sql("SELECT Branch, City, Gender FROM df")
print("\nSelected Columns (Branch, City, Gender):")
print(new_table)

# Create a new table by joining data from df1 and df2
new_data = sql('SELECT df1.Branch, df1.Customer, df1.Product, df2.Payment, df2.Rating FROM df1 JOIN df2 ')
print("\nNew Table created by Joining df1 and df2:")
print(new_data)

# Join df1 and df2 on the common column Invoice_ID
new_join = sql('SELECT df1.Invoice_ID, df1.Branch, df1.Customer, df1.Product, df2.Payment, df2.Rating FROM df1 JOIN df2 ON df1.Invoice_ID = df2.Invoice_ID')
print("\nJoining df1 and df2 on Invoice_ID:")
print(new_join)

# Average Rating by Product Line
avg_rating_by_product = sql('SELECT "Product line", AVG(Rating) as Avg_Rating FROM df GROUP BY "Product line"')
print("\nAverage Rating by Product Line:")
print(avg_rating_by_product)

# Total Sales by Branch
total_sales_by_branch = sql('SELECT Branch, SUM(Total) as Total_Sales FROM df GROUP BY Branch')
print("\nTotal Sales by Branch:")
print(total_sales_by_branch)

# Revenue Distribution by Payment Method
revenue_by_payment_method = sql('SELECT Payment, SUM(Total) as Total_Revenue FROM df GROUP BY Payment')
print("\nRevenue Distribution by Payment Method:")
print(revenue_by_payment_method)

#Top Selling Products
top_selling_products = sql('SELECT "Product line", SUM(Quantity) as Total_Quantity FROM df GROUP BY "Product line" ORDER BY Total_Quantity DESC')
print("\nTop Selling Products:")
print(top_selling_products)


# Data Visulization

# 1. Bar Chart - Total Sales by Branch
plt.figure(figsize=(10, 6))
colors = ['skyblue', 'lightgreen', 'lightcoral']
for i, branch in enumerate(total_sales_by_branch['Branch']):
    plt.bar(branch, total_sales_by_branch['Total_Sales'][i], color=colors[i], label=branch)
    plt.text(branch, total_sales_by_branch['Total_Sales'][i] + 1000, f'{total_sales_by_branch["Total_Sales"][i]:,.0f}', ha='center', va='bottom')
plt.legend()
plt.title('Total Sales by Branch')
plt.xlabel('Branch')
plt.ylabel('Total Sales')
plt.savefig('total_sales_branch_chart.png')
plt.show()

# 2. Line Chart - Average Rating by Product Line
plt.figure(figsize=(10, 6))
plt.plot(avg_rating_by_product['Product line'], avg_rating_by_product['Avg_Rating'], marker='o', color='green')
plt.title('Average Rating by Product Line')
plt.xlabel('Product Line')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('average_rating_chart.png')
plt.show()

# 3. Pie Chart - Revenue Distribution by Payment Method
plt.figure(figsize=(8, 8))
plt.pie(revenue_by_payment_method['Total_Revenue'], labels=revenue_by_payment_method['Payment'], autopct='%1.1f%%', startangle=90, colors=['gold', 'lightcoral', 'lightgreen'])
plt.title('Revenue Distribution by Payment Method')
plt.savefig('revenue_distribution_chart.png')
plt.show()

# 4. Horizontal Bar Chart - Top Selling Products
plt.figure(figsize=(10, 6))
bar_color = 'skyblue'
bars = plt.barh(top_selling_products['Product line'], top_selling_products['Total_Quantity'], color=bar_color)
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{bar.get_width():,.0f}', ha='left', va='center')
plt.title('Top Selling Products')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Line')
plt.savefig('top_selling_chart.png')
plt.show()