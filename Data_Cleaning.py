import pandas as pd

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/netflix_titles.csv")

print("Original dataset shape:", df.shape)


# ==========================================
# 2. REMOVE DUPLICATE RECORDS
# ==========================================

duplicates = df.duplicated().sum()
print("Duplicate records found:", duplicates)

df = df.drop_duplicates()


# ==========================================
# 3. HANDLE MISSING VALUES
# ==========================================

# Fill missing text values with "Unknown"
text_columns = ["director", "cast", "country"]

for column in text_columns:
    df[column] = df[column].fillna("Unknown")

# Fill missing rating with the most common rating
df["rating"] = df["rating"].fillna(df["rating"].mode()[0])

# Fill missing duration with "Unknown"
df["duration"] = df["duration"].fillna("Unknown")


# ==========================================
# 4. CLEAN DATE COLUMN
# ==========================================

# Convert date_added to datetime
df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

# Remove records where date_added is missing
df = df.dropna(subset=["date_added"])


# ==========================================
# 5. CLEAN TEXT COLUMNS
# ==========================================

text_columns = [
    "show_id",
    "type",
    "title",
    "director",
    "cast",
    "country",
    "rating",
    "duration",
    "listed_in",
    "description"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()


# ==========================================
# 6. CREATE NUMERIC DURATION COLUMN
# ==========================================

df["duration_value"] = pd.to_numeric(
    df["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

df["duration_type"] = df["duration"].str.extract(
    r"(min|Season|Seasons)"
)[0]

df["duration_type"] = df["duration_type"].fillna("Unknown")


# ==========================================
# 7. CHECK CLEANED DATA
# ==========================================

print("\n===== CLEANED DATASET INFORMATION =====")
print(df.info())

print("\n===== MISSING VALUES AFTER CLEANING =====")
print(df.isnull().sum())

print("\n===== CLEANED DATASET SHAPE =====")
print(df.shape)


# ==========================================
# 8. SAVE CLEANED DATASET
# ==========================================

df.to_csv(
    "data/cleaned_netflix_titles.csv",
    index=False
)

print("\n==========================================")
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("Cleaned dataset saved as:")
print("data/cleaned_netflix_titles.csv")
print("==========================================")