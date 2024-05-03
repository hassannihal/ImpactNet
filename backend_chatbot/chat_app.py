# This module uses Streamlit to interactively perform Corporate Social Responsibility (CSR) analysis using AI.
# It integrates with various external APIs and services to process and visualize data based on user input.

import streamlit as st
from gemini_image_request import extract_code, process_context_and_question, process_context_and_code
from dotenv import load_dotenv
import os
from embed import embed_text
from retrival import perform_vector_search, retrieve_text_chunks, concatenate_texts
import json
import time

def extract_text_from_response(response):
    """Extracts text from response JSON and returns a concatenated string of all text parts."""
    text_parts = []
    for candidate in response.get('candidates', []): # Iterating through each candidate part in the response
        content = candidate.get('content', {})
        for part in content.get('parts', []):  # Extracting text from each part of the content
            if 'text' in part:
                text_parts.append(part['text'])
    return ' '.join(text_parts)

def main():
    # Set up environment and load necessary variables
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)
    project_id = os.getenv("PROJECT_ID")
    
    # Initialize Streamlit UI with a title
    st.title("CSR Analysis with AI")
    # User input for question
    user_question = st.text_input("Enter your question related to CSR:")

    if user_question and st.button('Ask'):
        # Embed the user question and perform a vector search to find relevant text chunks
        embed_question = embed_text(user_question)
        chunk_ids = perform_vector_search(embed_question)
        text_chunks = retrieve_text_chunks(chunk_ids)
        single_text_context = concatenate_texts(text_chunks)

        # Process the question with the context obtained and display the response
        final_prompt = f"Answer this question in as much quality manner as possible: {user_question} The given context is {single_text_context}. Derive the answer from this context. And no comments from your side."
        descriptive_response = process_context_and_question(final_prompt)  # This should be a response that can be streamed
        if descriptive_response:
            extracted_text = extract_text_from_response(descriptive_response)
            st.write(extracted_text)

        # Generate and execute plotting code based on the user question and context
        plot_code_question = f"given the context: {single_text_context}, answer the following question with only charts: {user_question}. Strictly only give me the code to plot charts that are easy to digest narrative. Please provide charts only in one code utilizing streamlit graph capability with plotly, and no comments from your side. Consider splitting complex graphs into simpler ones as the charts should be super easy to understand. Only provide the charts if it is super easy to make sense of otherwise strictly give NULL response. If the question is not related to knowledge base, create charts basis your knowledge. Note: Atmost give 4 charts and display 2 in each row. And these charts should be center aligned when it comes to the width of the output area. The code should not try to access any file or directory. If there is extreme data such that the chart will not be easy understood, then avoid showing it. Do not include the actual source names like figure names, box names, table names etc."
        code_response = process_context_and_code(plot_code_question)
        plotting_code = ""
        if "error" not in code_response:
            plotting_code = extract_code(code_response)
            lines = plotting_code.strip().split('\n')
            modified_code = '\n'.join(lines[1:-1])

        if modified_code:
            try:
                exec(modified_code, globals())
            except Exception as e:
                st.error(f"Failed to execute plotting code: {str(e)}")

if __name__ == "__main__":
    main()
