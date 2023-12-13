import requests
import json
import hmac
import hashlib
import base64
import datetime

from decouple import config

HOST = "webservices.amazon.es"
URI_PATH = "/paapi5/getitems"
ACCESS_KEY = config("ACCESS_KEY")
SECRET_KEY = config("SECRET_KEY")
REGION = "eu-west-1"

request_payload = {
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
    "Marketplace": "www.amazon.es"
}

headers = {
    "host": HOST,
    "content-type": "application/json; charset=UTF-8",
    "x-amz-target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.GetItems",
    "content-encoding": "amz-1.0"
}


def get_signing_key_a(secret_key, sdate, region, service):
    """
    Genera la clave de firma para la solicitud HTTP.

    Args:
        secret_key: La clave secreta de AWS.
        sdate: La fecha en formato ISO 8601.
        region: La región de AWS.
        service: El servicio de AWS.

    Returns:
        La clave de firma.
    """

    k_date = hashlib.sha256(sdate.encode("utf-8")).digest()
    k_region = hashlib.sha256(k_date + region.encode("utf-8")).digest()
    k_service = hashlib.sha256(k_region + service.encode("utf-8")).digest()
    k_credentials = hashlib.sha256(k_service + "aws4_request".encode("utf-8")).digest()

    return k_credentials


def get_signing_key_b(secret_key, sdate, region, service):
    """
    Genera la clave de firma para el encabezado de autorización.

    Args:
        secret_key: El secreto de la clave de acceso de AWS.
        sdate: La fecha en formato ISO-8601.
        region: La región de AWS.
        service: El servicio de AWS.

    Returns:
        La clave de firma.
    """

    k_date = hmac.new(
        secret_key.encode("utf-8"),
        bytes(sdate, "utf-8"),
        hashlib.sha256,
    ).digest()

    k_region = hmac.new(
        k_date,
        bytes(region, "utf-8"),
        hashlib.sha256,
    ).digest()

    k_service = hmac.new(
        k_region,
        bytes(service, "utf-8"),
        hashlib.sha256,
    ).digest()

    k_credentials = hmac.new(
        k_service,
        bytes("aws4_request", "utf-8"),
        hashlib.sha256,
    ).digest()

    return k_credentials


timestamp = datetime.datetime.utcnow().isoformat()
date = timestamp[:8]
credentials_scope = f"{date}/{REGION}/ProductAdvertisingAPI/aws4_request"

canonical_request = f"POST\n{URI_PATH}\n\nhost:{HOST}\nx-amz-target:com.amazon.paapi5.v1.ProductAdvertisingAPIv1.GetItems\ncontent-encoding:amz-1.0\ncontent-type:application/json; charset=UTF-8\n\n"

signed_headers = ";".join(sorted(headers.keys()))
hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).digest()
hashed_canonical_request_hex = base64.b64encode(hashed_canonical_request).decode("utf-8")

string_to_sign = f"AWS4-HMAC-SHA256\n{timestamp}\n{credentials_scope}\n{hashed_canonical_request_hex}"

signing_key = get_signing_key_b(SECRET_KEY, date, REGION, "ProductAdvertisingAPI")
signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

authorization = f"AWS4-HMAC-SHA256 Credential={ACCESS_KEY}/{credentials_scope}, SignedHeaders={signed_headers}, Signature={signature}"

headers["authorization"] = authorization

request_payload = json.dumps(request_payload)

# response = requests.post("https://" + HOST + URI_PATH, headers=headers, data=request_payload)
response = requests.get("https://" + HOST + URI_PATH, headers=headers, data=request_payload)

if response.status_code == 200:
    json_response = json.loads(response.content)
    print(json_response)
    print("Successfully received response from Product Advertising API.")
else:
    json_response = json.loads(response.content)
    if "Errors" in json_response:
        for error in json_response["Errors"]:
            print(f"Error Code: {error['Code']}, Message: {error['Message']}")
    else:
        print("Error Code: InternalFailure, Message: The request processing has failed because of an unknown error, "
              "exception or failure. Please retry again.")
