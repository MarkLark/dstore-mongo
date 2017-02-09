from nose.tools import eq_
from dstore.Error import InstanceNotFound
from . import StoreTest, Car


class CRUD( StoreTest ):
    def test_add( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()

    def test_all( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2009 ).add()

        for car in Car.all():
            print( "\t%s" % car )

    def test_all_dict( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2009 ).add()

        for car in Car.all( to_dict = True ):
            print( "\t%s" % car )

    def test_update( self ):
        car = Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()

        car.year = 2016
        car.update()

    def test_get( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2009 ).add()

        car = Car.get(3)

        eq_( car.manufacturer, "Holden",    "Car.manufacturer != 'Holden'"    )
        eq_( car.make,         "Commodore", "Car.make != 'Commodore'"         )
        eq_( car.year,         2008,        "Car.year  %d != 2008" % car.year )

    def test_get_none( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()

        self.assertRaises( InstanceNotFound, Car.get, 3 )

    def test_delete( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        car = Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()

        car.delete()

    def test_filter( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Rodeo",     year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Colorado",  year = 2009 ).add()

        cars = Car.filter( make = "Commodore" )

        num_cars = len( cars )
        eq_( num_cars, 3, "Number of cars %d != 3" % num_cars )

    def test_filter_1( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Rodeo",     year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Colorado",  year = 2009 ).add()

        car = Car.filter( make = "Rodeo" )[0]

        eq_( isinstance( car, Car ), True, "Didn't return a single instance" )

    def test_filter_none( self ):
        Car( manufacturer = "Holden", make = "Commodore", year = 2005 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2006 ).add()
        Car( manufacturer = "Holden", make = "Commodore", year = 2007 ).add()
        Car( manufacturer = "Holden", make = "Rodeo",     year = 2008 ).add()
        Car( manufacturer = "Holden", make = "Colorado",  year = 2009 ).add()

        self.assertRaises( InstanceNotFound, Car.filter, make = "Gummy" )
