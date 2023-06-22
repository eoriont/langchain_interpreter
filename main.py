from langchain.chains import LLMChain, SimpleSequentialChain
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

def get_llm(cfg):
    llm_type = type_to_cls_dict[cfg["name"]]
    llm = llm_type(**cfg["args"])
    return llm

def get_llm_chain(cfg):
    llm = get_llm(cfg["llm"])
    prompt = PromptTemplate(**cfg["prompt"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    return llm_chain

def get_simple_sequential_chain(cfg):
    chains = [get_chain(chain) for chain in cfg["chains"]]
    ss_chain = SimpleSequentialChain(chains=chains, verbose=True)
    return ss_chain
