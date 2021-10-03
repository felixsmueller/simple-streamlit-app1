# simple-streamlit-app

A simple web app example built with Python and Streamlit

## Run locally

```
git clone https://github.com/professorkazarinoff/simple-streamlit-app.git
cd simple-streamlit-app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run simple_app.py
```

## Deploy to Heroku

Create a Heroku account and install the Heroku CLI.

You may need to save all the code in this repo to your own repo. Make sure to ```git add .``` , ```git commit -m "commit message"```, ```git push origin master``` up to GitHub.com

```
heroku login
heroku create
git push heroku master
heroku open
```
