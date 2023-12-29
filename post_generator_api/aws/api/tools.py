import requests

from decouple import config

ACCESS_KEY = config("ACCESS_KEY")
SECRET_KEY = config("SECRET_KEY")
AWS_SIGN = config("AWS_SIGN")
TODAY = "20231123"
NOW = "T072853Z"

HOST = "webservices.amazon.es"
URI_PATH = "/paapi5/getitems"
REGION = "eu-west-1"

aws_url = "https://webservices.amazon.es/paapi5/getitems"
payload = {
    "ItemIds": [
        "B0913K5V96"
    ],
    "Resources": [
        "ItemInfo.ContentInfo",
        "ItemInfo.ProductInfo",
        "ItemInfo.TechnicalInfo",
        "ItemInfo.Title"
    ],
    "PartnerTag": "iagentmaster.com-21",
    "PartnerType": "Associates",
    "Marketplace": "www.amazon.es",
    # "Operation": "GetItems"
}
# "Content-Type": "application/json; charset=UTF-8",
headers = {
    "Host": HOST,
    "Content-Type": "application/json; charset=UTF-8",
    "X-Amz-Target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.GetItems",
    "Content-Encoding": "amz-1.0",
    "Authorization": f"AWS4-HMAC-SHA256 Credential={ACCESS_KEY}/{TODAY}/eu-west-1/ProductAdvertisingAPI/aws4_request SignedHeaders=content-encoding;host;x-amz-date;x-amz-target Signature={AWS_SIGN}"
}
r = requests.get(aws_url, data=payload, headers=headers)

r"""
curl "https://webservices.amazon.es/paapi5/getitems"
-H "Host: webservices.amazon.es"
-H "Accept: application/json, text/javascript"
-H "Accept-Language: en-US"
-H "Content-Type: application/json; charset=UTF-8"
-H "X-Amz-Date: 20231122T072853Z"
-H "X-Amz-Target: com.amazon.paapi5.v1.ProductAdvertisingAPIv1.GetItems"
-H "Content-Encoding: amz-1.0"
-H "Authorization: AWS4-HMAC-SHA256 Credential={ACCESS_KEY}/20231122/eu-west-1/ProductAdvertisingAPI/aws4_request SignedHeaders=content-encoding;host;x-amz-date;x-amz-target  Signature={AWS_SIGN}"
-d "{
    \"ItemIds\": [
        \"B0913K5V96\"
    ],
    \"Resources\": [
        \"ItemInfo.ProductInfo\"
    ],
    \"PartnerTag\": \"iagentmaster.com-21\",
    \"PartnerType\": \"Associates\",
    \"Marketplace\": \"www.amazon.es\"
}"
"""

print()
print(r.text)
print(r.status_code)
print(r.content)
print("###########################")
# print(r.json())
