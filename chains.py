import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,model="llama-3.1-70b-versatile",groq_api_key= os.getenv("Groq_api_key"))


    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from carrer's page of a website
            your job is to extract the job postings and return them in json format containg the
            following keys :'role','experience','skills',notice period'and ;description'
            only return the valid JSON.
            ###VALID JSON
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data':cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException ("Context too big .Unable to Parse Jobs")
        return res if isinstance(res, list) else [res]

    def write_email(self,job, Link):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

        ### INSTRUCTION
        You are Mano, a business development executive at XYZ is an AI & Software company.
        the seamless integration of business process through automated tools.
        Over our experience we have empowered numerous enterprises with tailoured solutions
        Your job is to wrte a cold email to Client regarding thejob mentioned above with fulling
        their needs
        Also add most relevant one from the followng Link to showcase XYZ's port:{link_lists}
        Remember your are Mano, BDE at XYZ
        ### EMAIL (NO PREMABLE)

        """
    )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_lists":Link})
        return res.content

if __name__ =="__main__":
    print(os.getenv("Groq_api_key"))

