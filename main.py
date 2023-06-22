from langchain.chains import LLMChain, SimpleSequentialChain
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.llms import type_to_cls_dict
import json

def chain_from_file(filename):
    with open(filename) as f:
        cfg = json.load(f)

    llm_type = type_to_cls_dict[cfg["llm"]["name"]]
    llm = llm_type(**cfg["llm"]["args"])
    prompt = PromptTemplate(**cfg["prompt"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    return llm_chain
