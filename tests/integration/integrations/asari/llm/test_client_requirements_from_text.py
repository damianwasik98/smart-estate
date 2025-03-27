from langchain_core.language_models import BaseChatModel
from langchain_core.exceptions import OutputParserException
import pytest
from smart_estate.integrations.asari.llm import client_requirements_from_text
from smart_estate.integrations.asari.models import LLMClientRequirements
from langchain_groq import ChatGroq

# export GROQ_API_KEY to run this test
llama3 = ChatGroq(model="llama3-70b-8192")


@pytest.mark.parametrize("llm", [llama3])
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "Klient szuka nieruchomości w dzielnicy Śródmieście i ma budżet siedemset tysięcy.",
            LLMClientRequirements(
                location="Śródmieście",
                price_max=700000,
            ),
        ),
        (
            "Łódź Bałuty za max 500 tysięcy, 3 lub 4 piętro.",
            LLMClientRequirements(
                location="Łódź Bałuty",
                price_max=500000,
                floor_no_min=3,
                floor_no_max=4,
            ),
        ),
        (
            "Łódź Retkinia za max 555 tysięcy, przynajmniej 2 pokoje i chciałby kupić w tym miesiącu",
            LLMClientRequirements(
                location="Łódź Retkinia",
                price_max=555000,
                no_of_rooms_min=2,
                note="chciałby kupić w tym miesiącu",
            ),
        ),
        (
            "Górna, trzysta tysięcy, chce spotkanie jutro",
            LLMClientRequirements(
                location="Górna",
                price_max=300000,
                note="chce spotkanie jutro",
            ),
        ),
        (
            "Śródmieście 3 lub 4 lub 5 pokoi",
            LLMClientRequirements(
                location="Śródmieście", no_of_rooms_min=3, no_of_rooms_max=5
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_returns_parsed_requirements_when_note_contains_correct_information(
    text: str,
    expected: LLMClientRequirements,
    llm: BaseChatModel,
) -> None:
    result = await client_requirements_from_text(text, llm)
    assert result == expected, f"Result is not as expected for text: {text}"


@pytest.mark.parametrize("llm", [llama3])
@pytest.mark.parametrize(
    "text",
    ["", "Mieszkanie 50m", "3 pokoje"],
)
@pytest.mark.asyncio
async def test_raises_when_note_does_not_contain_required_information(
    text: str, llm: BaseChatModel
) -> None:
    with pytest.raises(OutputParserException):
        await client_requirements_from_text(text, llm)


@pytest.mark.parametrize("llm", [llama3])
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "Śródmieście 3 lub 4 lub 5 pokoi",
            LLMClientRequirements(
                location="Śródmieście", no_of_rooms_min=3, no_of_rooms_max=5
            ),
        )
    ],
)
@pytest.mark.asyncio
async def test_result_not_as_expected_when_note_is_not_precise(
    text: str, llm: BaseChatModel, expected: LLMClientRequirements
) -> None:
    result = await client_requirements_from_text(text, llm)
    assert result != expected
