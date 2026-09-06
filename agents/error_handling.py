import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from schemas.review import ReviewFinding

load_dotenv()

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is required to run the Error Handling Agent."
        )

    return genai.Client(api_key=api_key)


def review_error_handling_changes(
    changes: list[dict]
) -> list[ReviewFinding]:

    if not changes:
        return []

    changed_code = "\n\n".join(
        f"File: {change['file']}\n"
        f"Line: {change['line']}\n"
        f"Code: {change['code']}"
        for change in changes
        if change["code"].strip()
    )

    prompt = f"""
You are a senior Python code reviewer specializing in reliability
and error handling.

Review the following changed lines from a GitHub pull request.

{changed_code}

Identify ONLY genuine error-handling or reliability problems.

Focus on:
- missing exception handling around operations that can fail
- database/API/file operations without appropriate failure handling
- silently ignored errors
- overly broad exception handling
- unsafe cleanup/resource handling
- code that can leave the application in an inconsistent state

Rules:
- Do not invent hypothetical issues.
- Ignore security vulnerabilities.
- Ignore generic style issues.
- For every genuine issue, return one finding.
- If there are no issues, return an empty list.
- Preserve the exact file and line number from the input.
- category must be "error_handling".

Return a JSON array of ReviewFinding objects.
"""

    client = get_client()

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": list[ReviewFinding],
                },
            )

            if not response.text:
                return []

            return [
                ReviewFinding.model_validate(item)
                for item in response.parsed
            ]

        except errors.ClientError as exc:
            if getattr(exc, "status_code", None) == 429:
                print(
                    "Error Handling Agent quota exhausted. "
                    "Returning no findings for this run."
                )
                return []
            raise

        except errors.ServerError:
            if attempt == 2:
                print(
                    "Error Handling Agent unavailable after 3 attempts. "
                    "Returning no findings for this run."
                )
                return []

            wait_time = 2 ** attempt
            print(
                f"Error Handling Agent retrying in {wait_time}s..."
            )
            time.sleep(wait_time)

    return []
