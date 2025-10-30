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
                             invoicer_given_names: str,
                             invoicer_surname: str,
                             invoicer_email_address: str,
                             invoice_number: str = None, 
                             reference: str = None, 
                             invoice_date: str = None, 
                             note: str = None, 
                             term: str = None, 
                             memo: str = None,
                             payment_term: dict = None, # Expects dict of term_type and due_date
                             invoicer_address_line_one: str = None,
                             invoicer_address_line_two: str = None,
                             invoicer_admin_area_2: str = None,
                             invoicer_admin_area_1: str = None,
                             invoicer_postal_code: str = None,
                             invoicer_country_country_code: str = None,
                             invoicer_phones: list = None, # Expects list of dicts of country_code (int), national_number (int), phone_type (string)
                             invoicer_website: str = None,
                             invoicer_tax_id: str = None,
                             invoicer_logo_url: str = None,
                             invoicer_additional_notes: str = None,
                             ):
        
        # Initialise the data dictionary
        data = {}

        # Begin building the detail chunk of the invoice
        data["detail"] = {
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

        # Begin building invoicer chunk of the invoice

        data["invoicer"] = {
            "name": {
                "given_name": invoicer_given_names,
                "surname": invoicer_surname
            },
            "email_address": invoicer_email_address
        }

        if invoicer_address_line_one is not None:
            data["invoicer"]["address"]["address_line_1"] = invoicer_address_line_one
        if invoicer_address_line_two is not None:
            data["invoicer"]["address"]["address_line_2"] = invoicer_address_line_two
        if invoicer_admin_area_1 is not None:
            data["invoicer"]["address"]["admin_area_1"] = invoicer_admin_area_1
        if invoicer_admin_area_2 is not None:
            data["invoicer"]["address"]["admin_area_2"] = invoicer_admin_area_2
        if invoicer_postal_code is not None:
            data["invoicer"]["address"]["postal_code"] = invoicer_postal_code
        if invoicer_country_country_code is not None:
            data["invoicer"]["address"]["country_code"] = invoicer_country_country_code
        if invoicer_phones is not None:
            data["invoicer"]["address"]["phones"] = invoicer_phones
        if invoicer_website is not None:
            data["invoicer"]["address"]["website"] = invoicer_website
        if invoicer_tax_id is not None:
            data["invoicer"]["address"]["tax_id"] = invoicer_tax_id
        if invoicer_logo_url is not None:
            data["invoicer"]["address"]["logo_url"] = invoicer_logo_url
        if invoicer_additional_notes is not None:
            data["invoicer"]["address"]["additional_notes"] = invoicer_additional_notes