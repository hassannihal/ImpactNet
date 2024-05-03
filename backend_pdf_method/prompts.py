# Constants and Prompt Functions
initial_prompt = """Extract all the information from this image. For text-only information part such as sentences and paragraphs, extract as it is first, then for visual information - convert it into a table format in text such that you can understand later on and also explain it within 250 tokens. For table information, extract it and give it in a table format in text such that you can understand later on and also explain it within 250 tokens. If the image only has tables content then return them in comma seperate fashion and add a line on the top of output - 'Table,1'
If the image looks like contents section of a book or is empty then return '0' in response. Ensure your response does not contain any extra text or comments. Ensure that you organize the infomration such that if I feed the text back to you, you are capable of understanding it."""

def get_follow_up_prompt(current_csv_data):
    return f"""Analyze the image in relation to the provided CSV data: {current_csv_data}. 
- Condition 1: If the image directly continues the sequence of data and the current image looks like a continuation of csv data:
  1. Add metadata at the top of the this output, signifying what all analysis and insights are possible in a super concise manner within 250 tokens. 
  2. Following metadata, extract and add all the table data and add the previous csv data table header to the top of this new table.
  3. Then add another line to the top most part of the response with text 'Table,1'
  Ensure your response does not contain any extra text or comments.

- Condition 2: IF the image does not continue the sequence of data, then,
  1. Add metadata at the top of the this output, signifying what all analysis and insights are possible in a super concise manner within 250 tokens.
  2. Extract all the table data in comma seperated fashion and add a line to the top most part of response:'Table,1'
  Ensure your response does not contain any extra text or comments."""