# simple-streamlit-app

This simple streamlit app is used to deplonstrate the Azure restaurant recommender webservice.

## Files:
- aimple_app.py contains the streamlit app
- create_recommender_tables1.ipynb is used to generate the artificial training data
- Procfile and setup.sh are used for launching streamlit on Heroku
- requirements.txt is used to create the conda environment used by this project.


## Run locally

```
git clone https://github.com/professorkazarinoff/simple-streamlit-app.git
cd simple-streamlit-app
conda create --name simple-streamlit-app python=3.9.7​
pip install -r requirements.txt ​
conda activate simple-streamlit-app​
streamlit run simple_app.py
```

## Deploy to Heroku

Create a Heroku account and install the Heroku CLI.

You may need to save all the code in this repo to your own repo. Make sure to ```git add .``` , ```git commit -m "commit message"```, ```git push origin master``` up to GitHub.com

```
cd simple-streamlit-app
git init​
git add .​
git commit -m "Initial commit" ​
git remote add origin https://github.com/<your-account>/simple-streamlit-app.git​
git push origin main​```
