from pymongo import MongoClient
from os import environ


def main():
    if environ.get( "VM" ) is None: client = MongoClient( "localhost" )
    else                          : client = MongoClient( "192.168.2.165" )
    client.dstore_test.add_user( "test", "test123", roles = [{ "role": "readWrite", "db": "dstore_test" }] )

if __name__ == "__main__": main()
