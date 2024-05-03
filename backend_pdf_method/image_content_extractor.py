from gemini_request import process_image_with_api
from prompts import initial_prompt
from prompts import get_follow_up_prompt

def image_content_extractor(uploaded_uris):
    """
    Processes a list of uploaded image URIs to extract information using AI-powered image processing. 
    Adapts the processing prompts dynamically based on the content extracted from previous images.

    Args:
        uploaded_uris (list of str): URIs of images uploaded for processing.

    Returns:
        tuple: A tuple containing the concatenated string of all extracted data and a boolean 
               indicating whether the data includes table content.
    """
    accumulated_data = [] # Store all relevant extracted information
    use_follow_up_prompt = False # Flag to determine which prompt to use
    last_relevant_info = ""  # Store last relevant info for generating follow-up prompts
    table_content = False # Flag to track if any extracted content is a table
    for i, uri in enumerate(uploaded_uris):
        # Select the appropriate prompt based on the context of previous extractions
        if use_follow_up_prompt:
            prompt_text = get_follow_up_prompt(last_relevant_info)
        else:
            prompt_text = initial_prompt
        
        print(f"Using prompt for image {i + 1}: {prompt_text[:100]}...")

        # Process the image with the selected prompt
        continue_processing, extracted_info = process_image_with_api(uri, prompt_text)
        print(f"Response for image {i + 1}: Continue Processing = {continue_processing}, Extracted Data Length = {len(extracted_info)}")

        if extracted_info:
            # Check the first line to decide on handling
            first_line = extracted_info.split('\n', 1)[0]
            if first_line == "Table,1":
                # Extracted content indicates a table, switch to follow-up prompt and process subsequent parts
                last_relevant_info = '\n'.join(extracted_info.split('\n')[1:])
                accumulated_data.append(last_relevant_info)
                use_follow_up_prompt = True
                table_content = True
            elif extracted_info == '0':
                # If output is '0', ignore this output and continue with the same prompt status
                continue
            else:
                # For any other content, reset to the initial prompt for the next image
                accumulated_data.append(extracted_info)
                use_follow_up_prompt = False 
                table_content = False

        if not continue_processing:
            print(f"Processing concluded with image {i + 1}")
            break
    # Join all accumulated data into a single string
    final_data = '\n'.join(accumulated_data)
    print(final_data)
    return final_data, table_content

