import base64
import httpx
import asyncio

class PayPy:
    def __init__(self, client_id, client_secret, vendor_given_names, vendor_last_names, vendor_email, currency_code="GBP", dev_mode=False):
        self.__api_token = None

        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__vendor_given_names = vendor_given_names
        self.__vendor_last_names = vendor_last_names
        self.__vendor_email = vendor_email
        self.__currency_code = currency_code
        self.__dev_mode = dev_mode

    async def __get_base_url(self):
        if self.__dev_mode:
            return "https://api-m.sandbox.paypal.com"
        else:
            return "https://api-m.paypal.com"
        
    async def __get_api_token(self):
        auth = base64.b64encode(f"{self.__client_id}:{self.__client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{await self.__get_base_url()}/v1/oauth2/token",
                headers=headers,
                data=data
            )
            response.raise_for_status()
            return response.json()["access_token"]
        
    async def login(self):
        self.__api_token = await self.__get_api_token()