import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import random
r = random.randint(0, 200)
g = random.randint(0, 200)
b = random.randint(0, 200)

st.set_page_config(layout="wide")


schoolData = pd.read_csv('collegedata.csv')
name = schoolData[["INSTNM", "CITY", "STABBR", "ZIP", "CONTROL","COSTT4_A","COSTT4_P","TUITIONFEE_IN","TUITIONFEE_OUT","TUITIONFEE_PROG","BOOKSUPPLY", "NPT4_PUB", "NPT4_PRIV","PFTFAC", "ADM_RATE",'C100_4','MD_EARN_WNE_P6','MD_EARN_WNE_P8','MD_EARN_WNE_P10']]

st.sidebar.header("Choose the area to explore:")
state = st.sidebar.selectbox(
    "Select the state:",
    options=(name.sort_values(by="STABBR").STABBR.unique())
)
df_selection = name.query(
    "STABBR == @state"
)

#change variable name on pie chart
df_selection.loc[df_selection['CONTROL']==1, 'CONTROL'] = "public school"
df_selection.loc[df_selection['CONTROL']==2, 'CONTROL'] = "private school non profit"
df_selection.loc[df_selection['CONTROL']==3, 'CONTROL'] = "private school for profit"

# delete all null data in state data
mask_state_pub = ~df_selection["NPT4_PUB"].isna()
mask_state_priv = ~df_selection["NPT4_PRIV"].isna()

list_state_pub = df_selection[mask_state_pub]
list_state_priv = df_selection[mask_state_priv]


# choose certain city
city = st.sidebar.selectbox(
    "Select the city:",
    options=df_selection.sort_values(by="CITY").CITY.unique()
)
df_selection = df_selection.query(
    "CITY == @city"
)

# delete all null data in city data
mask_city_pub = ~df_selection["NPT4_PUB"].isna()
mask_city_priv = ~df_selection["NPT4_PRIV"].isna()

list_city_pub = df_selection[mask_city_pub]
list_city_priv = df_selection[mask_city_priv]

mask = ~df_selection["TUITIONFEE_IN"].isnull()
frpl = df_selection[mask]

year = st.sidebar.selectbox(
    "Select the year:",
    options=(6,8,10)
)
# df_selection = df_selection.query(
#     "CITY == @city"
# )
x_name = 'C100_4'
y_name = f'MD_EARN_WNE_P{year}'
college = df_selection[["INSTNM", "CITY", "STABBR", x_name, y_name,'CONTROL']]
college['School Type'] = np.select([college['CONTROL']=="public school",college['CONTROL']=="private school non profit",college['CONTROL']=="private school for profit"],
                                   ['Public','Private Nonprofit','Private For-Profit'])
mask_completion = (~college[x_name].isna()) & (~college[y_name].isna())
college = college[mask_completion]
college_city = college[(college['STABBR']==state)&(college['CITY']==city)]

st.markdown("<h1 style='text-align: center; color: rgb({2}, {3}, {4}); font-size: 70px'>{0}, {1}</h1>".format(city, state, r, g, b), unsafe_allow_html=True)

st.write("#")
st.write("#")


# General info
col1, col2, col3 = st.columns([1.3,1.5,1])
tuition_col = df_selection[['INSTNM','COSTT4_A','COSTT4_P']].copy()

#st.write(tuition_col)
tuition_sum = tuition_col.sum(axis=0, skipna = True)
tuition_sum2 = tuition_sum['COSTT4_A']+tuition_sum['COSTT4_P']
school_numbers = len(tuition_col['INSTNM'])

tuition_mean = round(tuition_sum2/school_numbers)

#change variable name on pie chart
df_selection.loc[df_selection['CONTROL']==1, 'CONTROL'] = "public school"
df_selection.loc[df_selection['CONTROL']==2, 'CONTROL'] = "private school non profit"
df_selection.loc[df_selection['CONTROL']==3, 'CONTROL'] = "private school for profit"


st.markdown("""
<style>
.medium-font {
    font-size:70px;
}
.small-font {
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

#st.write(cost_list)
with col1:
    st.markdown('<p class="medium-font">  {0}</p>'.format(school_numbers), unsafe_allow_html=True)
    st.markdown('<p class="small-font">Schools in this city</p>', unsafe_allow_html=True)

with col2:
   av_adm = round(df_selection['ADM_RATE'].sum(axis=0, skipna = True)*100/df_selection['ADM_RATE'].count(), 2)
   st.markdown('<p class="medium-font">{0}%</p>'.format(av_adm), unsafe_allow_html=True)
   st.markdown('<p class="small-font">Average Admission Rate</p>', unsafe_allow_html=True)
with col3:
   st.markdown('<p class="medium-font">${0}</p>'.format(tuition_mean), unsafe_allow_html=True)
   st.markdown('<p class="small-font">Average Tuition</p>', unsafe_allow_html=True)

st.write("#")
st.write("#")


col4, col5 = st.columns(2)
with col4:
    st.subheader("Public vs Private")
    fig = px.pie(df_selection, names='CONTROL')
    fig.update_layout(
            autosize=False,
            width=450,
            height=400,
            margin=dict(
                l=0,
                r=100,
                b=50,
                t=50,
                pad=4
            )
        )
    st.plotly_chart(fig)

with col5:
    faculty_col = df_selection[['INSTNM','PFTFAC']].copy().dropna()

    def fxn(stng):

        # add first letter
        oupt = stng[0]

        # iterate over string
        for i in range(1, len(stng)):
            if stng[i - 1] == ' ':
                # add letter next to space
                oupt += stng[i]

        # uppercase oupt
        oupt = oupt.upper()
        return oupt
    new_column=[]
    for school in faculty_col['INSTNM']:
        new_column.append(fxn(school))
    faculty_col['School Abbreviation'] = new_column


    st.subheader("Full-time faculty percentage ")

    fig3 = px.bar_polar(faculty_col, r="PFTFAC", theta="School Abbreviation",
                       color="PFTFAC", template="seaborn",hover_name="INSTNM",
                        labels={
                            "INSTNM": " ",
                            "PFTFAC": "Percentage"},

                    color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig3.update_layout(
        autosize=False,
        width=500,
        height=400,
        hoverlabel_font_color="#445B51",
        hoverlabel_bgcolor="white",
        margin=dict(
            l=0,
            r=100,
            b=50,
            t=50,
            pad=4
        )
    )

    st.plotly_chart(fig3)






# Public School
st.subheader("Public School: " + city + " city VS " + state + " state")
df_pub = pd.DataFrame()
df_pub["state_name"] = list_state_pub["INSTNM"]
df_pub["state_cost"] = list_state_pub["NPT4_PUB"]
df_pub["city_name"] = list_city_pub["INSTNM"]
df_pub["city_cost"] = list_city_pub["NPT4_PUB"]

# Create the chart
if list_city_pub["INSTNM"].empty:
    left_column, right_column = st.columns([1,3])
    with left_column:
        st.image("https://cdn4.iconfinder.com/data/icons/data-and-network-7/135/57-512.png")
    with right_column:
        st.write("#")
        st.write("#")
        st.subheader("There is no available public school in this area!")
else:
    left_column, right_column = st.columns([1,1])
    with left_column:
        fig_pub_city = px.box(df_pub, y="city_cost", labels={"city_cost":"Cost($)"})
        fig_pub_city.update_yaxes(range=[df_pub["state_cost"].min()-500, df_pub["state_cost"].max()+500])
        fig_pub_city.update_layout(
            autosize=False,
            width=450,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
        )
        fig_pub_city.update_layout(title_text="<b>"+city+"</b>", title_x=0.5)
        st.plotly_chart(fig_pub_city)
    with right_column:
        fig_pub_state = px.box(df_pub, y="state_cost", labels={"state_cost":"Cost($)"})
        fig_pub_state.update_yaxes(range=[df_pub["state_cost"].min()-500, df_pub["state_cost"].max()+500])
        fig_pub_state.update_layout(
            autosize=False,
            width=450,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
        )
        fig_pub_state.update_layout(title_text= "<b>"+state+"</b>", title_x=0.5)
        st.plotly_chart(fig_pub_state)

# Private School
st.subheader("Private School: " + city + " city VS " + state + " state")
df_priv = pd.DataFrame()
df_priv["state_name"] = list_state_priv["INSTNM"]
df_priv["state_cost"] = list_state_priv["NPT4_PRIV"]
df_priv["city_name"] = list_city_priv["INSTNM"]
df_priv["city_cost"] = list_city_priv["NPT4_PRIV"]

# Create the chart
if list_city_priv["INSTNM"].empty:
    left_column, right_column = st.columns([1,3])
    with left_column:
        st.image("https://cdn4.iconfinder.com/data/icons/data-and-network-7/135/57-512.png")
    with right_column:
        st.write("#")
        st.write("#")
        st.subheader("There is no available private school in this area!")
else:
    left_column, right_column = st.columns(2)
    with left_column:
        fig_priv_city = px.box(df_priv, y="city_cost", labels={"city_cost":"Cost($)"})
        fig_priv_city.update_yaxes(range = [df_priv["state_cost"].min()-500, df_priv["state_cost"].max()+500])
        fig_priv_city.update_layout(
            autosize=False,
            width=450,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
        )
        fig_priv_city.update_traces(marker_color='orange')
        fig_priv_city.update_layout(title_text="<b>" + city + "</b>", title_x=0.5)
        st.plotly_chart(fig_priv_city)
    with right_column:
        fig_priv_state = px.box(df_priv, y="state_cost", labels={"state_cost":"Cost($)"})
        fig_priv_state.update_yaxes(range=[df_priv["state_cost"].min()-500, df_priv["state_cost"].max()+500])
        fig_priv_state.update_layout(
            autosize=False,
            width=450,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
        )
        fig_priv_state.update_traces(marker_color='orange')
        fig_priv_state.update_layout(title_text="<b>" + state + "</b>", title_x=0.5)
        st.plotly_chart(fig_priv_state)

st.subheader("Graduation Rate v.s Median Income")
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
    width=950
)
fig.update_traces(
    marker = dict(size=10, symbol='star-diamond')
)
st.write(fig)

# Collage Graduates Earnings
st.subheader("Collage Graduates Earnings")
college_city = college_city.rename(
    columns={'INSTNM': 'Collage Name', 'STABBR': 'State', 'C100_4': 'Graduation Rate',
            y_name: f'Income after {year} years'}
)
college_city = college_city.drop(columns=['CONTROL', 'CITY', 'State'])
college_city = college_city.reset_index(drop=True)
college_city.index += 1
st.dataframe(college_city, use_container_width=True)



