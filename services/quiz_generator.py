from utils.gemini import model
import json 
from utils.llm import (
    generate_response
)
from services.text_processor import chunk_text

def generate_quiz(notes:str ,num_questions: int=10)->list:
    text_chunks=chunk_text(notes,chunk_size=1200,overlap=150)
    combined_context="\n----CONTENT BLOCK-----\n".join(text_chunks[:5])

    prompt = f"""
              you are an expert academic examiner .create a strictly accurate multiple-choice quiz based only on the source material provided below.
              ANTI-HALLUCINATION GUARDAILS:
              -direct facts only.do not extrapolate,assume,or pull outside concepts different from the main concept of source material.
              -if the source material does not contain enough data for {num_questions} questions ,only generate as many can be verified.
                
              OUTPUT :
              you must respond only with a raw json array of objects.do not include any markdown like '''json or trailing text.'''follow this exact structure:
              [{{
              "question":"clear question text drawn from context?",
              "options":["option A","option B","option C","option D"],
              "answer":"The exact string matching the correct option"
              }}]
               ----start of source material-----
               {combined_context}
               ----end of source material------
               JSON output:
               """
    print(f"generating {num_questions}grounded quiz questions...")
    raw_response=generate_response(prompt).strip()
    if raw_response.startswith("'''"):
        raw_response=raw_response.strip("'").replace("json","",1).strip()
    try:
        quiz_data=json.loads(raw_response)  
        return quiz_data
    except Exception as e:
        print(f"JSON parsing error:{e}.falling back to default container.")
        return []  