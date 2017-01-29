from dstore import Store
from pymongo import MongoClient


class MongoStore( Store ):
    def __init__( self, models, name = "DataStore", config = None, config_prefix = "DSTORE_", con_cache = None ):
        super( MongoStore, self ).__init__( models, name, config, config_prefix, con_cache )
        self.db_name = None

    def init_app( self ):
        self.set_config_defaults({
            "DSTORE_DB_HOST"  : "localhost",
            "DSTORE_DB_USER"  : None,
            "DSTORE_DB_PASSWD": None,
            "DSTORE_DB_DB"    : None
        })
        super( MongoStore, self ).init_app()

    def connect( self ):
        self.events.before_connect( self )
        con = MongoClient( self.get_config( "DSTORE_DB_HOST" ) )
        self.db_name = self.get_config( "DSTORE_DB_DB" )
        self.events.after_connect( self )
        return con

    def _get_db( self ):
        con = self.con
        return con[ self.db_name ]

    def _get_collection( self, model ):
        db = self._get_db()
        return db[ model._namespace.replace( ".", "_" )]

    def disconnect( self ):
        self.events.before_disconnect( self )
        self.con.close()
        self._con = None
        self.events.after_disconnect( self )

    def destroy( self, model ):
        col = self._get_collection( model )
        col.delete_many({})
