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
                             recipients: list, # Expects list of dicts of ATLEAST billinginfo.name.given_name (str) billing_info.name.surname (str) billing_info.email_address (str) more info can be found in the docs
                             items: list, # Expects list of dicts of ATLEAT name (str) quantity (int) unit_amount.currency_code (str) unit_amount.value (float)
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
                             allow_partial_payment: bool = False,
                             minimum_amount_due: int = None,
                             allow_tip: bool = True,
                             tax_calculated_after_discount: bool = True,
                             tax_inclusive: bool = False,
                             template_id: str = None,
                             amount_breakdown: dict = None # May add a amount breakdown, read docs
                             ):
        
        # Initialise the data dictionary

        data = {}

        # Begin building the detail chunk of the invoice

        data["detail"] = {
            "invoice_number": invoice_number if invoice_number is not None else await self.__get_next_invoice_number(),
            "currency_code": currency_code
        }

        if reference: data["detail"]["reference"] = reference
        if invoice_date: data["detail"]["invoice_date"] = invoice_date
        if note: data["detail"]["note"] = note
        if term: data["detail"]["term"] = term
        if memo: data["detail"]["memo"] = memo
        if payment_term: data["detail"]["payment_term"] = payment_term

        # Begin building the invoicer chunk of the invoice
        
        data["invoicer"] = {
            "name": {"given_name": invoicer_given_names, "surname": invoicer_surname},
            "email_address": invoicer_email_address
        }
        
        invoicer_address = {}
        if invoicer_address_line_one: invoicer_address["address_line_1"] = invoicer_address_line_one
        if invoicer_address_line_two: invoicer_address["address_line_2"] = invoicer_address_line_two
        if invoicer_admin_area_1: invoicer_address["admin_area_1"] = invoicer_admin_area_1
        if invoicer_admin_area_2: invoicer_address["admin_area_2"] = invoicer_admin_area_2
        if invoicer_postal_code: invoicer_address["postal_code"] = invoicer_postal_code
        if invoicer_country_country_code: invoicer_address["country_code"] = invoicer_country_country_code
        if invoicer_phones: invoicer_address["phones"] = invoicer_phones
        if invoicer_website: invoicer_address["website"] = invoicer_website
        if invoicer_tax_id: invoicer_address["tax_id"] = invoicer_tax_id
        if invoicer_logo_url: invoicer_address["logo_url"] = invoicer_logo_url
        if invoicer_additional_notes: invoicer_address["additional_notes"] = invoicer_additional_notes
        if invoicer_address:
            data["invoicer"]["address"] = invoicer_address

        # Begin building the recipients chunk of the invoice

        data["primary_recipients"] = recipients

        # Begin building the items chunk of the invoice

        data["items"] = items

        # Begin building the extra configuration chunk of the invoice

        data["configuration"] = {
            "allow_tip": allow_tip,
            "tax_calculated_after_discount": tax_calculated_after_discount,
            "tax_inclusive": tax_inclusive
        }
        if allow_partial_payment and minimum_amount_due is not None:
            data["configuration"]["partial_payment"] = {
                "allow_partial_payment": True,
                "minimum_amount_due": {"currency_code": currency_code, "value": str(minimum_amount_due)}
            }
        if template_id: data["configuration"]["template_id"] = template_id

        if amount_breakdown:
            data["amount"] = {"breakdown": amount_breakdown}
