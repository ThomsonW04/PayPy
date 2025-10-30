import httpx

class PayPyInvoicer:
    def __init__(self, base_url, headers):
        self.__base_url = base_url
        self.__headers = headers

    async def __get_next_invoice_number(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.__base_url}/v2/invoicing/generate-next-invoice-number",
                headers=self.__headers
            )
            response.raise_for_status()
            return response.json()["access_token"]

    async def create_invoice(self, 
                             currency_code: str, 
                             invoice_number: str = None, 
                             reference: str = None, 
                             invoice_date: str = None, 
                             note: str = None, 
                             term: str = None, 
                             memo: str = None,
                             payment_term: dict = None):
        
        # Initialise the data dictionary
        data = {}

        # Begin building the detail chunk of the invoice
        data['detail'] = {
            "invoice_number": invoice_number if invoice_number is not None else await self.__get_next_invoice_number(),
            "currency_code": currency_code
        }
        if reference is not None:
            data['detail']['reference'] = reference
        if invoice_date is not None:
            data['detail']['invoice_date'] = invoice_date
        if note is not None:
            data['detail']['note'] = note
        if term is not None:
            data['detail']['term'] = term
        if memo is not None:
            data['detail']['memo'] = memo
        if payment_term is not None:
            data['detail']['payment_term'] = payment_term

"""
"detail": {
"invoice_number": "#123",
"reference": "deal-ref",
"invoice_date": "2018-11-12",
"currency_code": "USD",
"note": "Thank you for your business.",
"term": "No refunds after 30 days.",
"memo": "This is a long contract",
"payment_term": {
"term_type": "NET_10",
"due_date": "2018-11-22"
}
},
"""