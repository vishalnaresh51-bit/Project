
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('tips.csv')

st.set_page_config(
    page_title="Tips Dashboard",
    page_icon="💸",
    layout="wide"
)

st.title("Restaurant Analytics Dashboard")


meal_options = ["All"] + list(df['time'].unique())

meal = st.selectbox("Select Meal Type", meal_options)

if meal == "All":
    filtered_df = df
else:
    filtered_df = df[df['time'] == meal]
    

days = ["All"] + list(df["day"].unique())

selected_days = st.multiselect(
    "Select Days",
    options=df["day"].unique()
)

if selected_days:
    filtered_df = filtered_df[filtered_df["day"].isin(selected_days)]
    

bill_range = st.slider("Select a range of total bill", float(df['total_bill'].min()), float(df['total_bill'].max()), (float(df['total_bill'].min()), float(df['total_bill'].max())))
filtered_df = filtered_df[(filtered_df['total_bill'] >= bill_range[0]) & (filtered_df['total_bill'] <= bill_range[1])]



col1, col2, col3 = st.columns(3)
col1.metric("Recorded Bills", int(len(filtered_df)))
col2.metric(" Total Bill", f"${filtered_df['total_bill'].mean():.2f}")

col3.metric("Average Bill", f"{(filtered_df['tip'].mean() / filtered_df['total_bill'].mean()) * 100:.2f}%")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.scatter(
        filtered_df,
        x="total_bill",
        y="tip",
        color="time",
        size="size",
        hover_data=["sex", "day"],
        title="Total Bill vs Tip"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    bar_data = filtered_df.groupby("day", as_index=False)["total_bill"].mean()

    fig2 = px.bar(
        bar_data,
        x="day",
        y="total_bill",
        color="day",
        title="Average Bill by Day",
        labels={
            "day": "Day",
            "total_bill": "Average Bill ($)"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

filtered_df.to_csv("filtered_data.csv", index=False)
styled_df = filtered_df.style.background_gradient(cmap="YlGnBu")
st.dataframe(styled_df, width="stretch")

st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)






