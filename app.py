from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import uvicorn
from extract import extract_csv_data
import traceback

app = FastAPI(title="CSV Data Extraction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HeaderMapping(BaseModel):
    header: str
    selected: str = ""
    sub_header1: Optional[str] = None
    selected1: Optional[str] = None
    sub_header2: Optional[str] = None
    selected2: Optional[str] = None
    sub_header3: Optional[str] = None
    selected3: Optional[str] = None

class HeaderInfo(BaseModel):
    header: str
    subHeaders: List[str] = []

class ExtractionRequest(BaseModel):
    excel_url: Optional[str] = None
    excel_headers: Optional[List[HeaderMapping]] = None
    csv: Optional[str] = None
    csvUrl: Optional[List[HeaderInfo]] = None
    exclude_photo: Optional[bool] = False

class ApiResponse(BaseModel):
    status_code: int
    status: bool
    data: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None

@app.post("/extract", response_model=ApiResponse)
async def extract_data(request: ExtractionRequest):
    """
    Extract data from a CSV file based on the provided header structure.
    
    Returns a response with status_code, status flag, and the extracted data.
    """
    try:
        # Handle the new format with csvUrl
        if request.csv and request.csvUrl:
            # Convert the new format for the extraction function
            headers_mapping = []
            
            for header_info in request.csvUrl:
                # Create minimal mapping with just the header info
                mapping = {
                    "header": header_info.header,
                    "selected": header_info.header, # Use the header name as the output field name
                    "use_subheaders": len(header_info.subHeaders) > 0 # Flag to indicate this has subheaders
                }
                
                # Add subheaders if present
                for i, subheader in enumerate(header_info.subHeaders[:3], 1):  # Only process first 3 subheaders
                    mapping[f"sub_header{i}"] = subheader
                    mapping[f"selected{i}"] = subheader  # Use the subheader name as its output field
                
                headers_mapping.append(mapping)
                
            # Call the extraction function with the simplified mapping
            result = extract_csv_data(
                csv_url=request.csv,
                headers_mapping=headers_mapping
            )
            
            # Remove Photo field if exclude_photo is True
            if request.exclude_photo:
                for row in result:
                    if "Photo" in row:
                        row["Photo"] = ""
            
            return ApiResponse(status_code=200, status=True, data=result)
            
        # Legacy format handling for backward compatibility
        elif request.excel_url and request.excel_headers:
            result = extract_csv_data(
                csv_url=request.excel_url,
                headers_mapping=request.excel_headers
            )
            
            # Remove Photo field if exclude_photo is True
            if request.exclude_photo:
                for row in result:
                    if "Photo" in row:
                        row["Photo"] = ""
            
            return ApiResponse(status_code=200, status=True, data=result)
        
        else:
            return ApiResponse(
                status_code=400, 
                status=False, 
                message="Missing required parameters: either csv and csvUrl, or excel_url and excel_headers"
            )
            
    except Exception as e:
        error_detail = f"Error extracting data: {str(e)}"
        print(f"{error_detail}\n{traceback.format_exc()}")  # Log the full error for debugging
        return ApiResponse(status_code=500, status=False, message=error_detail)

@app.get("/", response_model=ApiResponse)
async def root():
    return ApiResponse(
        status_code=200, 
        status=True, 
        message="CSV Data Extraction API is running. Go to /docs for the API documentation."
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
