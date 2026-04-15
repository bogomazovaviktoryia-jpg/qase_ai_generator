from pathlib import Path
import openpyxl


def read_xlsx(path: Path) -> str:
    workbook = openpyxl.load_workbook(path, data_only=True)
    parts = []

    for sheet in workbook.worksheets:
        parts.append(f"# Sheet: {sheet.title}")
        for row in sheet.iter_rows(values_only=True):
            values = [str(cell).strip() for cell in row if cell is not None and str(cell).strip()]
            if values:
                parts.append(" | ".join(values))

    return "\n".join(parts)