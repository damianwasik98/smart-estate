from asari import AsariAPI
from asari.exceptions import AsariAuthenticationError
from asari_automation_api.db.models import AsariCredentials
from asari_automation_api.integrations.asari.exceptions import CRMAuthenticationError
from asari_automation_api.integrations.asari.models import (
    ClientRequirements,
    LLMClientRequirements,
)
from asari_automation_api.api.schemas import PhonecallNote
from asari_automation_api.integrations.asari.llm import client_requirements_from_text


from langchain_groq import ChatGroq


class AsariCRMService:
    def __init__(self, credentials: AsariCredentials) -> None:
        try:
            self._asari_client = AsariAPI(
                email=credentials.username,
                password=credentials.password,
            )
        except AsariAuthenticationError:
            raise CRMAuthenticationError("Invalid asari credentials. Login failed.")

        self._llm = ChatGroq(model="llama3-70b-8192")

    async def save_phonecall_to_crm(
        self,
        phonecall_note: PhonecallNote,
    ) -> None:
        parsed_requirements: LLMClientRequirements = (
            await client_requirements_from_text(
                text=phonecall_note.text,
                llm=self._llm,
            )
        )
        requirements = ClientRequirements(
            phone_number=phonecall_note.client_phone_number,
            first_name=phonecall_note.client_name,
            **parsed_requirements.model_dump(),
        )

        locations = self._asari_client.find_locations(requirements.location)
        # TODO: handle scenario when no location found
        first_location_id = locations["data"][0]["id"]

        contact_response = self._asari_client.create_contact(
            first_name=requirements.first_name,
            last_name=requirements.last_name,
            phone_number=requirements.phone_number,
        )
        # TODO: handle scenario when create contact failed
        contact_id = contact_response["data"]["id"]
        self._asari_client.create_sale(
            location_id=first_location_id,
            customer_id=contact_id,
            description=requirements.note,
            area_min=requirements.area_min,
            area_max=requirements.area_max,
            price_max=requirements.price_max,
            no_of_rooms_min=requirements.no_of_rooms_min,
            floor_no_max=requirements.floor_no_max,
            private_description="Oryginalna notatka z rozmowy:\n" + phonecall_note.text,
        )
