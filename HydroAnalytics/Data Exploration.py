import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
page_title="Data Exploration",
page_icon="📊",
layout="centered",
initial_sidebar_state="expanded")

#The title and text
st.title("Data Exploration 📊 ")
st.write("In this tab we can see the most relevant information that we can extract through the data from the visual analytics.")

sns.set_palette("viridis")

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def plot_features_against_target(df):
    target = 'price'
    features = [x for x in df.columns if x not in ["car", "model", "registration", target]]
    n_cols = 3
    n_rows = (len(features) + 2) // n_cols
    sns.set(font_scale=2)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 6, n_rows * 6))
    axes = axes.flatten()
    
    # Plot each feature against the target variable in the dataframe
    for i, feature in enumerate(features):
        ax = axes[i]
        if df[feature].dtype == 'object' or df[feature].nunique() < 10:
            # For categorical data, use a boxplot or violin plot
            sns.boxplot(x=feature, y=target, data=df, ax=ax, palette="viridis")
        else:
            # For numerical data, use a scatter plot
            sns.scatterplot(x=feature, y=target, data=df, ax=ax, palette="viridis")
        ax.set_title(f'{feature} vs {target}')
        plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    # Hide any unused subplots
    for j in range(i + 1, n_rows * n_cols):
        fig.delaxes(axes[j])
    fig.tight_layout()

    return fig

@st.cache_data
def load_data():
    df =  pd.read_csv("car_ad_display.csv", encoding = "ISO-8859-1", sep=";").drop(columns='Unnamed: 0')

    car_map = shorten_categories(df.car.value_counts(), 10)
    df['car'] = df['car'].map(car_map)

    model_map = shorten_categories(df.model.value_counts(), 10)
    df['model'] = df['model'].map(model_map)

    df = df[df["price"] <= 100000]
    df = df[df["price"] >= 1000]
    df = df[df["mileage"] <= 600]
    df = df[df["engV"] <= 7.5]
    df = df[df["year"] >= 1975]

    return df

df = load_data()

#Basic info:
st.subheader("How does the data look like?")
rows = len(df)
columns =len(df.columns)
st.write("We have:")
st.write(str(rows)+" rows")
st.write(str(columns)+" columns")
st.dataframe(df.head(3))

sns.set(font_scale=0.7)

#Target:
st.subheader("Distribution of the target")
sns.set(font_scale=0.5)
sns.set_palette("viridis")
fig = plt.figure(figsize=(5, 1.5))
sns.kdeplot(x="price", data=df, fill=True)
plt.title("Prices")
st.pyplot(fig)

# 10 Most expensive cars
st.subheader("Top 10 Most expensive cars")
df_priceByCar = df[['car','price']].groupby('car').mean().reset_index()
df_priceByCar = df_priceByCar.sort_values('price', ascending=False).head(10)
fig = plt.figure(figsize=(5, 2))
ax = sns.barplot(df_priceByCar, x="price", y="car", palette= "viridis")
ax.bar_label(ax.containers[0], fontsize=5)
st.pyplot(fig)

#Features distribution vs target:
st.subheader("Distribution of the features against the target")
fig= plot_features_against_target(df)
st.pyplot(fig)

st.set_option('deprecation.showPyplotGlobalUse', False)

#1. Engine Volume Distribution by Car Body Type
st.subheader("Engine Volume Distribution by Car Body Type (Violin Plot)")
plt.figure(figsize=(10, 6))
sns.violinplot(x='body', y='engV', data=df, palette='viridis')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(fontsize=8)
plt.xlabel('Car Body Type', fontsize=10)
plt.ylabel('Engine Volume', fontsize=10)
st.pyplot()

#2. Car Make Distribution Pie Chart
st.subheader("Car Make Distribution Pie Chart")
top_n_brands = 5
top_car_brands = df['car'].value_counts().nlargest(top_n_brands)
colors = sns.color_palette('viridis')[0:5]
plt.figure(figsize=(5, 5))
plt.pie(top_car_brands, labels = top_car_brands.index, colors = colors, autopct='%.0f%%', textprops={'fontsize': 6})
plt.show()
st.pyplot()

#3. Most Common Car Bodies for Top 10 Car Brands
top_n_brands = 10
top_car_brands = df['car'].value_counts().nlargest(top_n_brands).index
df_top_brands = df[df['car'].isin(top_car_brands)]
st.subheader("Most Common Car Bodies for Top 10 Car Brands (Horizontal Bar Chart)")
plt.figure(figsize=(12, 8))
sns.countplot(y='body', hue='car', data=df_top_brands, order=df_top_brands['body'].value_counts().index, palette='viridis')
plt.xlabel('Frequency')
plt.ylabel('Car Body')
plt.legend(title='Car Brand', bbox_to_anchor=(1, 1))
st.pyplot()

#4. Yearly Trends in Car Prices
average_prices_by_year = df.groupby('year')['price'].mean()
st.subheader("Yearly Trends in Car Prices without Slider")
plt.figure(figsize=(7, 4))
plt.plot(average_prices_by_year.index, average_prices_by_year.values, marker='o', color='indigo')
plt.xlabel("Year", fontsize=10)
plt.ylabel("Average Car Price", fontsize=10)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
st.pyplot()

#5. Interactive Violin Plot for Car Prices
st.subheader(f"Violin Plot for Car Prices")
selected_brand = st.selectbox("Select Car Brand", df['car'].unique())
df_selected_brand = df[df['car'] == selected_brand]
plt.figure(figsize=(10, 6))
sns.violinplot(y=df_selected_brand['price'], palette='viridis')
plt.ylabel("Price", fontsize=15)
plt.yticks(fontsize=10)
plt.title(f"Violin Plot for {selected_brand} Car Prices", fontsize=20)
st.pyplot()