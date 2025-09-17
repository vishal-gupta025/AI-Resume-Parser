from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser

# -------------------------
# Resume Schema
# -------------------------
class ResumeSchema(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    skills: List[str] = Field(..., description="Skills")
    experience: List[str] = Field(..., description="Work experiences")

# -------------------------
# LLM Resume Parser (normal class, not Pydantic)
# -------------------------
class LLMResumeParser:
    """LLM-powered Resume Parser using LangChain prompt + schema."""
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=ResumeSchema)
        self.prompt = PromptTemplate(
            template="""Extract candidate details (name, email, phone, skills, experience)
from the resume text below and return JSON.

Resume:
{text}

{format_instructions}""",
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def parse(self, text: str) -> dict:
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"text": text}).dict()

# -------------------------
# Parsers Instances
# -------------------------
llm = ChatOpenAI(model="gpt-4")
str_parser = StrOutputParser()
pydantic_parser = PydanticOutputParser(pydantic_object=ResumeSchema)
llm_resume_parser = LLMResumeParser(llm=llm)
