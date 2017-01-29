from . import BaseTest


class BaseLib( BaseTest ):
    def test_add( self ):
        self.add_one()

    def test_get_all( self ):
        self.add_many(3)
        cars = self.db.Cars.find()
        for car in cars:
            print( car )

    def test_get_one( self ):
        self.add_one()
        car = self.db.Cars.find_one({ "name": "MarkLark" })
        print( car )

    def test_update( self ):
        self.add_many(3)
        self.db.Cars.update_one( {"id": 1}, { "$set": { "name": "Monkey", "age": 26 } })
        car = self.db.Cars.find_one({ "id": 1 })
        print( car )

    def test_count( self ):
        self.add_many(50)
        print( self.db.Cars.count() )

    def test_filter( self ):
        self.add_many(10)
        cars = self.filter( id = 1 )
        for car in cars:
            print( car )
