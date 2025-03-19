from asari import AsariAPI
from estmate_api.models import ClientRequirements


def save_to_asari(
    api_client: AsariAPI, requirements: ClientRequirements, phonecall_note: str
):
    locations = api_client.find_locations(requirements.location)
    first_location_id = locations["data"][0]["id"]

    contact_response = api_client.create_contact(
        first_name=requirements.first_name,
        last_name=requirements.last_name,
        phone_number=requirements.phone_number,
    )
    contact_id = contact_response["data"]["id"]
    api_client.create_sale(
        location_id=first_location_id,
        customer_id=contact_id,
        description=requirements.note,
        area_min=requirements.area_min,
        area_max=requirements.area_max,
        price_max=requirements.price_max,
        no_of_rooms_min=requirements.no_of_rooms_min,
        floor_no_max=requirements.floor_no_max,
        private_description=phonecall_note,
    )
