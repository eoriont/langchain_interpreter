from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.memory import SimpleMemory
from langchain.llms import type_to_cls_dict
import json

def chain_from_file(filename):
    with open(filename) as f:
        cfg = json.load(f)
    return get_chain(cfg)

def get_chain(cfg):
    if cfg["type"] == "LLMChain":
        return get_llm_chain(cfg)
    if cfg["type"] == "SimpleSequentialChain":
        return get_simple_sequential_chain(cfg)
    if cfg["type"] == "SequentialChain":
        return get_sequential_chain(cfg)

def get_llm(cfg):
    llm_type = type_to_cls_dict[cfg["name"]]
    llm = llm_type(**cfg["args"])
    return llm

def get_llm_chain(cfg):
    llm = get_llm(cfg["llm"])
    prompt = get_prompt(cfg["prompt"])
    output_key = cfg.get("output_key")
    memory = try_memory(cfg)
    llm_chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key, memory=memory)
    return llm_chain

def get_simple_sequential_chain(cfg):
    chains = [get_chain(chain) for chain in cfg["chains"]]
    memory = try_memory(cfg)
    ss_chain = SimpleSequentialChain(chains=chains, verbose=True, memory=memory)
    return ss_chain

def get_prompt(cfg):
    prompt = PromptTemplate(**cfg)
    return prompt

def get_sequential_chain(cfg):
    chains = [get_chain(chain) for chain in cfg["chains"]]
    input_variables = cfg["input_variables"]
    output_variables = cfg["output_variables"]
    memory = try_memory(cfg)
    seq_chain = SequentialChain(chains=chains, input_variables=input_variables, output_variables=output_variables, verbose=True, memory=memory)
    return seq_chain

def try_memory(cfg):
    if "memory" in cfg:
        return get_memory(cfg["memory"])
    return None

def get_memory(cfg):
    if cfg["type"] == "SimpleMemory":
        return get_simple_memory(cfg)

def get_simple_memory(cfg):
    memories = cfg["memories"]
    simple_memory = SimpleMemory(memories=memories)
    return simple_memory
