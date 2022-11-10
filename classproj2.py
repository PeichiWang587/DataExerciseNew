import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

df = pd.read_csv('collegedata.csv')

st.set_page_config(layout='wide')
col1, col2 = st.columns([1, 1])


with st.sidebar:
    state = st.selectbox(
        'Select a State:',
        ('AL', 'AK', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'),
        index=32)

    city = st.text_input(
        "Which city?   (*Tip: Please make sure the city name follows the format of 'Aaa Aaa', such as 'New York')",
        'New York')

year = st.selectbox(
    'Filter **YEARS AFTER ENROLLMENT** to see different income level:', (6, 8, 10))
x_name = 'C100_4'
y_name = f'MD_EARN_WNE_P{year}'
college = df[["INSTNM", "CITY", "STABBR", x_name, y_name,'CONTROL']]
college['School Type'] = np.select([college['CONTROL']==1,college['CONTROL']==2,college['CONTROL']==3],
                                   ['Public','Private Nonprofit','Private For-Profit'])
mask_completion = (~college[x_name].isna()) & (~college[y_name].isna())
college = college[mask_completion]
college_city = college[(college['STABBR']==state)&(college['CITY']==city)]


with col1:
    st.title("Graduation Rate v.s Median Income")
    fig = px.scatter(
        college_city,
        x=x_name,
        y=y_name,
        color='School Type',
        hover_name='INSTNM',
        labels={'INSTNM': 'College',
                x_name: 'Graduation Rate',
                y_name: 'Median Income'}
    )
    fig.update_layout(
        xaxis_title='Graduation Rate',
        yaxis_title='Median Annual Income',
    )
    fig.update_traces(
        marker = dict(size=10, symbol='star-diamond')
    )

    st.write(fig)

with col2:
    st.title("Collage Graduates Earnings")
    college_city = college_city.rename(
        columns={'INSTNM': 'Collage Name', 'STABBR': 'State', 'C100_4': 'Graduation Rate',
                 y_name: f'Income after {year} years of enrollment'}
    )
    college_city = college_city.drop(columns=['CONTROL', 'CITY', 'State', 'Graduation Rate', 'School Type'])
    college_city = college_city.reset_index(drop=True)
    college_city.index += 1
    college_city
