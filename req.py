import requests
res = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:9781461492986")
formatted = res.json()
if formatted['totalItems']>0:
    print(True)
    img=formatted['items'][0]['volumeInfo']['imageLinks']['thumbnail']
    print(img)
    desc=formatted['items'][0]['volumeInfo']['description']
    print(desc)