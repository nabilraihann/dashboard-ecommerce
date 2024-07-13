import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from format_currency import format_currency
from matplotlib.ticker import ScalarFormatter


def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        'order_id': 'nunique',
        'price': 'sum'
    })
    # monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
    monthly_orders_df.index = monthly_orders_df.index.strftime(
        '%b-%Y')  # mengubah format order date menjadi nama bulan
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)

    return monthly_orders_df


def create_day_of_purchase_df(df):
    day_of_purchase_df = df.groupby(by='day_of_purchase').agg({
        'order_id': 'nunique'
    })
    day_of_purchase_df = day_of_purchase_df.reset_index()
    day_of_purchase_df.rename(columns={
        "order_id": "count_of_order"
    }, inplace=True)
    day_of_purchase_df = day_of_purchase_df.sort_values(
        by='count_of_order', ascending=False)
    return day_of_purchase_df


def create_delivery_status_df(df):
    delivery_status_df = df.groupby(
        by='delivery_status').order_id.nunique().reset_index()
    delivery_status_df.rename(columns={
        "order_id": "order"
    }, inplace=True)

    return delivery_status_df


def create_city_df(df):
    city_df = df.groupby(by='customer_city').agg({
        'price': 'sum',
        'order_id': 'nunique'
    })
    city_df = city_df.reset_index()
    city_df = city_df.rename(columns={
        'price': 'revenue',
        'order_id': 'order_count'
    })
    city_df = city_df.sort_values(
        by=['revenue', 'order_count'], ascending=False)
    city_df = city_df.head(10)

    return city_df


def create_category_df(df):
    category_df = df.groupby(by='product_category_name_english').agg({
        'order_id': 'nunique',
        'price': 'sum'
    })
    category_df = category_df.reset_index()
    category_df = category_df.rename(columns={
        'product_category_name_english': 'category_name',
        'order_id': 'order_count',
        'price': 'revenue'
    })
    category_df = category_df.sort_values(by='revenue', ascending=False)
    category_df = category_df.head(10)

    return category_df


def create_weight_category_df(df):
    weight_category_df = df.groupby(by='weight_group').agg({
        'order_id': 'count'
    })
    weight_category_df = weight_category_df.reset_index()
    weight_category_df = weight_category_df.rename(columns={
        'order_id': 'order_count'
    })

    return weight_category_df

def create_map_df(df):
    map_df = all_df.groupby(by='customer_city').agg({
    'geolocation_lng': 'max',
    'geolocation_lat': 'max',
    'order_id': 'count',
    'price': 'sum'
    })

    map_df = map_df.reset_index()
    map_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue",
        'geolocation_lng': 'longitude',
        'geolocation_lat': 'latitude',
    }, inplace=True)
    map_df = map_df.dropna()
    
    return map_df


all_df = pd.read_csv("all_data.csv")


all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
all_df['order_purchase_timestamp'] = pd.to_datetime(
    all_df['order_purchase_timestamp'])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://www.linkedin.com/in/nabilmraihan">@nabilmraihan</a></h6>',
            unsafe_allow_html=True,
        )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) &
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

weight_category_df = create_weight_category_df(main_df)
category_df = create_category_df(main_df)
city_df = create_city_df(main_df)
delivery_status_df = create_delivery_status_df(main_df)
day_of_purchase_df = create_day_of_purchase_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
map_df = create_map_df(main_df)


st.header(':shopping_bags: E-Commerce Dashboard')

col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total Orders", value=f"📦{total_orders}")

with col2:
    total_revenue = format_currency(monthly_orders_df.revenue.sum(), 'pt_BR')
    st.metric(label='Total Revenue', value=f"💰 {total_revenue} $")

with col3:
    average_delivery = round(all_df.delivery_time.mean())
    st.metric("AVG Delivery Time", value=f"🏣{average_delivery} Day")

st.subheader("📈 Orders and Revenue Trend 2016-2018")

# Membuat figure dan axis
fig, ax1 = plt.subplots(figsize=(10, 5))

# Menggambar grafik pertama dengan order count
ax1.plot(monthly_orders_df["order_purchase_timestamp"],
         monthly_orders_df["order_count"], linewidth=2, marker='o', color='dodgerblue')
ax1.set_xlabel('Order Purchase Month')
ax1.set_ylabel('Order Count', color='dodgerblue')
ax1.tick_params(axis='y', labelcolor='dodgerblue')

# Menonaktifkan notasi ilmiah pada sumbu y1
ax1.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax1.ticklabel_format(style='plain', axis='y')
plt.xticks(fontsize=10, rotation=45, ha='right')

# Membuat sumbu y kedua
ax2 = ax1.twinx()
ax2.plot(monthly_orders_df["order_purchase_timestamp"],
         monthly_orders_df["revenue"], linestyle="-", marker='s', linewidth=2, color='green')
ax2.set_ylabel('Revenue', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Menonaktifkan notasi ilmiah pada sumbu y2
ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax2.ticklabel_format(style='plain', axis='y')

# Menambahkan judul
# plt.title("Orders and Revenue Trend 2016-2018", loc="center", fontsize=16)

st.pyplot(fig)


def set_custom_palette(series, max_color='turquoise', other_color='lightgrey'):
    max_val = series.max()
    pal = []

    for item in series:
        if item == max_val:
            pal.append(max_color)
        else:
            pal.append(other_color)
    return pal
  
col1, col2 = st.columns([4,3])
  
with col1:
  st.subheader("📈 Top days orders created")

  fig = plt.figure(figsize=(10, 6))
  plot = sns.barplot(x='day_of_purchase', y='count_of_order', data=day_of_purchase_df,
                    palette=set_custom_palette(day_of_purchase_df['count_of_order']))

  for i in plot .containers:
      plot .bar_label(i,)

  # plot .set_title('Top days most orders created')

  st.pyplot(fig)
  
with col2:
  st.subheader("🎯 Delivery Status Percentage")
  fig, ax = plt.subplots()
  ax.pie(delivery_status_df['order'], labels=delivery_status_df['delivery_status'],
        autopct='%1.1f%%', colors=['lightgrey', 'turquoise'])
  st.pyplot(fig)
  
  
col1, col2, col3 = st.columns([2,2,2])

with col1:
    st.subheader("🏢 Top 10 cities by orders")
    fig, ax = plt.subplots()

    ax.bar(city_df['customer_city'], city_df['order_count'], color='limegreen')
    # ax.set_title("Top 10 cities by order")
    plt.xticks(fontsize=10, rotation=45, ha='right')
    st.pyplot(fig)

with col2:
    st.subheader("🛒 Top 10 categories by revenue")
    fig, ax = plt.subplots()

    ax.bar(category_df['category_name'],
        category_df['revenue'], color='deepskyblue')
    # ax.set_title("Top 10 categories by revenue")
    plt.xticks(fontsize=10, rotation=45, ha='right')
    st.pyplot(fig)

with col3:
    st.subheader("⚖ Weight category by order")
    fig, ax = plt.subplots()

    ax.bar(weight_category_df['weight_group'],
        weight_category_df['order_count'], color='yellowgreen')
    # ax.set_title("Weight category by order")
    for i in ax.containers:
        ax.bar_label(i,)
    plt.xticks(fontsize=10, rotation=45, ha='right')
    st.pyplot(fig)
    

st.subheader("🗺 Map chart by revenue")
st.map(data=map_df,latitude='latitude',longitude='longitude',size='revenue')
