import sec_conf, hashlib
from pymongo import MongoClient
from datetime import datetime, timedelta
from flask import session


class Session:
    def __init__(self, headers):
        self.http_headers = headers
        self.db_username = sec_conf.dbUsername
        self.db_pass = sec_conf.dbPassword
        self.mongo_client = MongoClient('127.0.0.1')
        self.sessions_db = self.mongo_client.sessions_db

    def insert_one_in_sessions(self, data):
        self.sessions_db.sessions_coll.insert_one(data)

    def validate_record_exists(self, query):
        print(f"self.sessions_db.sessions_coll.find({query})")
        if self.sessions_db.sessions_coll.count_documents(query) > 0:
            print('Record found')
            return True
        else:
            print('Record not found')
            return None

    def extend_timeout(self):
        self.sessions_db.sessions_coll.update_one({"username": self.http_headers['username']},
                                                  {"$set": {
                                                      "session_timeout_datetime": str(
                                                          datetime.now() + timedelta(minutes=15))
                                                  }})

    def validate_timeout(self):
        for document in self.sessions_db.sessions_coll.find({"username": self.http_headers["username"]}):
            session_expire_time = datetime.strptime(document['session_timeout_datetime'], '%Y-%m-%d %H:%M:%S.%f')
            if datetime.now() > session_expire_time:
                self.sessions_db.sessions_coll.remove({"username": self.http_headers["username"]})
                return False
            else:
                self.extend_timeout()
                return True

    def open_session(self):
        session_headers = {"username": self.http_headers['username'], "password": self.http_headers['password'],
                           "ipaddress": self.http_headers['ipaddress'], "user_agent": self.http_headers['user_agent'],
                           "session_timeout_datetime": str(datetime.now())}
        self.insert_one_in_sessions(session_headers)
        self.validate_timeout()

    def create_session_hash(self):
        hash = hashlib.md5()
        encoded_value = f"{self.http_headers['username']}{self.http_headers['password']}".encode('utf-8')
        hash.update(encoded_value)
        return hash.hexdigest()


session_start_headers = {"username": "TestUsername", "password": "Jw!12345", "ipaddress": "1.1.1.1",
                         "user_agent": "Mozilla", "session_timeout_datetime": datetime.now()}

new_session = Session(session_start_headers)
print(new_session.create_session_hash())
# new_session.open_session()
# new_session.validate_timeout()
