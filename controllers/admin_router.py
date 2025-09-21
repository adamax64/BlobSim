from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from controllers.auth_dependency import require_auth
from domain.admin_service import create_database_dump


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/db-dump", response_class=StreamingResponse)
def download_db_dump(_=Depends(require_auth)):
    """
    Returns a PostgreSQL database dump as a downloadable file for authenticated users.
    """
    try:
        data_stream, filename = create_database_dump()

        headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/octet-stream",
            "Cache-Control": "no-cache",
            "Connection": "close"
        }
        return StreamingResponse(
            data_stream,
            media_type="application/octet-stream",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate database dump: {str(e)}")
