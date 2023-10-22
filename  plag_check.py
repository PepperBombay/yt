import json
import nltk

def lambda_handler(event, context):

  nltk.data.path.append("/opt/python/nltk_data") # this one line fixed it!

  text = "Hello, how are you doing?"
  #tokens = word_tokenize(text)
  print(text)

  return {
    "statusCode": 200,
    "body": json.dumps({
        "message": "inbound",
        "text":text,
             
    }),
  }