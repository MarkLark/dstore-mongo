from dstore import Store
from dstore.Error import InstanceNotFound
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

        db = con[ self.db_name ]
        db.authenticate(
            self.get_config( "DSTORE_DB_USER" ),
            self.get_config( "DSTORE_DB_PASSWD" )
        )

        self.events.after_connect( self )
        return con

    def _get_db( self ):
        con = self.con
        return con[ self.db_name ]

    def _get_collection( self, model ):
        db = self._get_db()
        return db[ model._namespace.replace( ".", "_" )]

    def _num_rows( self, model ):
        col = self._get_collection( model )
        return col.count()

    def disconnect( self ):
        self.events.before_disconnect( self )
        self.con.close()
        self._con = None
        self.events.after_disconnect( self )

    def destroy( self, model ):
        col = self._get_collection( model )
        col.delete_many({})

    def empty( self, model ):
        self.destroy( model )

    def add( self, instance ):
        col = self._get_collection( instance )
        instance.id = self._num_rows( instance )
        col.insert_one( instance.to_dict() )

    def all( self, model ):
        col = self._get_collection( model )
        rtn = []
        for row in col.find({}): rtn.append( model( **row ))
        return rtn

    def update( self, instance ):
        col = self._get_collection( instance )
        col.update_one(
            { "id": instance.id },
            { "$set": instance.to_dict() }
        )

    def get( self, model, row_id ):
        col = self._get_collection( model )
        row = col.find_one({ "id": row_id })

        if row is None: raise InstanceNotFound( self, model( id = row_id ))
        return model( **row )

    def delete( self, instance ):
        col = self._get_collection( instance )
        col.delete_one({ "id": instance.id })

    def filter( self, model, **kwargs ):
        col = self._get_collection( model )

        # Remove kwarg entries with a value of None
        kargs = {}
        for key, val in kwargs.items():
            if val is not None: kargs[ key ] = val

        rtn = []
        for row in col.find( dict( kargs ) ): rtn.append( model( **row ))

        num_rows = len( rtn )
        if num_rows == 0:
            kwargs["id"] = -1
            raise InstanceNotFound( self, model( **kwargs ))

        return rtn
