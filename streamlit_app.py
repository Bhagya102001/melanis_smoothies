# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title(f":cup_with_straw: CUSTOMIZE UR SMOOTHIE :cup_with_straw:")
st.write(
  """CHOOSE THE FRUITS YOU WANT IN YOUR CUSTOM SMOOTHIE! """
)

name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose five ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        st_df = st.dataframe(data = smoothiefroot_response.json(),use_container_width = True)

    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert = st.button('Submit order');

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
    st.write(my_insert_stmt)
    st.stop()
