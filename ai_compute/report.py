"""Generate JSON and PDF reports for AutoHS jobs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_json_report(output_dir: Path, job_id: str, metrics: dict[str, Any], meta: dict[str, Any]) -> Path:
    payload = {
        "job_id": job_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "meta": meta,
    }
    path = output_dir / "report.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_pdf_report(output_dir: Path, job_id: str, metrics: dict[str, Any], meta: dict[str, Any]) -> Path:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError as exc:
        raise ImportError("reportlab is required for PDF reports") from exc

    pdf_path = output_dir / "report.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AutoHS — Hippocampal Asymmetry Report", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Job ID: {job_id}", styles["Normal"]))
    story.append(Paragraph(f"Input: {meta.get('input_file', 'N/A')}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    rows = [
        ["Metric", "Value"],
        ["Left hippocampus (mm³)", str(metrics["left_hippocampus_mm3"])],
        ["Right hippocampus (mm³)", str(metrics["right_hippocampus_mm3"])],
        ["Asymmetry index (AI)", str(metrics["asymmetry_index"])],
        ["Laterality", metrics["laterality"]],
        ["HS classification", metrics["hs_classification"]],
    ]
    table = Table(rows, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003d7a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "Formula: AI = (L − R) / (L + R). See Ndagijimana et al., Brain Communications (in press).",
            styles["Italic"],
        )
    )

    doc.build(story)
    return pdf_path


def write_text_summary(output_dir: Path, job_id: str, metrics: dict[str, Any]) -> Path:
    path = output_dir / "summary.txt"
    lines = [
        f"AutoHS job {job_id}",
        f"Left hippocampus:  {metrics['left_hippocampus_mm3']} mm³",
        f"Right hippocampus: {metrics['right_hippocampus_mm3']} mm³",
        f"Asymmetry index:   {metrics['asymmetry_index']}",
        f"Laterality:        {metrics['laterality']}",
        f"HS classification: {metrics['hs_classification']}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
