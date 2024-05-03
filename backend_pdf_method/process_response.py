def process_response(response_json):
    """
    Processes the JSON response from an API to extract relevant text content. It handles special
    text cases like 'Table,1' and ignores responses that explicitly contain '0'.

    Args:
        response_json (dict): The JSON object containing the API response.

    Returns:
        tuple (bool, str): A tuple where the first element is a flag indicating whether to continue
                           processing (always True here) and the second element is the extracted text,
                           or an empty string in case of errors or special ignored cases.
    """    
    try:
        # Access the first candidate in the response, if available
        candidate = response_json.get('candidates', [])[0]
        content_parts = candidate.get('content', {}).get('parts', [])
        response_text = ' '.join(part['text'] for part in content_parts).strip()

        lines = response_text.split('\n')
        first_line = lines[0].strip()
        
        # Ignore the output completely if response is '0'
        if response_text == '0':
            return True, ""  # Continue processing, but return no data for this image
        
        # Special handling for 'Table,1' indicating the response contains table data
        if first_line == "Table,1":
            # Return all the text for special handling in the main processing loop
            return True, response_text
        
        # Normal text processing, returning all the extracted information
        return True, response_text  # Always continue processing the next image
    except Exception as error:
        print(f"Error processing API response: {error}")
        return True, ""  # Continue processing, but return empty data on error