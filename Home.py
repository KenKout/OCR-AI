import asyncio
import io

import requests
import streamlit
from PIL import Image
from streamlit_paste_button import paste_image_button

from app.utils.ocr import SYSTEM_PROMPT, process_image

if __name__ == '__main__':
    streamlit.set_page_config(page_title='LaTeX-OCR')
    streamlit.title('LaTeX OCR')
    streamlit.markdown('Convert images of equations to corresponding LaTeX code.\n\n')

    uploaded_file = streamlit.file_uploader(
        'Upload an image an equation',
        type=['pdf', 'png', 'jpg', 'jpeg']
    )

    paste_result = paste_image_button(
        label="📋 Paste an image",
        background_color="#222831",
        hover_background_color="#31363F",
        errors='raise')

    if paste_result.image_data is not None:
        streamlit.write('Pasted image:')
        streamlit.image(paste_result.image_data)
        bytes = io.BytesIO()
        paste_result.image_data.save(bytes, format='PNG')
        image_bytes = bytes.getvalue()
    else:
        image_bytes = None

    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            # Select the first page of the PDF to display
            image = True
        else:
            image = Image.open(uploaded_file)
            streamlit.image(image, caption='Uploaded image', use_container_width=True)
    else:
        image = None
        streamlit.text('\n')
    # Option to convert the image to LaTeX or Text
    option = streamlit.radio('Select the type of conversion', ['LaTeX', 'Custom'])
    streamlit.write(f"You selected: `{option}`", )
    if option == 'Custom':
        # Input text with multiple lines, with 10 as the default number of lines
        user_instruction = streamlit.text_area('Enter user instruction', value='', height=300)
        system_instruction = streamlit.text_area('Enter system instruction', value=SYSTEM_PROMPT, height=300)
    else:
        user_instruction = None
        system_instruction = None
    if streamlit.button('Convert'):
        if uploaded_file is not None and image is not None and uploaded_file.type == 'application/pdf':
            with streamlit.spinner('Computing'):
                response = requests.post('http://127.0.0.1:8000/pdf/submit', files={'file': uploaded_file.getvalue()}, data={'user_instruction': user_instruction or None, 'system_instruction': system_instruction or None})
            if response.ok:
                response = response.json()
                streamlit.markdown(response['message'])
                streamlit.code(response['task_id'], language='text')
            else:
                streamlit.error(response.text)
        elif uploaded_file is not None and image is not None and uploaded_file.type != 'application/pdf':
            with streamlit.spinner('Converting'):
                response = asyncio.run(process_image(uploaded_file.getvalue(), user_instruction, system_instruction))
            if response:
                streamlit.code(response, language='latex')
            else:
                streamlit.error('An error occurred. Please try again.')
        elif paste_result.image_data is not None:
            with streamlit.spinner('Converting'):
                response = asyncio.run(process_image(image_bytes, user_instruction, system_instruction))
            if response:
                streamlit.code(response, language='latex')
            else:
                streamlit.error('An error occurred. Please try again.')
        else:
            streamlit.error('Please upload an image.')
