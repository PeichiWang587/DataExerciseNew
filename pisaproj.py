import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

import random
r = random.randint(0, 200)
g = random.randint(0, 200)
b = random.randint(0, 200)

st.set_page_config(layout="wide")


# DADA PREP #
pisascore = pd.read_csv('2015pisa.csv')
pisascore = pisascore.drop(columns=['Series Name','2013 [YR2013]', '2014 [YR2014]'])
pisascore.columns = ['country','country_code','series','score']

pisascore = pisascore.dropna(subset = ['score'] )
pisascore = pisascore[pisascore['score'] != '..']

pisascore['score'] = pisascore['score'].astype('float').round(2)

col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.title('PISA Scores by Country 2015')
with col3:
    st.write('')

col1, col2 = st.columns([1, 2])
# FILTERS #
with col1:
    st.header('What is the PISA SCore and why is it important?')
    st.write('''
    Program for International Student Assessment (PISA) tests critical thinking in math, science, and reading to 15 year olds. Since 2000, PISA has involved more than 90 countries and economies and around 3, 000, 000 students worldwide.
    ''')
    st.header('Look into the data:')
    countries = pisascore.sort_values(by="country").country.unique()
    countries_options = st.multiselect(
        'Which countries do you want to look at?',
        countries,
        countries[:12])

    subjects = ['mathematics','reading','science']
    subjects_option = st.selectbox(
        'Please choose a test subject:',
        subjects)
    subjects_dict = {'mathematics':'MAT', 'reading':'REA', 'science':'SCI'}

    subjects_code = subjects_dict[subjects_option]

    genders = ['male','female','both']
    genders_option = st.selectbox(
        'See different gender performance: ',
        genders)
    genders_dict = {'male':'.MA', 'female':'.FE', 'both':''}

    genders_code = genders_dict[genders_option]

    series_code = f'LO.PISA.{subjects_code}{genders_code}'

    pisascore_countries = pisascore[(pisascore['series']==series_code)&(pisascore['country'].isin(countries_options))]


with col2:

    pisascore_all = pisascore[
        (pisascore['series'] == series_code)]
    fig = px.scatter_geo(pisascore_all, locations="country_code", color="country",
                         hover_name="country", size="score")
    st.plotly_chart(fig, use_container_width=True)

    st.bar_chart(pisascore_countries, x='country', y='score')