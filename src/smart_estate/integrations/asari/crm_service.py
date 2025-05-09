from asari import AsariAPI
from asari.exceptions import AsariAuthenticationError
from smart_estate.db.models import AsariCredentials
from smart_estate.integrations.asari.exceptions import CRMAuthenticationError
from smart_estate.integrations.asari.models import (
    ClientRequirements,
    LLMClientRequirements,
)
from smart_estate.api.schemas import PhonecallNote
from smart_estate.integrations.asari.llm import client_requirements_from_text


from langchain_groq import ChatGroq

from smart_estate.repositories.asari_phonecalls import AsariPhonecallRepository


class AsariCRMService:
    def __init__(
        self,
        credentials: AsariCredentials,
        asari_phonecall_repository: AsariPhonecallRepository,
    ) -> None:
        try:
            self._asari_client = AsariAPI(
                email=credentials.username,
                password=credentials.password,
            )
        except AsariAuthenticationError:
            raise CRMAuthenticationError("Invalid asari credentials. Login failed.")

        self._credentials = credentials
        self._llm = ChatGroq(model="llama3-70b-8192")
        self._asari_phonecall_repo = asari_phonecall_repository

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
        parsed_requirements_dump = parsed_requirements.model_dump(exclude_unset=True)
        await self._asari_phonecall_repo.save_phonecall(
            user_id=self._credentials.user_id,
            client_name=phonecall_note.client_name,
            client_phone_number=phonecall_note.client_phone_number,
            phonecall_note=phonecall_note.text,
            parsed_requirements=parsed_requirements_dump,
        )
        requirements = ClientRequirements(
            phone_number=phonecall_note.client_phone_number,
            first_name=phonecall_note.client_name,
            **parsed_requirements_dump,
        )

        locations = self._asari_client.find_locations(requirements.location)
        first_location_id = locations["data"][0]["id"]

        contact_response = self._asari_client.create_contact(
            first_name=requirements.first_name,
            last_name=requirements.last_name,
            phone_number=requirements.phone_number,
        )
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
