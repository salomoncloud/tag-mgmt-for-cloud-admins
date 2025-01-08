#!/usr/bin/env python3

from google.cloud.resourcemanager_v3.services.projects import ProjectsClient
from openpyxl import Workbook

# Replace this with your actual org ID, e.g., "123456789012"
ORG_ID = "YOUR_ORG_ID"

REQUIRED_LABELS = [
    "BU",
    "contact1",
    "contact2",
    "contact3",
    "owner",
    "TypeOfEnvironment",
    "Mandate_Code",
    "Description",
]

def main():
    # Instantiate the v3 ProjectsClient
    client = ProjectsClient()

    # Prepare Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "GCP Projects Tag Validation"

    # Header row
    header = ["Project ID", "Project Name"]
    for label in REQUIRED_LABELS:
        header.append(label + " Present?")
        header.append(label + " Value")
    ws.append(header)

    # Build the parent resource string:
    # "organizations/123456789012" (replace 123456789012 with your actual ID)
    parent_resource = f"organizations/{ORG_ID}"

    # List all projects under this org
    response = client.list_projects(parent=parent_resource)

    for project in response:
        # The v3 'Project' object has project_id, display_name, and labels
        project_id = project.project_id
        project_name = project.display_name or "N/A"
        labels = project.labels

        row_data = [project_id, project_name]

        for label_key in REQUIRED_LABELS:
            if label_key in labels and labels[label_key].strip():
                row_data.append("Yes")
                row_data.append(labels[label_key])
            else:
                row_data.append("No")
                row_data.append("")

        ws.append(row_data)

    # Save the Excel file
    output_file = "gcp_tag_report.xlsx"
    wb.save(output_file)
    print(f"Tag validation complete. Report saved to {output_file}")

if __name__ == "__main__":
    main()
