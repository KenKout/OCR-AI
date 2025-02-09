import asyncio
import uuid
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger

from app.config import config
from app.models.pdf import PDFModel, PDFTables
from app.models.result import ResultModel, ResultTables
from app.utils.ocr import process_image
from app.utils.process_pdf import ProcessPDF

router = APIRouter(prefix='/pdf')


class BackgroundTask:
    def __init__(self):
        self.pdf_tables = PDFTables()
        self.result_tables = ResultTables()

    async def process_pdf(self, pdf_id: str, file_path: str, user_instruction: str, system_instruction: str):
        # Split the PDF into images
        images = ProcessPDF(file_path).split_pdf_into_images()

        # Insert PDF metadata into the database
        insert = PDFModel(pdf_id=pdf_id, pages=len(images))
        await self.pdf_tables.insert_pdf(insert)

        # Process the images concurrently using asyncio
        tasks = [
            process_image(image, user_instruction, system_instruction)
            for image in images
        ]

        # Gather results asynchronously
        results = await asyncio.gather(*tasks)

        # Insert results into the database
        for i, result in enumerate(results):
            logger.info(f'Result: {result}')
            insert = ResultModel(pdf_id=pdf_id, page=i, text=result)
            await self.result_tables.insert_result(insert)


@router.post('/submit')
async def submit_pdf(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        user_instruction: Optional[str] = Form(None),
        system_instruction: Optional[str] = Form(None)):
    pdf_id = str(uuid.uuid4())
    file_path = f"{config.BASE_DIR}/downloads/{pdf_id}.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Submit the task to BackgroundTask
    background_task = BackgroundTask()
    background_tasks.add_task(background_task.process_pdf, pdf_id, file_path, user_instruction, system_instruction)

    # Return the task_id
    return JSONResponse(content={"task_id": pdf_id, "message": "PDF processing started, go to the status page to check the status"})
