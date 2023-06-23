from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain import PromptTemplate, OpenAI, LLMChain
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
    llm_chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key)
    return llm_chain

def get_simple_sequential_chain(cfg):
    chains = [get_chain(chain) for chain in cfg["chains"]]
    ss_chain = SimpleSequentialChain(chains=chains, verbose=True)
    return ss_chain

def get_prompt(cfg):
    prompt = PromptTemplate(**cfg)
    return prompt

def get_sequential_chain(cfg):
    chains = [get_chain(chain) for chain in cfg["chains"]]
    input_variables = cfg["input_variables"]
    output_variables = cfg["output_variables"]
    seq_chain = SequentialChain(chains=chains, input_variables=input_variables, output_variables=output_variables, verbose=True)
    return seq_chain
