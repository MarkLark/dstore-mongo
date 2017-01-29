from unittest import TestCase
from pymongo import MongoClient
from dstore import Model, var, mod


class Car( Model ):
    _namespace = "cars.make"
    _vars = [
        var.RowID,
        var.String( "manufacturer", 32, mods = [ mod.NotNull() ] ),
        var.String( "make", 32, mods = [ mod.NotNull() ] ),
        var.Number( "year", mods = [ mod.NotNull(), mod.Min( 1950 ), mod.Max( 2017 ) ] ),
    ]


class BaseTest( TestCase ):
    def setUp( self ):
        self.client = MongoClient( "192.168.2.165" )
        self.db     = self.client.test
        self.db.authenticate( "test", "test123" )

    def tearDown( self ):
        self.db.Cars.delete_many({})
        self.db.logout()
        self.client.close()
