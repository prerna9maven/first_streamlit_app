import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My first streamlit file")
streamlit.header('🍌🥭 Breakfast Menu')
streamlit.text('🍇 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥝 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥭 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)


#New function for repeateable code block
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # takes the json version and normalize it 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  

# New section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  # adding a text box to enter fruit choice
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # output it on screen as a table
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

  #streamlit.write('The user entered ', fruit_choice)



#  streamlit.text(fruityvice_response.json())






# adding snowflake connector
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("SELECT * from fruit_load_list")

#getting all the rows, not just one
#my_data_row = my_cur.fetchone()
# my_data_rows = my_cur.fetchall()
# streamlit.dataframe(my_data_rows)


# streamlit.text("Hello from Snowflake:")
#making the display a little better
streamlit.header("View our fruit list. Add your favourites!")
#adding snowflake related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
        
#add a button to load the fruit list
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
    
    


# adding another text box to enter fruit to be added- this is first challenge lab of ch 12
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
#streamlit.write('Thanks for adding ', add_my_fruit)

#adding execute statement to check control of flow
#my_cur.execute("insert into fruit_load_list values ('from streamlit') ")


# Allow the end user to add a fruit tothe list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"') ")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
