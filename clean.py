import pandas as pd

# Load the sales data
df = pd.read_csv("data/messy_sales.csv")

# Inspect the dataset
print(df.info())

# Check for missing values
print(df.isnull().sum())


# Data Quality Issues:
# 1. Order ID has 31 missing values.
# 2. Order Date has 25 missing values and is stored as an object instead of datetime.
# 3. Region has 111 missing values.
# 4. Unit Price is stored as an object instead of a numeric data type.
# 5. Customer ID has 362 missing values.

# Exercise 2: Standardize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Print updated column names
print(df.columns.tolist())

# Exercise 3: Handle missing values

# Show the original number of rows and columns
print("Shape before cleaning:", df.shape)

# Fill missing numeric values with the column mean
df["quantity_sold"] = df["quantity_sold"].fillna(df["quantity_sold"].mean())

# Drop rows missing essential identifiers because they cannot be reliably tracked
df = df.dropna(subset=["order_id", "order_date"])

# Check the new shape
print("Shape after cleaning:", df.shape)

# Check for remaining missing values
print(df.isnull().sum())

# Exercise 4: Fix data types

# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Count dates that could not be converted
print("Invalid dates:", df["order_date"].isna().sum())

# Convert unit_price to float after removing dollar signs and commas
df["unit_price"] = (
    df["unit_price"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
).astype(float)

# Convert quantity_sold to integer
df["quantity_sold"] = df["quantity_sold"].astype(int)

# Calculate revenue
df["revenue"] = (df["unit_price"] * df["quantity_sold"]).round(2)

# Display data types
print(df.dtypes)

# Exercise 5: Check for duplicates

# Count duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Print updated shape
print("Shape after removing duplicates:", df.shape)

# Exercise 6: Describe the cleaned data

# Display statistics for the dataset
print(df.describe())

# Data quality observations:
# 1. The maximum quantity sold is 9,999, which is unrealistic
# and appears to be a placeholder or data entry error.
#
# 2. Some revenue values are negative, which may represent
# customer returns or refunds. These are legitimate transactions
# and should be kept.

# Remove rows where quantity_sold is 9,999
# This value is a placeholder, not a real customer order.
df = df[df["quantity_sold"] != 9999]

# Print the updated shape
print("Shape after removing incorrect quantities:", df.shape)

# Exercise 7: Save cleaned data

# Save the cleaned dataset as a CSV file
df.to_csv("data/clean_sales.csv", index=False)

# Reload the CSV file
cleaned_df = pd.read_csv("data/clean_sales.csv")

# Display information about the reloaded data
print(cleaned_df.info())

# Reload the CSV with the date column correctly formatted
cleaned_df = pd.read_csv(
    "data/clean_sales.csv",
    parse_dates=["order_date"]
)

# Check the data types
print(cleaned_df.dtypes)

"""
REFLECTION

1. Which cleaning decision feels most ambiguous?

Flagging missing values feels most ambiguous because
we may not know whether the information was accidentally
left out or is simply unavailable.

2. Would someone understand my cleaning decisions?

Yes. My comments explain why I filled missing numeric
values, removed rows with missing identifiers, and
removed unrealistic quantities.

3. What surprised me about the dataset?

I was surprised by how many missing values and unusual
entries were in the original sales data. Cleaning the
dataset helped make the information more accurate
and useful for analysis.
"""