from async_generator import yield_, async_generator

import asyncio
import pytest
import pymongo

from motor import motor_asyncio


def pytest_addoption(parser):
    parser.addoption(
        "--mongo-port", action="store", default=27017, 
        type=int, help="port to use to connect to mongo"
    )


# the connection gets created just once in the session
@pytest.fixture(scope="session")
def mongo_connection(request):
    port = request.config.getoption("--mongo-port")
    client = pymongo.MongoClient(port=port)
    client.admin.command('ismaster')
    print('Connected to local mongo on port', port)
    return client


# and then for every test we need to make the proper inserts
# and delete everything.
@pytest.fixture
def mongodb(mongo_connection):
    mongo_connection.test.names.insert({'name': 'John Smith'})
    yield mongo_connection
    mongo_connection.test.names.delete_many({})


# need to redefine an event loop
# https://github.com/pytest-dev/pytest-asyncio/issues/68#issuecomment-334083751
@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# need an event_loop or mongo will use its own
# and be different than the one used in the test
# https://github.com/pytest-dev/pytest-asyncio/issues/38#issuecomment-264415067
@pytest.fixture(scope="session")
async def motor_connection(request, event_loop):
    port = request.config.getoption("--mongo-port")
    client = motor_asyncio.AsyncIOMotorClient(port=port, io_loop=event_loop)
    await client.admin.command('ismaster')
    print('Connected to local mongo on port', port)
    return client


# and then for every test we need to make the proper inserts
# and delete everything.
@pytest.fixture
@async_generator
async def async_mongodb(motor_connection):
    await motor_connection.test.names.insert({'name': 'John Smith'})
    await yield_(motor_connection)
    await motor_connection.test.names.delete_many({})
