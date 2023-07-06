from referencing import Registry, Resource
from jsonschema import Draft202012Validator


def get_validator():
    chain_schema_resource = Resource.from_contents(chain_schema)
    llm_schema_resource = Resource.from_contents(llm_schema)

    registry = chain_schema_resource @ (llm_schema_resource @ Registry())

    validator = Draft202012Validator(chain_schema, registry=registry)

    return validator


def validate_chain(json):
    validator = get_validator()
    validator.validate(json)


chain_schema = {
    "$id": "https://example.com/template.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain Template",
    "description": "A langchain chain",
    "type": "object",
    "properties": {
        "type": {"type": "string", "description": "The type of chain to be used"},
        "llm": {
            "$ref": "https://example.com/llm.schema.json",
            "description": "Specification of the llm to be used",
        },
        "chains": {
            "type": "array",
            "description": "A list of chains to be executed in the sequential chain.",
            "items": {"$ref": "https://example.com/template.schema.json"},
        },
    },
    "required": ["type"],
}

llm_schema = {
    "$id": "https://example.com/llm.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain LLM",
    "description": "A langchain llm",
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "description": "The type of llm to be used",
        },
        "args": {
            "type": "object",
            "description": "The arguments of the llm to be passed in",
        },
    },
    "required": ["type"],
}
