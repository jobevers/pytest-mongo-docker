import pytest

# content of test_sample.py
def test_answer(mongodb):
    mongodb.test.names.insert({'name': 'William Shatner'})
    names = [doc['name'] for doc in mongodb.test.names.find()]
    assert names == ['John Smith', 'William Shatner']


def test_b(mongodb):
    mongodb.test.names.insert({'name': 'Betty Boop'})
    names = [doc['name'] for doc in mongodb.test.names.find()]
    assert names == ['John Smith', 'Betty Boop']


@pytest.mark.asyncio
async def test_some_asyncio_code_a(async_mongodb):
    await async_mongodb.test.names.insert({'name': 'Betty Boop'})
    names = []
    async for doc in async_mongodb.test.names.find():
        names.append(doc['name'])
    assert names == ['John Smith', 'Betty Boop']


@pytest.mark.asyncio
async def test_some_asyncio_code_b(async_mongodb):
    await async_mongodb.test.names.insert({'name': 'Picard'})
    names = []
    async for doc in async_mongodb.test.names.find():
        names.append(doc['name'])
    assert names == ['John Smith', 'Picard']
