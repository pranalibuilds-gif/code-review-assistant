from typing import List, Dict
import json
from app.analyzers.schemas import NormalizedFinding, NormalizedMetric

class PromptBuilder:
    @staticmethod
    def build_review_prompt(
        language: str,
        files_content: Dict[str, str],
        static_findings: List[NormalizedFinding],
        metrics: List[NormalizedMetric]
    ) -> str:
        """
        Assembles a comprehensive prompt for the AI reviewer.
        """

        findings_summary = [
            f"- {f.severity.value}: {f.title} ({f.file_path}:{f.line})"
            for f in static_findings
        ]

        metrics_summary = [
            f"- {m.metric_name}: {m.metric_value} {m.unit if m.unit else ''}"
            for m in metrics
        ]

        code_samples = []
        for path, content in list(files_content.items())[:5]:  # Limit to 5 files for context size
            code_samples.append(f"File: {path}\n```python\n{content[:2000]}\n```") # Limit content per file

        prompt = f"""
You are a Senior Software Engineer and Mentor. Review the following {language} code project.

CONTEXT:
I have already performed static analysis. Here are the findings and metrics:

STATIC FINDINGS:
{chr(10).join(findings_summary) if findings_summary else "No major issues found by static analyzers."}

METRICS:
{chr(10).join(metrics_summary) if metrics_summary else "Metrics not available."}

CODE SAMPLES:
{chr(10).join(code_samples)}

INSTRUCTIONS:
1. Provide a brief high-level summary of the code quality.
2. Provide an overall assessment (e.g. Excellent, Good, Fair, Needs Improvement).
3. Identify 3-5 additional findings that static analysis might have missed (e.g. logic errors, bad naming, architectural issues).
4. Provide 3 actionable recommendations for the developer to improve their skills.

RESPONSE FORMAT:
You MUST return a valid JSON object with the following structure:
{{
  "summary": "string",
  "overall_assessment": "string",
  "findings": [
    {{
      "source": "AI",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
      "category": "string",
      "title": "string",
      "description": "string",
      "recommendation": "string",
      "file_path": "string",
      "line": integer
    }}
  ],
  "recommendations": [
    {{
      "title": "string",
      "description": "string",
      "impact": "string"
    }}
  ]
}}

Ensure all fields are present. Use your best professional judgment.
"""
        return prompt
