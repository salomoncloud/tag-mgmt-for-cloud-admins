#!/usr/bin/env python3

import boto3
from openpyxl import Workbook

REQUIRED_TAGS = [
    "Contact 1",
    "Contact 2",
    "Contact 3",
    "Owner",
    "BU",
    "Description",
    "Mandate Code",
    "Mandate code",
    "Client",
    "Customer",
    "Type",
    "Confidentiality",
    "Type of environment",
    "TypeOfEnvironment",
]

def main():
    org_client = boto3.client("organizations")

    # Prepare the Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "AWS Account Tag Validation"

    # Build the header row
    header = ["Account ID", "Account Name"]
    for tag_key in REQUIRED_TAGS:
        header.append(f"{tag_key} Present?")
        header.append(f"{tag_key} Value")
    ws.append(header)

    # Use a paginator to list all accounts in the org
    paginator = org_client.get_paginator("list_accounts")

    for page in paginator.paginate():
        accounts = page["Accounts"]
        for account in accounts:
            # account["Id"] is the 12-digit numeric ID, e.g. "123456789012"
            account_id = account["Id"]
            account_name = account["Name"]

            # Retrieve the tags for this account
            tag_response = org_client.list_tags_for_resource(ResourceId=account_id)
            # Convert list of {Key, Value} into a dictionary
            tags_dict = {t["Key"]: t["Value"] for t in tag_response["Tags"]}

            # Build a row for Excel output
            row_data = [account_id, account_name]

            # Check each required tag
            for required_tag in REQUIRED_TAGS:
                if required_tag in tags_dict and tags_dict[required_tag].strip():
                    row_data.append("Yes")
                    row_data.append(tags_dict[required_tag])
                else:
                    row_data.append("No")
                    row_data.append("")

            ws.append(row_data)

    # Save the Excel file
    output_file = "aws_tag_report.xlsx"
    wb.save(output_file)
    print(f"Tag validation complete. Report saved to {output_file}")

if __name__ == "__main__":
    main()