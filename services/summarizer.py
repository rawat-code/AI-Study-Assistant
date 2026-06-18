from utils.llm import generate_response
from services.text_processor import chunk_text
from utils.db_manager import generate_text_hash,check_cache,save_to_cache

def generate_summary(notes: str) ->str:
    text_hash=generate_text_hash(notes)
    cached_summary=check_cache(text_hash,request_type='summary')
    if cached_summary:
      print("cache hit! returning summary from database.")
      return cached_summary
    text_chunks=chunk_text(notes,chunk_size=1200,overlap=150)
    combined_context="\n---CONTEXT SEPARATOR---\n".join(text_chunks)
    prompt = f"""
    you are an expert academic verification assistant.your goal is to write a highly detailed ,comprehensive ,and deeply structured summary based only on the verified source material provided below.
    
    CRITICAL ANTI-HALLUCINATION INSTRUCTIONS:
    1.rely only on the clear facts explicitly mentioned in the context.
    2.do no assume,explorate,or bring in outside historical or technical facts not written below.
    3.if a concept connot be verified directly from this text,completely ignore it.do not invent explanations.
    4.for every main point or definition you write, ensure it can be tracked straight back to a sentence in the text.

    --START OF VERIFIED SOURCE MATERIAL---
    {combined_context}
    ---END OF VERIFIED SOURCE MATERIAL---
    please structure your response beautifully using the following format:
    IMPORTANT RULES:
       - Use proper line breaks.
       - Leave ONE blank line between sections.
       - Leave ONE blank line between bullet points.
       - Never write everything in one paragraph.
       - Never write section titles and content on the same line.
    #1.📖comprehensive summary[overview]:
    [provide a deep,thorough or introduction ,5-8 lines high-level overview of what this chapter/material covers based strictly on the text.]
     
    ---
    #2.🎯key concepts:
    * **[core concept 1]**: detailed explanation of the core concept directly from the text.
    * **[core concept 2]**: detailed explanation of the core concept directly from the text.
    * [add as many terms as are present in the text]

    ---
    #3.📖chapter breakdown &details:
    * **important insight**:provide detailed bullet points on the specific sub topics ,processes or facts written in the material.
    * **supporting detail**:ensure nothing important from the text is omitted,keeping descriptions clear and thorough.
    provide these details also:
    🧠 IMPORTANT DEFINITIONS

       • Term1: Definition

       • Term2: Definition
       *[add aleast 3 terms and 5 max only,give importance to those which are highly crucial for the concept.]

    🔑 KEY TAKEAWAYS

       • Takeaway 1

       • Takeaway 2
       ----

    🚀 QUICK REVISION NOTES

       • Revision Point 1

       • Revision Point 2
       [add atleast 3 to 4 revision points that are highly crucial for revision.]

    DETAILED GROUNDED SUMMARY:
    """
    print("printing advanced structure summary and anti_hallucinationpipelines....")

    summary_output=generate_response(prompt)
    save_to_cache(text_hash,request_type='summary',cached_response=summary_output)
    return summary_output
