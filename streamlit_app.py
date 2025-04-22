# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json(),use_container_width = True)
# Write directly to the app
st.title(f":cup_with_straw: CUSTOMIZE UR SMOOTHIE :cup_with_straw:")
st.write(
  """CHOOSE THE FRUITS U WANT IN YOUR CUSTOM SMOOTHIE! """
)

name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

#session = get_active_session()

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

    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert = st.button('Submit order');

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
    st.write(my_insert_stmt)
    st.stop()
