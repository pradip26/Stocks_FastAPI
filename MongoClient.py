import pymongo
import configparser
import datetime


class Mongo:
    url = ""
    database = ""
    appLogFile = ""
    fileHandler = ""
    connection = ""

    # Define the mongo connections
    def __init__(self):
        mongoConfig = configparser.ConfigParser()
        mongoConfig.read('config.ini')
        self.url = "mongodb://" + mongoConfig['Mongo']['host'] + ":" + mongoConfig['Mongo']['port'] + "/"
        self.appLogFile = mongoConfig['ErrorLog']['app']
        self.fileHandler = open(self.appLogFile, "a")
        self.connection = self.getMongoConnection()
        self.database = self.connection[mongoConfig['Mongo']['database']]

    # get mongo DB connection
    def getMongoConnection(self):
        try:
            client = pymongo.MongoClient(self.url)
            return client
        except:
            error = " Connection : " + self.url + " database : " + self.database + " Error : Connection not established"
            self.writeLogs(error)

    # insert single record in collecton
    def insertRecord(self, collection, data):
        try:
            col = self.database[collection]
            col.insert_one(data)
            return True
        except:
            error = ' Unable to insert record'
            self.writeLogs(error)

    # insert bulk records in collections
    def bulkInsertRecord(self, collection, data):
        try:
            col = self.database[collection]
            col.insert_many(data)
            return True
        except:
            error = ' Unable to insert records '
            self.writeLogs(error)

    # update records in collection based on condition and default it is upsert true
    def updateRecord(self, collection, condition, updateData, upsertFlag=True):
        try:
            col = self.database[collection]
            col.update_one(condition, {'$set': updateData}, upsertFlag)
            return True
        except:
            error = ' Unable to update records , filter: ' + condition + ' Data : ' + updateData
            self.writeLogs(error)

    # get records from collection based on the condition
    def getRecords(self, collection, condition=None, fields=None, sortFields=None,limitValue=None):
        if condition is None:
            condition = {}
        try:
            col = self.database[collection]

            if sortFields is not None and limitValue is not None:
                data = col.find(condition, fields).sort(sortFields).limit(limitValue)
            elif limitValue is not None:
                data = col.find(condition, fields).limit(limitValue)
            elif sortFields is not None:
                data = col.find(condition, fields).sort(sortFields)
            else:
                data = col.find(condition, fields)

            return data
        except:
            error = ' Unable to fetch records, Filter : ' + condition + ' Collection : ' + collection
            self.writeLogs(error)

    # delete the records based on condition and want to delete all then pass condition as none
    def deleteRecord(self, collection, condition=None):
        if condition is None:
            condition = {}
        try:
            col = self.database[collection]
            deletedCount = col.delete_many(condition)
            return deletedCount
        except:
            error = ' Unable to delete records, Filter : ' + condition + ' Collection : ' + collection
            self.writeLogs(error)

    # get the record count from collection based on condition
    def getCount(self, collection, condition=None):
        if condition is None:
            condition = {}
        try:
            col = self.database[collection]
            docCount = col.count_documents(condition)
            return docCount
        except:
            error = ' Unable to get document count, Filter : ' + condition + ' Collection : ' + collection
            self.writeLogs(error)

    def writeLogs(self, errorString):
        dt = str(datetime.datetime.now())
        log = '\n ' + dt + " " + errorString
        self.fileHandler.write(log)
        return True

    def __del__(self):
        self.fileHandler.close()
        self.connection.close()
