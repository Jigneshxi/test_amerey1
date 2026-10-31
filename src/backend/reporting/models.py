from datetime import datetime
from typing import List, Dict, Any

from pydantic import BaseModel, validator

class ReportData(BaseModel):
    """
    Represents a single row of data in a report.
    This is a base class and can be extended to include more specific data.
    """
    product_id: str
    date: datetime
    sales_volume: int
    revenue: float

class ReportRequest(BaseModel):
    """
    Model for request body of report generation endpoints.
    """
    date_range: str

    @validator('date_range')
    def validate_date_range(cls, value):
        try:
            # Expected format: "YYYY-MM-DD to YYYY-MM-DD"
            start_date_str, end_date_str = value.split(" to ")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if start_date > end_date:
                raise ValueError("Start date must be before end date.")

            return (start_date, end_date)

        except ValueError as e:
            raise ValueError(f"Invalid date range format. Expected YYYY-MM-DD to YYYY-MM-DD. Error: {e}")


class ReportSummary(BaseModel):
    """
    Summary of a generated report, used for caching and tracking.
    """
    report_id: str
    date_range: str
    data_count: int
    generated_at: datetime
    status: str  # e.g., "success", "failed"
    error_message: str = None