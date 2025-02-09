from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger

from app.models.pdf import PDFTables
from app.models.result import ResultTables

router = APIRouter(prefix='/status')


@router.get("/{task_id}")
async def check_status(task_id: str):
    logger.info(f'Task ID: {task_id}')
    result_tables = ResultTables()
    pdf_tables = PDFTables()

    pdf = await pdf_tables.get_pdf_by_id(task_id)
    try:
        pdf = dict(pdf)
    except TypeError:
        return JSONResponse(content={"status": "processing", "result": "Your PDF is still being processed or not found", "processed_pages": 0, "total_pages": 0, "missing_pages": []})

    if not pdf:
        return JSONResponse(content={"status": "processing", "result": "Your PDF is still being processed or not found", "processed_pages": 0, "total_pages": 0, "missing_pages": []})

    results = await result_tables.get_result_by_pdf_id(task_id)
    results = list(results)

    if not results:
        return JSONResponse(content={"status": "processing", "result": "Processing in progress", "processed_pages": 0, "total_pages": pdf['pages'], "missing_pages": [i+1 for i in range(pdf['pages'])]})

    if len(results) > 0:
        return_data = ""
        for result in results:
            return_data += result["text"]

        status = "complete" if len(results) == pdf["pages"] else "processing"
        missing_pages = [i+1 for i in range(pdf["pages"]) if i not in [res["page"] for res in results]]
        return {"status": status, "result": return_data, "processed_pages": len(results), "total_pages": pdf["pages"], "missing_pages": missing_pages}
    else:
        return {"status": "processing", "result": "Processing in progress", "processed_pages": 0, "total_pages": pdf["pages"], "missing_pages": [i+1 for i in range(pdf["pages"])]}
