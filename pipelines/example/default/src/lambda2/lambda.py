def handler(event, context):
    print("HELLO WORLD FROM LAMBDA 2")

    return {
        "statusCode": 200,
        "body": "Hello World"
    }
