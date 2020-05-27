# pyrebase documentation : https://github.com/thisbejim/Pyrebase
# firebase realtime database documentation: https://firebase.google.com/docs/database/admin/save-data#section-ways-to-save
'''
requirements: 
gcloud==0.17.0
googleapis-common-protos==1.51.0
httplib2==0.18.1
jws==0.1.3
oauth2client==3.0.0
protobuf==3.12.1
pyasn1==0.4.8
pyasn1-modules==0.2.8
pycryptodome==3.4.3
Pyrebase==3.0.27
python-jwt==2.0.1
requests==2.11.1
requests-toolbelt==0.7.0
rsa==4.0
'''
# from libdw import pyrebase        #this way of importing don't need "storageBucket"
import pyrebase

projectid = "replaceMEEE"
dburl = "https://" + projectid + ".firebaseio.com"
authdomain = projectid + ".firebaseapp.com"
apikey = "replaceMEEE"
email = "replaceMEEE"
password = "replaceMEEE"

config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
    "storageBucket": projectid + ".appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()

root = db.child("/").get(user['idToken'])
print(root.key(), root.val())

age = db.child("age").get(user['idToken'])
print(age.key(), age.val())

facts = db.child("facts_about_me").get(user['idToken'])
print(facts.key(), facts.val())


facts = db.child("facts_about_me").child("1").get(user['idToken'])
print(facts.key(), facts.val())

name = db.child("name").get(user['idToken'])
print(name.key(), name.val())

# to create a new node with our own key
db.child("pie").set(3.14, user['idToken'])

# to add to existing child
db.child("feedback").update({'time_diff_diff':{'username':'user_feedback'}}, user['idToken'])

# to update existing entry
db.child("pie").set(3.1415, user['idToken'])
db.child("love_dw").set({True:123}, user['idToken'])