# THIS IS JUST TO DEMONSRATE HOW FIREBASE READS DATA
from firebase_init import db

db.collection("RegisteredUsers").document("user1").set({
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
})

db.collection("RegisteredUsers").document("user2").set({
    "name": "Bob",
    "email": "bob@example.com",
    "age": 30
})

print("Documents successfully written!")
