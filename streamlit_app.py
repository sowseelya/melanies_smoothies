# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched
import requests
# Write directly to the app
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom smoothie!
    """
)


name_on_smoothie = st.text_input('Name on smoothie')
st.write('The name on the smoothie is:', name_on_smoothie)

cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))

pd_df=my_dataframe.to_pandas()

ingrediant_list= st.multiselect('choose upto 5 ingredients:', my_dataframe,max_selections=5)
if ingrediant_list:
    
    ingrediant_string=''
    for each_fruit in ingrediant_list:
        ingrediant_string+=each_fruit+' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME']== each_fruit,'SEARCH_ON'].iloc[0]
        st.write('The search value of fruit is' , search_on)
        st.subheader(each_fruit + 'Nutritional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit )

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingrediant_string + """','"""+ name_on_smoothie+"""')"""
    time_to_insert = st.button('submit order')
    st.write(my_insert_stmt)
    
    if time_to_insert:
    
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+name_on_smoothie, icon="✅")
