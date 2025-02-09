import requests
import streamlit

if __name__ == '__main__':
    streamlit.set_page_config(page_title='Status')
    streamlit.title('Status')
    streamlit.markdown('Check the status of task.\n\n')
    # Create a box to input the task ID and a button to check the status
    task_id = streamlit.text_input('Task ID')
    if streamlit.button('Check status') or task_id:
        response = requests.get(f'http://127.0.0.1:8000/status/{task_id}')
        if response.ok:
            response = response.json()
            if response['status'] == 'complete':
                streamlit.success('Processing complete')
                # Display the result as latex
                streamlit.code(response['result'], language='latex')
            else:
                display_text = f'Pages processed: {response["processed_pages"]}/{response["total_pages"]}. Missing pages: {response["missing_pages"]}'
                streamlit.warning(f'Processing in progress. {display_text}')
                streamlit.code(response['result'], language='latex')
        else:
            streamlit.error(response.text)
