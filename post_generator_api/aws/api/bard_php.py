import hashlib
import hmac
import json
import requests

from decouple import config


def gmdate(format_string):
    """
    Devuelve una cadena de fecha y hora en formato UTC.

    Args:
        format_string: El formato de la cadena de fecha y hora.

    Returns:
        Una cadena de fecha y hora en formato UTC.
    """

    import datetime

    utcnow = datetime.datetime.utcnow()
    return utcnow.strftime(format_string)


# Replace with your Amazon API keys
access_key = config("ACCESS_KEY")
secret_key = config("SECRET_KEY")

# Define API parameters
service_name = "ProductAdvertisingAPI"
region = "eu-west-1"
host = "webservices.amazon.es"
uri_path = "/paapi5/getitems"
payload = {
    "ItemIds": ["B0913K5V96"],
    "Resources": ["ItemInfo.ContentInfo", "ItemInfo.ProductInfo", "ItemInfo.TechnicalInfo", "ItemInfo.Title"],
    "PartnerTag": "iagentmaster.com-21",
    "PartnerType": "Associates",
    "Marketplace": "www.amazon.es"
}

# Create the canonical request
canonical_request = str(requests.Request(
    method="POST", url="https://" + host + uri_path, headers={}, data=json.dumps(payload)))

# Create the string to sign
string_to_sign = f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

# Calculate the signature
signature = hmac.new(secret_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

# Create the authorization header
authorization_header = f"AWS4-HMAC-SHA256 Credential={access_key}/{region}/{service_name}/aws4_request, SignedHeaders=host;x-amz-date;x-amz-target, Signature={signature}"

# Create the request headers
headers = {
    "host": host,
    "x-amz-date": gmdate("Ymd\THis\Z"),
    "x-amz-target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.GetItems",
    "Authorization": authorization_header,
    "content-encoding": "amz-1.0",
    "content-type": "application/json; charset=utf-8"
}

# Send the request and get the response
response = requests.post("https://" + host + uri_path, headers=headers, data=json.dumps(payload))

# Print the response
print(response.text)
print(response.status_code)
print()
