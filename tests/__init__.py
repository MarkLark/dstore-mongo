from unittest import TestCase
from pymongo import MongoClient


class BaseTest( TestCase ):
    def setUp( self ):
        self.client = MongoClient( "192.168.2.165" )
        self.db     = self.client.test
        self.db.authenticate( "test", "test123" )

    def tearDown( self ):
        self.db.Cars.delete_many({})
        self.db.logout()
        self.client.close()
