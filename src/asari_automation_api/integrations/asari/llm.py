from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseChatModel

from asari_automation_api.integrations.asari.models import LLMClientRequirements


async def client_requirements_from_text(
    text: str, llm: BaseChatModel
) -> LLMClientRequirements:
    parser = PydanticOutputParser(pydantic_object=LLMClientRequirements)
    prompt = PromptTemplate(
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template="""
        Analyze the following real estate client conversation note and extract information
        to correct model fields based on fields description described in format instructions below. 
        Ensure values remain in the same language as the original note.
        Ensure that values are converted to correct types like in format instructions.

        Client conversation note: {text}
        
        Format instructions:
        {format_instructions}

        
        For the fields specified in required, if the note does not contain any value for that field.
        For example if the field is location, do not include the "location" field in the JSON output at all.
        If "location" is not mentioned, leave it out entirely, do not fill it with arbitrary or inferred data.
        """,
    )
    chain = prompt | llm | parser
    result = await chain.ainvoke({"text": text})
    return result
