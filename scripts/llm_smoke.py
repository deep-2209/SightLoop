# from sightloop.llm_anthropic import make_anthropic_llm

# llm = make_anthropic_llm()
# print(llm("Reply with exactly: hello"))


# from sightloop.llm_openai import make_openai_llm

# llm = make_openai_llm()
# print(llm("Reply with exactly: hello"))


from sightloop.llm_groq import make_groq_llm

llm = make_groq_llm()
print(llm("Reply with exactly: hello"))