import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
from vega_datasets import data as vega_data
alt.data_transformers.disable_max_rows()

data = pd.read_csv('./Global Economy Indicators.csv')

# data.info()
data.columns = data.columns.str.strip()
rename_rules = {
    'CountryID': 'country_id',  # 国家的唯一标识符
    'Country': 'country',  # 国家名称
    'Year': 'year',  # 年份
    'AMA exchange rate': 'ama_exchange_rate',  # AMA汇率
    'IMF based exchange rate': 'imf_exchange_rate',  # 基于IMF的汇率
    'Population': 'population',  # 人口数量
    'Currency': 'currency',  # 使用的货币
    'Per capita GNI': 'per_capita_gni',  # 人均国民总收入
    'Agriculture, hunting, forestry, fishing (ISIC A-B)': 'agr_hunt_forest_fish_gva',  # 农业、狩猎、林业、渔业产值
    'Changes in inventories': 'changes_in_inventories',  # 存货变动
    'Construction (ISIC F)': 'construction_gva',  # 建筑业产值
    'Exports of goods and services': 'exports',  # 商品和服务出口总额
    'Final consumption expenditure': 'final_consumption_expenditure',  # 最终消费支出
    'General government final consumption expenditure': 'gov_final_consumption_expenditure',  # 政府最终消费支出
    'Gross capital formation': 'gross_capital_formation',  # 固定资本形成总额
    'Gross fixed capital formation (including Acquisitions less disposals of valuables)': 'gross_fixed_capital_formation',  # 固定资本形成净额
    'Household consumption expenditure (including Non-profit institutions serving households)': 'household_consumption_expenditure',  # 家庭消费支出
    'Imports of goods and services': 'imports',  # 商品和服务进口总额
    'Manufacturing (ISIC D)': 'manufacturing_gva',  # 制造业产值
    'Mining, Manufacturing, Utilities (ISIC C-E)': 'mining_manufacturing_utilities_gva',  # 采矿业、制造业和公共事业产值
    'Other Activities (ISIC J-P)': 'other_activities_gva',  # 其他活动产值
    'Total Value Added': 'total_value_added',  # 总增加值
    'Transport, storage and communication (ISIC I)': 'transport_storage_comm_gva',  # 运输、仓储和通信业产值
    'Wholesale, retail trade, restaurants and hotels (ISIC G-H)': 'wholesale_retail_trade_gva',  # 批发和零售贸易、餐饮和酒店业产值
    'Gross National Income(GNI) in USD': 'gni_usd',  # 以美元计的国民总收入
    'Gross Domestic Product (GDP)': 'gdp'  # 国内生产总值
}

df = data.rename(columns=rename_rules)
df = df.fillna(0)


world_geojson = vega_data.world_110m.url
countries = alt.topo_feature(world_geojson, 'countries')

year = st.slider('Year', min_value=df['year'].min(), max_value=df['year'].max(), step=1)

df['country_id'] = df['country_id'].astype(str)
df['year'] = df['year'].astype(int)
df_small = df[['country_id', 'gdp', 'year']]
# 使用滑动条的值来筛选数据
df_filtered = df_small[df_small['year'] == year]

# 创建地图
base = alt.Chart(countries).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(type='equalEarth')

colored = alt.Chart(countries).mark_geoshape().encode(
    color=alt.condition(
        alt.datum.gdp != 0, 
        alt.Color('gdp:Q', scale=alt.Scale(scheme="blueorange"), title="GDP"),
        alt.value('lightgray')
    )
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_filtered, 'country_id', ['gdp', 'year'])
).project(type='equalEarth')

chart = alt.layer(base, colored).properties(
    width=700,
    height=400,
    title='Global GDP Map by Year'
)
# 在 Streamlit 中显示地图
st.altair_chart(chart)


