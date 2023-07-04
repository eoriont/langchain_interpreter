from langchain.chains import (
    LLMChain,
    SimpleSequentialChain,
    SequentialChain,
    ConversationChain,
)
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.memory import SimpleMemory, ConversationBufferMemory
from langchain.llms import type_to_cls_dict
import json


def chain_from_file(filename, **kwargs):
    with open(filename) as f:
        cfg = json.load(f)
    return get_chain(cfg, **kwargs)


def chain_from_str(s, **kwargs):
    return get_chain(json.loads(s), **kwargs)


def get_chain(cfg, **kwargs):
    if cfg["type"] == "LLMChain":
        return get_llm_chain(cfg, **kwargs)
    if cfg["type"] == "SimpleSequentialChain":
        return get_simple_sequential_chain(cfg, **kwargs)
    if cfg["type"] == "SequentialChain":
        return get_sequential_chain(cfg, **kwargs)
    if cfg["type"] == "ConversationChain":
        return get_conversation_chain(cfg, **kwargs)


def get_conversation_chain(cfg, **kwargs):
    llm = get_llm(cfg["llm"], **kwargs)
    memory = try_memory(cfg, **kwargs)

    conv_chain = ConversationChain(llm=llm, memory=memory)
    return conv_chain


def get_llm(cfg, **kwargs):
    llm_type = type_to_cls_dict[cfg["name"]]
    llm = llm_type(**cfg["args"], openai_api_key=kwargs.get("openai_api_key"))
    return llm


def get_llm_chain(cfg, **kwargs):
    llm = get_llm(cfg["llm"], **kwargs)
    prompt = get_prompt(cfg["prompt"])
    output_key = cfg.get("output_key", "text")
    memory = try_memory(cfg, **kwargs)
    llm_chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key, memory=memory)
    return llm_chain


def get_simple_sequential_chain(cfg, **kwargs):
    chains = [get_chain(chain, **kwargs) for chain in cfg["chains"]]
    memory = try_memory(cfg, **kwargs)
    ss_chain = SimpleSequentialChain(chains=chains, verbose=True, memory=memory)
    return ss_chain


def get_prompt(cfg):
    prompt = PromptTemplate(**cfg)
    return prompt


def get_sequential_chain(cfg, **kwargs):
    chains = [get_chain(chain, **kwargs) for chain in cfg["chains"]]
    input_variables = cfg["input_variables"]
    output_variables = cfg["output_variables"]
    memory = try_memory(cfg)
    seq_chain = SequentialChain(
        chains=chains,
        input_variables=input_variables,
        output_variables=output_variables,
        verbose=True,
        memory=memory,
    )
    return seq_chain


def try_memory(cfg, **kwargs):
    if "memory" in cfg:
        return get_memory(cfg["memory"], **kwargs)
    return None


def get_memory(cfg, **kwargs):
    if cfg["type"] == "SimpleMemory":
        return get_simple_memory(cfg, **kwargs)
    if cfg["type"] == "ConversationBufferMemory":
        return get_conversation_buffer_memory(cfg, **kwargs)


def get_simple_memory(cfg, **kwargs):
    memories = cfg["memories"]
    simple_memory = SimpleMemory(memories=memories)
    return simple_memory


def get_conversation_buffer_memory(cfg, **kwargs):
    conv_buf_memory = ConversationBufferMemory()

    if "context" in cfg:
        context = cfg["context"]
        if len(context) % 2 != 0:
            raise ValueError("the context doesn't have an even number of elements!")
    elif "history" in cfg:
        history = cfg["history"]
        context = parse_history(history)
    else:
        context = []

    if "history" in kwargs:
        history = kwargs.get("history")
        context += parse_history(history)

    # Save context
    for pos in range(0, len(context), 2):
        conv_buf_memory.save_context(context[pos], context[pos + 1])

    return conv_buf_memory


def parse_history(history: str):
    lines = history.split("\n")
    ctx = []

    for l in lines:
        if l.startswith("Human: "):
            ctx.append({"input": l.lstrip("Human: ")})
        elif l.startswith("AI: "):
            ctx.append({"output": l.lstrip("AI: ")})
        else:
            raise ValueError("each line in history must be from AI or human")

    return ctx
