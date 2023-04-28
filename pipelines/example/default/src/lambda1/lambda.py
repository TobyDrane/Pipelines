def handler(event, context):
    print('HELLO WORLD FROM LAMBDA 1')

    return {
        "statusCode": 200,
        "body": "Hello World"
    }
