import base64
import httpx
import asyncio
from .PayPyInvoicer import PayPyInvoicer


class PayPy(PayPyInvoicer):
    def __init__(self, client_id, client_secret, vendor_given_names, vendor_last_names, vendor_email, currency_code="GBP", dev_mode=False):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__vendor_given_names = vendor_given_names
        self.__vendor_last_names = vendor_last_names
        self.__vendor_email = vendor_email
        self.__currency_code = currency_code
        self.__dev_mode = dev_mode

        self.__api_token = None
        self._tasks = asyncio.Queue()
        self._running = False

    def __get_base_url(self):
        return "https://api-m.sandbox.paypal.com" if self.__dev_mode else "https://api-m.paypal.com"

    async def __get_api_token(self):
        auth = base64.b64encode(f"{self.__client_id}:{self.__client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.__get_base_url()}/v1/oauth2/token",
                headers=headers,
                data=data
            )
            response.raise_for_status()
            return response.json()["access_token"]

    async def __login(self):
        print("Attempting Login!")
        try:
            self.__api_token = await self.__get_api_token()
            print("Login Successful!")
        except Exception as e:
            print(f"Failed to login: {str(e)}")
        try:
            print("Initialising the rest of PayPy!")
            PayPyInvoicer.__init__(self, self.__get_base_url(), self.__api_token)
            print("Successfully initialised the rest of PayPy!")
        except Exception as e:
            print(f"Failed to initialise: {str(e)}")

    async def __worker(self):
        while self._running:
            func, args, kwargs = await self._tasks.get()
            try:
                await func(*args, **kwargs)
            except Exception as e:
                print(f"Error in task: {e}")
            self._tasks.task_done()

    async def run(self):
        self._running = True

        worker_task = asyncio.create_task(self.__worker())

        await self.__login()

        print("PayPy is running. Press Ctrl+C to exit.")

        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Shutting down...")
            self._running = False
            worker_task.cancel()
            await worker_task

