from asari import AsariAPI
from estmate_api.models import (
    ClientRequirements,
    LLMClientRequirements,
    PhonecallNote,
    User,
)
from estmate_api.llm import client_requirements_from_text
from estmate_api.deps.chat_model import get_chat_model


class AsariService:
    def __init__(self, user: User) -> None:
        self._asari_client = AsariAPI(
            email=user.asari_username,
            password=user.asari_password,
        )

    async def save_to_asari(
        self,
        phonecall_note: PhonecallNote,
    ) -> None:
        parsed_requirements: LLMClientRequirements = (
            await client_requirements_from_text(
                text=phonecall_note.text, llm=get_chat_model()
            )
        )
        requirements = ClientRequirements(
            phone_number=phonecall_note.client_phone_number,
            first_name=phonecall_note.client_name,
            **parsed_requirements.model_dump(),
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
            private_description="Notatka ze skrótu iOS:\n" + phonecall_note.text,
        )
