Welcome To DStore-Mongo
#######################

.. image:: https://img.shields.io/coveralls/MarkLark/dstore-mongo.svg
    :target: https://coveralls.io/github/MarkLark/dstore-mongo?branch=master

.. image:: https://img.shields.io/travis/MarkLark/dstore-mongo/master.svg
    :target: https://travis-ci.org/MarkLark/dstore-mongo

.. image:: https://img.shields.io/pypi/v/dstore-mongo.svg
    :target: https://pypi.python.org/pypi/dstore-mongo

.. image:: https://img.shields.io/pypi/pyversions/dstore-mongo.svg
    :target: https://pypi.python.org/pypi/dstore-mongo

DStore-Mongo is a MongoDB storage layer for DStore.
This allows you to use the same Model descriptions to Create, Read, Update and Delete from a Mongo DataBase.


Installing
==========

DStore-Mongo is available from the PyPi repository.

This means that all you have to do to install DStore-Mongo is run the following in a console:

.. code-block:: console

    $ pip install dstore-mongo

Minimal Example
===============

.. code-block:: python

    from dstore import Model, var, mod
    from dstore_mongo import MongoStore

    class Car( Model ):
        _namespace = "cars.make"
        _vars = [
            var.RowID,
            var.String( "manufacturer", 32, mods = [ mod.NotNull() ] ),
            var.String( "make", 32, mods = [ mod.NotNull() ] ),
            var.Number( "year", mods = [ mod.NotNull(), mod.Min( 1950 ), mod.Max( 2017 ) ] ),
        ]

    # Create the MemoryStore instance, and add Models to it
    store = MongoStore( self.models )
    store.init_app()
    store.set_config({
        "DSTORE_DB_HOST"  : "localhost",
        "DSTORE_DB_USER"  : "username",
        "DSTORE_DB_PASSWD": "password",
        "DSTORE_DB_DB"    : "dstoredb"
    })
    store.connect()
    store.create_all()

    # Destroy all instances and shut down the application
    store.destroy_all()
    store.disconnect()
    store.destroy_app()


Documentation: `ReadTheDocs <https://python-dstore.readthedocs.io/en/latest/storage.html#mongostore>`_

Source Code: `GitHub <https://github.com/MarkLark/dstore-mongo>`_
