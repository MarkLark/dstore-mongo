from unittest import TestCase
from pymongo import MongoClient
from dstore import Model, var, mod
from os import environ
from dstore_mongo import MongoStore


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
        if environ.get( "VM" ) is None: self.client = MongoClient( "localhost" )
        else                          : self.client = MongoClient( "192.168.2.165" )

        self.db = self.client.dstore_test
        self.db.authenticate( "test", "test123" )

    def tearDown( self ):
        self.db.Cars.delete_many({})
        self.db.logout()
        self.client.close()

    def add_one( self ):
        self.db.Cars.insert_one( { "id": 1, "manufacturer": "Holden", "make": "Commodore", "year": 2006 } )

    def add_many( self, num_rows ):
        for i in range( num_rows ):
            self.db.Cars.insert_one( { "id": i, "manufacturer": "Holden", "make": "Commodore", "year": 2006 + i } )

    def filter( self, **kwargs ):
        return self.db.Cars.find( dict( **kwargs ) )


class StoreTest( TestCase ):
    models      = [ Car ]
    auto_init   = True
    auto_create = True

    def setUp( self ):
        if self.auto_init:
            self.store = MongoStore( self.models )
            self.store.init_app()

            if environ.get( "VM" ) is None: host = "localhost"
            else                          : host = "192.168.2.165"

            self.store.set_config(dict(
                DSTORE_DB_HOST   = host,
                DSTORE_DB_USER   = "test",
                DSTORE_DB_PASSWD = "test123",
                DSTORE_DB_DB     = "dstore_test"
            ))

            self.store.connect()

    def tearDown( self ):
        if self.auto_create: self.store.destroy_all()
        if self.auto_init:
            self.store.disconnect()
            self.store.destroy_app()
