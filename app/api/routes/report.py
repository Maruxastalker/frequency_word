"""
API-роутер для экспорта отчётов.
"""

import os
import asyncio

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from app.application.services.report_service import ReportExportService

router = APIRouter(tags=["Reports"])

MAX_CONCURRENT_EXPORTS = 3
MAX_FILE_SIZE = 500 * 1024 * 1024
EXPORT_TIMEOUT = 300 

_export_semaphore = asyncio.Semaphore(MAX_CONCURRENT_EXPORTS)


def _cleanup_file(path: str) -> None:
    """Удалить временный файл после отправки."""
    try:
        if os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass


@router.post(
    "/public/report/export",
    summary="Экспорт частотного анализа в Excel",
    description=(
        "Принимает текстовый файл, выполняет частотный анализ словоформ "
        "(приведение к леммам) и возвращает xlsx-файл с тремя столбцами: "
        "лемма, общее количество, распределение по строкам."
    ),
    response_class=FileResponse,
)
async def export_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Текстовый файл для анализа"),
):
    """
    POST /public/report/export
    
    Принимает: текстовый файл (multipart/form-data)
    Возвращает: xlsx-файл с частотным анализом
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Файл не передан.")

    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"Файл слишком большой"
        )

    try:
        service = ReportExportService()

        try:
            xlsx_path = await asyncio.wait_for(
                service.export(file),
                timeout=EXPORT_TIMEOUT,
            )

        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail=f"Превышено время обработки ({EXPORT_TIMEOUT} секунд)"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке файла: {str(e)}"
        )
    finally:
        _export_semaphore.release()
        await file.close()
        

    background_tasks.add_task(_cleanup_file, xlsx_path)

    return FileResponse(
        path=xlsx_path,
        filename="frequency_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.document",
    )
