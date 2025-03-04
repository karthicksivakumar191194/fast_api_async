import re
import json
import gspread
from typing import List
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import CellFormat, TextFormat, format_cell_range

from app.models import Tenant
from app.settings import settings


ONBOARDED_TENANT_LIST_GSHEET_HEADERS = ["Tenant ID", "Status", "Company Name", "Owner Name", "Owner Email",
                                        "Workspace Name", "Business Location", "Business Country", "Industry",
                                        "Account Owner Handle", "Solutions Interested", "Team Size"]

async def add_tenant_details_to_admin_gsheet(tenant: Tenant, owner_name: str, owner_email: str):
    """
    Add tenant details to the admin Google Sheet based on the environment.
    """
    try:
        credentials_path = json.loads(settings.google_sheet_credentials)
        sheet_url = settings.admin_sheet_url

        # Define the scope and authenticate
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_path)
        client = gspread.authorize(creds)

        # Extract Spreadsheet ID and GID from URL
        sheet_id, gid = extract_sheet_id_and_gid(sheet_url)

        # Open spreadsheet
        spreadsheet = client.open_by_key(sheet_id)

        # Find the correct worksheet by GID
        worksheet = None
        if gid:
            for ws in spreadsheet.worksheets():
                if str(ws.id) == gid:
                    worksheet = ws
                    break
        if not worksheet:
            worksheet = spreadsheet.sheet1

            # Check if headers exist
        existing_headers = worksheet.row_values(1)
        if existing_headers != ONBOARDED_TENANT_LIST_GSHEET_HEADERS:
            worksheet.insert_row(ONBOARDED_TENANT_LIST_GSHEET_HEADERS, index=1)

            # Apply bold formatting to headers
            header_format = CellFormat(textFormat=TextFormat(bold=True))
            format_cell_range(worksheet, "A1:Z1", header_format)

        tenant_details = [
            str(tenant.id),
            tenant.company_name,
            owner_name,
            owner_email,
        ]

        worksheet.append_row(tenant_details)

        print("Tenant details successfully added to Google Sheet.")
    except Exception as e:
        print(f"Failed to add tenant details to Google Sheet: {e}")


async def update_tenant_details_to_admin_gsheet(tenant: Tenant):
    """
    Update tenant details to the admin Google Sheet based on the environment.
    """

    # TODO

    pass


def extract_sheet_id_and_gid(sheet_url: str):
    """
    Extract Spreadsheet ID and GID from the full Google Sheets URL.
    """
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url)
    gid_match = re.search(r"gid=(\d+)", sheet_url)

    if not match:
        raise ValueError("Invalid Google Sheet URL")

    sheet_id = match.group(1)
    gid = gid_match.group(1) if gid_match else None  # GID is optional
    return sheet_id, gid