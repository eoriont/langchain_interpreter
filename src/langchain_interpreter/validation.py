from referencing import Registry, Resource
from jsonschema import Draft202012Validator
import json


def get_validator():
    chain_resource = Resource.from_contents(chain_schema)
    llm_resource = Resource.from_contents(llm_schema)
    prompt_resource = Resource.from_contents(prompt_schema)
    memory_resource = Resource.from_contents(memory_schema)

    registry = chain_resource @ (
        llm_resource @ (prompt_resource @ (memory_resource @ Registry()))
    )

    validator = Draft202012Validator(chain_schema, registry=registry)

    return validator


def validate_chain(json):
    """Validate chain template json against json schema.

    Args:
        json (string): The json to validate

    Raises:
        ValidationError: The schema validation error
    """
    validator = get_validator()
    validator.validate(json)


def validate_file(path):
    """Validate chain template json against json schema.

    Args:
        path (string): The path to the file containing json

    Raises:
        ValidationError: The schema validation error
    """
    with open(path) as f:
        cfg = json.load(f)
    validate_chain(cfg)


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
        "prompt": {"$ref": "https://example.com/prompt.schema.json"},
        "memory": {"$ref": "https://example.com/memory.schema.json"},
        "input_variables": {
            "type": "array",
            "description": "List of input variables to the chain",
            "items": {"type": "string"},
        },
        "output_variables": {
            "type": "array",
            "description": "List of output variables for the chain",
            "items": {"type": "string"},
        },
        "output_key": {
            "type": "string",
            "description": "The key for the output of this specific chain.",
        },
    },
    "additionalProperties": False,
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
    "additionalProperties": False,
    "required": ["type"],
}

prompt_schema = {
    "$id": "https://example.com/prompt.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain Prompt Template",
    "description": "A langchain prompt template",
    "type": "object",
    "properties": {
        "template": {
            "type": "string",
            "description": "The template string for the prompt template.",
        },
        "input_variables": {
            "type": "array",
            "description": "A list of the input variables for the template",
            "items": {"type": "string"},
        },
    },
    "additionalProperties": False,
    "required": ["template"],
}

memory_schema = {
    "$id": "https://example.com/memory.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain Memory",
    "description": "A langchain memory object",
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "description": "The type of memory to use.",
        },
        "memories": {
            "type": "object",
            "description": "A kv store of the memories for simple memory.",
            "additionalProperties": {"type": "string"},
        },
        "context": {
            "type": "array",
            "description": "List of conversation inputs and outputs.",
            "items": {"type": "object"},
        },
        "history": {
            "type": "string",
            "description": "String of previous conversation.",
        },
    },
    "additionalProperties": False,
    "required": ["type"],
}
