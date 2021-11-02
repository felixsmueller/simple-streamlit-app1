'''
This file contains the streamlit application to get the top restaurants for a user.
As input we provide the user_id and as output we provide the top 5 restaurants including a score.
If you enter a new user by specifying a user_id which was not used for training then you can specify in addition the cuisine preference of the user.
The recommender will then proposethe top restaurants for this cuisine.
The recommender is based on artificial data for demonstration purposes. The training data is contained in the 'data' folder of this project.
There are only 10 Users and 20 restaurants. The users and restaurants having ODD ids prefer italian food or are Italian restaurants.
The users and restaurants having EVEN ids prefer French food or are French restaurants.
'''

import streamlit as st
import json
import urllib.request
import json
import os
import ssl
import pandas as pd

def get_top_restaurant_recommendations(user_id, user_preference):
    '''
    This function gets for the current user (defined by user_id) the top restaurant recommendations.
    For NEW users (whose user-id was not used for training) we can pass their cuisine preference.
    Note that the recommender system seems to learn this preference immediately.
    :param user_id: The user id for which we provide a rating. If the user is a new user then use a random very high user id.
    :param user_preference: The user cuisine preference such as 'Italian' or 'French'.
    :return: Returns the predictions as a dictionary.
    '''

    def allowSelfSignedHttps(allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.

    # The parameters for the webrequest.
    # If you want to add another recommender then exchange this part of the code until the mark '***' below. to get the code go in Azure to the endpoint and there to the 'consume' tab. Then choose 'python' and extract the relevant parts only.
    # In addition you have to adapt the hardcoded parameters to use the parameters user_id and user_preference.
    data = {
        "Inputs": {
            "WebServiceInput0":
                [
                    {
                        'restaurant': "1",
                        'style': "Italian",
                        'name': "Pizeria_1",
                    },
                ],
            "WebServiceInput1":
                [
                    {
                        'user': user_id,
                        'restaurant': "-1",
                        'rating': "-1",
                    },
                ],
            "WebServiceInput2":
                [
                    {
                        'user': user_id,
                        'style': user_preference,
                        'name': "",
                    },
                ],
        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'http://20.203.142.7:80/api/v1/service/mulx-wide-and-deep-recom-artif1/score'
    api_key = 'Do1PgNTBMdbwAetoVxT4MPWS0kjxBQWO'  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    # '***' The above code is extracted from the Endpoint/consume/python.

    #Do the actual webrequest:
    req = urllib.request.Request(url, body, headers)

    #Try to get the response:
    try:
        result = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError as error:
        print("The webservice request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
    return convert_bytes_to_dict(result)


def convert_bytes_to_dict(bytes_value):
    '''Decode UTF-8 bytes to Unicode, and convert single quotes
    to double quotes to make it valid JSON
    :param  bytes_value the byte values to be converted into a dicttionary.
    :return Returns the converted byte values as a dictionary.
    '''

    my_json = bytes_value.decode('utf8').replace("'", '"')

    # Load the JSON to a Python list & dump it back out as formatted JSON
    res = json.loads(my_json)
    return res

def get_restaurant_name(rest_id):
    '''
    This function takes a restaurant_id and looks up the restaurant name form the training data. This is only used for convenience to make the GUI a bit more handy.
    :param rest_id: The restaurant id to be looked up.
    :return: The restaurant name.
    '''
    try:
        return st.session_state.restaurants[st.session_state.restaurants.restaurant == int(rest_id)]['name'].values[0]
    except Exception as ex:
        st.text(ex)
    return ''

def get_user_details(user_id):
    '''
    This function can be used to look up the user details for a given user_id. The lookup uses the training data files. This is only used for convenience to make the GUI a bit more handy.
    :param user_id:
    :return: The user details as a DataFrame.
    '''
    try:
        return st.session_state.users[st.session_state.users.user == int(user_id)]
    except:
        pass
    return pd.DataFrame()

#Read in the restaurant and user data once and only once per Session:
if 'users' not in st.session_state:
    st.session_state.users = pd.read_csv('./data/mulx_user_artificial_1.csv', sep=';')
if 'restaurants' not in st.session_state:
    st.session_state.restaurants = pd.read_csv('./data/mulx_restaurant_artificial_1.csv', sep=';')

#Print out the title of the app:
st.title("Restaurant Recommender")

#Ask for the user Id to be predicted
st.header("Enter User ID")
user_id     = st.text_input('User Id', '1', help='Please enter the user id. If it is a new user then use a new high random number as user id.')
st.table(get_user_details(user_id))

#Ask for the user food preference (relevant for new users)
st.header("Enter User Cuisine Preference")
user_preference = st.radio(label='', options=('Any', 'Italian', 'French'), help='For NEW users please enter the user cuisine preference.')

#Add a button to get the recommendation:
if st.button('Get Recommendation'):
    #Get the prediction form the azure webservice:
    res         = get_top_restaurant_recommendations(user_id, user_preference)
    #Display the Restaurant ratings including the prediction score (in predicted rating):
    ratings     = res['Results']['WebServiceOutput0'][0]
    rest_ids    = []
    rest_name   = []
    scores      = []
    for i in range(1,int(len(ratings)/2)+1):
        rest_id = ratings['Recommended Item ' + str(i)]
        rest_ids.append(rest_id)
        rest_name.append(get_restaurant_name(rest_id))
        scores.append(round(ratings['Predicted Rating '+str(i)],2))
    #Print the results as table:
    st.header("Recommendations")
    st.table(pd.DataFrame({'Restaurant Id':rest_ids, 'Restaurant Name': rest_name, 'Recommender Score':scores}))