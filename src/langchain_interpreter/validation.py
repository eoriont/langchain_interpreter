from referencing import Registry, Resource
from jsonschema import Draft202012Validator
import json


def get_validator():
    registry = Resource.from_contents(template_schema) @ Registry()
    registry = Resource.from_contents(chain_schema) @ registry
    registry = Resource.from_contents(llm_schema) @ registry
    registry = Resource.from_contents(prompt_schema) @ registry
    registry = Resource.from_contents(memory_schema) @ registry
    registry = Resource.from_contents(retriever_schema) @ registry
    registry = Resource.from_contents(vectorstore_schema) @ registry

    validator = Draft202012Validator(template_schema, registry=registry)

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


template_schema = {
    "$id": "https://example.com/template.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain Template",
    "description": "A langchain template",
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "The name of the langchain template"},
        "description": {
            "type": "string",
            "description": "Description of the langchain template",
        },
        "template_version": {
            "type": "string",
            "description": "Version of the langchain template interpreter.",
        },
        "chain": {"$ref": "https://example.com/chain.schema.json"},
    },
    "additionalProperties": False,
    "required": ["name", "template_version", "chain"],
}

chain_schema = {
    "$id": "https://example.com/chain.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain Chain",
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
            "items": {"$ref": "https://example.com/chain.schema.json"},
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
        "chain_type": {
            "type": "string",
            "description": "For retrieverqa, the chaintype",
        },
        "retriever": {"$ref": "https://example.com/retriever.schema.json"},
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

retriever_schema = {
    "$id": "https://example.com/retriever.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain Retriever",
    "description": "A langchain retriever object",
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "description": "The type of retriever.",
        },
        "vectorstore": {"$ref": "https://example.com/vectorstore.schema.json"},
    },
    "additionalProperties": False,
    "required": ["type"],
}


vectorstore_schema = {
    "$id": "https://example.com/vectorstore.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "LangChain Vector Store",
    "description": "A langchain vector store object",
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "description": "The type of vector store.",
        },
        "host": {
            "type": "string",
            "description": "The host for the vector store service.",
        },
        "port": {
            "type": "string",
            "description": "The port of the vector store service.",
        },
    },
    "additionalProperties": False,
    "required": ["type"],
}
