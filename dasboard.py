import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
reviews_df = pd.read_csv('order_reviews_dataset.csv')
products_df = pd.read_csv('products_dataset.csv')
orders_df = pd.read_csv('orders_dataset.csv')
order_items_df = pd.read_csv('order_items_dataset.csv')
customers_df=pd.read_csv("customers_dataset.csv")

# Menambahkan sidebar dengan logo dan judul Olist Store
st.sidebar.image('olist.png', width=200)
st.sidebar.title('Olist Store Dashboard')

# EDA - Review Score
st.title("Olist Store Dashboard")
st.header("Review Score")

# Statistik Deskriptif Review Score
stats_review_score = reviews_df['review_score'].describe()
st.write("Statistik Deskriptif Review Score:")
st.write(stats_review_score)

# Tabel untuk keterangan review_score
table_review_score = reviews_df['review_score'].value_counts().reset_index()
table_review_score.columns = ['Review Score', 'Jumlah']
st.write("Tabel Review Score:")
st.write(table_review_score)

# Analisis kepuasan pelanggan saat ini
kepuasan_pelanggan = stats_review_score.loc[['mean', '50%']]
st.write("Rata-rata Review Score (Kepuasan Pelanggan):", kepuasan_pelanggan['mean'])
st.write("Median Review Score:", kepuasan_pelanggan['50%'])

# Visualisasi distribusi review score
st.subheader("Distribusi Review Score")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='review_score', data=reviews_df, palette='viridis', ax=ax)
plt.title('Distribusi Review Score')
plt.xlabel('Review Score')
plt.ylabel('Jumlah')
st.pyplot(fig)

# EDA - Total Penjualan per Kategori Produk
st.header("Total Penjualan per Kategori Produk")

# Menggabungkan data produk dengan data item pesanan
merged_df = pd.merge(products_df, order_items_df, on='product_id')
# Menggabungkan data pesanan dengan data gabungan
merged_df = pd.merge(merged_df, orders_df, on='order_id')

# Menghitung total penjualan per kategori produk
sales_by_category = merged_df.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(5)

# Menampilkan tabel total penjualan per kategori
st.write("Total Penjualan per Kategori Produk:")
st.write(sales_by_category)

# Visualisasi penjualan per kategori
st.subheader("Total Penjualan per Kategori Produk (Top 5)")
fig, ax = plt.subplots(figsize=(10, 6))
sales_by_category.plot(kind='bar', color='skyblue', ax=ax)
plt.title('Total Penjualan per Kategori Produk (Top 5)')
plt.xlabel('Kategori Produk')
plt.ylabel('Total Penjualan')
st.pyplot(fig)

# RFM Analysis
st.header("RFM Analysis")

# Menggabungkan data pesanan dan item pesanan
merged_df = pd.merge(orders_df, order_items_df, on='order_id')

# Menghitung nilai Monetery (total pembelian) per pelanggan
rfm_df = merged_df.groupby('customer_id').agg({
    'order_purchase_timestamp': 'max',  # Recency
    'order_id': 'nunique',  # Frequency
    'price': 'sum'  # Monetary
}).reset_index()

# Menghitung Recency dalam hari dari tanggal terakhir pembelian
rfm_df['recency_days'] = (pd.to_datetime('2023-01-01') - pd.to_datetime(rfm_df['order_purchase_timestamp'])).dt.days

# Ganti nama kolom
rfm_df.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RecencyDays']

# Visualisasi Distribusi Recency, Frequency, Monetary
st.subheader("Distribusi RFM")
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(rfm_df['RecencyDays'], kde=True, color='skyblue', ax=axes[0])
axes[0].set_title('Distribusi Recency')

sns.histplot(rfm_df['Frequency'], kde=True, color='salmon', ax=axes[1])
axes[1].set_title('Distribusi Frequency')

sns.histplot(rfm_df['Monetary'], kde=True, color='lightgreen', ax=axes[2])
axes[2].set_title('Distribusi Monetary')

plt.tight_layout()
st.pyplot(fig)

# Keterangan RFM
st.write("Statistik RFM:")
st.write(rfm_df[['RecencyDays', 'Frequency', 'Monetary']].describe())