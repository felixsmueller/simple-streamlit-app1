'''
This file contains the streamlit application to get the top restaurants for a user.
As input we provide the user_id and as output we provide the top 5 restaurants including a score.
'''
import streamlit as st
import json
import urllib.request
import json
import os
import ssl
import pandas as pd

def get_top_restaurant_recommendations(user_id):
    '''
    This function gets for the current user (defined by user_id) the top restaurant recommendations.
    :param user_id: The user id for which we provide a rating. If the user is a new user then use a random very high user id.
    :return:
    '''

    def allowSelfSignedHttps(allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.

    # The parameters for the webrequest. TODO: For new users we may allow to specify other parameters in future.
    data = {
        "Inputs": {
            "WebServiceInput0":
                [
                    {
                        'userID':user_id,
                        'placeID': "-1",
                        'rating': "-1",
                    },
                ],
            "WebServiceInput1":
                [
                    {
                        'userID': "NA",
                        'latitude': "22.139997",
                        'longitude': "-100.978803",
                        'smoker': "false",
                        'drink_level': "abstemious",
                        'dress_preference': "informal",
                        'ambience': "family",
                        'transport': "on foot",
                        'marital_status': "single",
                        'hijos': "independent",
                        'birth_year': "1989",
                        'interest': "variety",
                        'personality': "thrifty-protector",
                        'religion': "none",
                        'activity': "student",
                        'color': "black",
                        'weight': "69",
                        'budget': "medium",
                        'height': "1.77",
                    },
                ],
            "WebServiceInput2":
                [
                    {
                        'placeID': "134999",
                        'latitude': "18.915421",
                        'longitude': "-99.184871",
                        'the_geom_meter': "0101000020957F000088568DE356715AC138C0A525FC464A41",
                        'name': "Kiku Cuernavaca",
                        'address': "Revolucion",
                        'city': "Cuernavaca",
                        'state': "Morelos",
                        'country': "Mexico",
                        'zip': "",
                        'alcohol': "No_Alcohol_Served",
                        'smoking_area': "none",
                        'dress_code': "informal",
                        'accessibility': "no_accessibility",
                        'price': "medium",
                        'url': "kikucuernavaca.com.mx",
                        'Rambience': "familiar",
                        'franchise': "f",
                        'area': "closed",
                        'other_services': "none",
                    },
                ],
        },
        "GlobalParameters": {
        }
    }

    body    = str.encode(json.dumps(data))
    url     = 'http://20.203.142.7:80/api/v1/service/mulx-wide-and-deep-recommender/score'
    api_key = 'xph52KOF2ViNMiFSt2MdjAuPhsvTtDvg'  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    #Do the actual webrequest:
    req = urllib.request.Request(url, body, headers)

    #Try to get the response:
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
    return convert_bytes_to_dict(result)


def convert_bytes_to_dict(bytes_value):
    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON
    my_json = bytes_value.decode('utf8').replace("'", '"')

    # Load the JSON to a Python list & dump it back out as formatted JSON
    res = json.loads(my_json)
    return res

#Print out the title of the app:
st.title("Restaurant Recommender")

#Ask for th euser Id to be predicted
st.header("Enter User ID")
user_id     = st.text_input('User Id', 'U1001', help='Please enter the user id. If it is a new user then use a new very high random user id')

if st.button('Get Recommendation'):
    #Get the prediction form the azure webservice:
    res         = get_top_restaurant_recommendations(user_id)
    #Display the Restaurant ratings including the prediction score (in predicted rating):
    ratings     = res['Results']['WebServiceOutput0'][0]
    restaurants = []
    scores      = []
    for i in range(1,int(len(ratings)/2)+1):
        restaurants.append(ratings['Recommended Item '+str(i)])
        scores.append(round(ratings['Predicted Rating '+str(i)],2))
    #Print the results as table:
    st.table(pd.DataFrame({'Restaurant':restaurants, 'Score':scores}))

