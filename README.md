# cloudrunapp

To run this app:

1. Create a venv ```python -m venv env```
2. Activate the venv ```env\Scripts\activate```
3. Install dependencies ```pip install -r requirements.txt```
4. Run the app ```python main.py```

Once you run the ```main.py``` your output should look something like this:

```
Setting up selenium

DevTools listening on ws://127.0.0.1:61051/devtools/browser/6a42ded0-68af-4a9e-b9c6-3b7ae789881d
Fetching from url
Fetching tags
{'LOCATION': ['Waverley', 'Bondi Beach', 'Greater Sydney', 'Bondi', 'Waverley'], 'ORGANIZATION': ['Council', "St Vincent's Health", 'Bondi & Districts Chamber of Commerce', 'NSW Health', 'Bronte Coastal Walk', 'Beach Ambassadors', 'Council', 'Waverley Council'], 'PERSON': ['Waverley', 'Waverley Councillors', 'Paula Masselos</strong></p> <p><strong>Mayor of Waverley']}
```

To Deploy The App:
First, login to gcloud:
```bash
[root@test ~] gcloud auth login
or create a service account, download the json key and active:
[root@test ~] gcloud auth activate-service-account --key-file=key.json

```
Second, build and push the docker image to your gcr:
```bash
[root@test ~] gcloud auth configure-docker
[root@test ~] docker build -t gcr.io/<your project id>/selenium-app .
[root@test ~] docker push gcr.io/<your project id>/selenium-app
or you can push to Google Cloud Build to build the image (maybe longer time)
[root@test ~] gcloud builds submit --tag gcr.io/<your project id>/selenium-app
```
Final, create the Cloud Run service for your use:
```
gcloud beta run deploy selenium-ap --image gcr.io/<your project id>/selenium-app --region us-central1 --platform managed --memory 1Gi
```
It will asking some questions if you want to enable the API, or if you allowed unauthenticate call.
Answer yes and waiting some minutes for deployment.
After that it will return the url.
