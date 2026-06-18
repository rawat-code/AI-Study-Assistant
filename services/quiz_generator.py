from utils.llm import generate_response
from services.text_processor import chunk_text
from utils.db_manager import generate_text_hash,check_cache,save_to_cache

def generate_quiz(notes:str ,num_questions: int=10)->str:
    text_hash=generate_text_hash(notes)
    cached_quiz=check_cache(text_hash,request_type='quiz')
    if cached_quiz:
        print("cache hit!,returning quiz instantly from database.")
        return cached_quiz
    
    text_chunks=chunk_text(notes,chunk_size=1200,overlap=150)
    combined_context="\n----CONTENT BLOCK-----\n".join(text_chunks)

    prompt = f"""
              you are an expert academic examiner .create a strictly accurate multiple-choice quiz based only on the source material provided below.
              ANTI-HALLUCINATION GUARDAILS:
              -rely only on the clear facts explicitly mentioned in the context.
              -direct facts only.do not extrapolate,assume,or pull outside concepts different from the main concept of source material.
              -if the source material does not contain enough data for {num_questions} questions ,only generate as many can be verified.
                
              OUTPUT FORMAT INSTRUCTION:
              For EACH question use EXACTLY this format:

                Q1. Question

                   A) Option A
                   B) Option B
                   C) Option C
                   D) Option D

                    Answer: [insert only the correct option letter here (eg:A,B,C,D)]

                    Explanation:
                    Short explanation of why the answer is correct.

                Repeat for all{num_questions} questions.
             
               ----start of source material-----
               {combined_context}
               ----end of source material------
               """
    print(f"generating {num_questions}grounded quiz questions...")
    result=generate_response(prompt)
    save_to_cache(text_hash,request_type='quiz',cached_response=result)
    return result 