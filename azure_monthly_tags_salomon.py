#!/usr/bin/env python3

import os
from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient
from openpyxl import Workbook

# Define your required tags
REQUIRED_TAGS = [
    "Contact 1",
    "Contact 2",
    "Contact 3",
    "Contact1",
    "Contact2",
    "Contact3",
    "Contact4",
    "Owner",
    "owner",
    "Approver",
    "BU",
    "Description",
    "Mandate Code",
    "MandateCode",
    "Mandate code",
    "Client",
    "Customer",
    "PersonalData",
    "Type",
    "Confidentiality",
    "Type of environment",
    "TypeOfEnvironment",
]

def main():
    credential = AzureCliCredential()

    subscription_client = SubscriptionClient(credential)

    wb = Workbook()
    ws = wb.active
    ws.title = "Azure Subscription Tag Validation"

    header = ["Subscription ID", "Subscription Name"]
    for tag_key in REQUIRED_TAGS:
        header.append(f"{tag_key} Present?")
        header.append(f"{tag_key} Value")
    ws.append(header)

    print("Fetching subscriptions from Azure...")
    subscriptions = subscription_client.subscriptions.list()

    for sub in subscriptions:
        sub_id = sub.subscription_id
        sub_name = sub.display_name
        
        sub_tags = sub.tags or {}

        row_data = [sub_id, sub_name]

        for tag_key in REQUIRED_TAGS:

            if tag_key in sub_tags and sub_tags[tag_key].strip():
                row_data.append("Yes")
                row_data.append(sub_tags[tag_key])
            else:
                row_data.append("No")
                row_data.append("")

        ws.append(row_data)

    output_file = "azure_sub_tag_report.xlsx"
    wb.save(output_file)

    print(f"Tag validation complete. Report saved to {output_file}")

if __name__ == "__main__":
    main()
