# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending smoothie orders :cup_with_straw:")
st.write(
    """
    orders that need to filled
    """
)


session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
if my_dataframe:
    editable_df = st.experimental_data_editor(my_dataframe)
    submitted=st.button('Submit')
    if submitted:
        
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
                
            og_dataset.merge(edited_dataset
                         , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success('some one clicked the submit button')
        except:
            st.write('something Wrong')
else:
    st.success('No Pending orders')
        
# ingrediant_list= st.multiselect('choose upto 5 ingredients:', my_dataframe)
# if ingrediant_list:
    
#     ingrediant_string=''
#     for each_fruit in ingrediant_list:
#         ingrediant_string+=each_fruit+' '

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
#             values ('""" + ingrediant_string + """','"""+ name_on_smoothie+"""')"""
#     time_to_insert = st.button('submit order')
#     st.write(my_insert_stmt)
    
#     if time_to_insert:
    
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!'+name_on_smoothie, icon="✅")
