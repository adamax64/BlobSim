import json
from pathlib import Path
from main import app  # Import the FastAPI app from main.py


def generate_openapi_json(output_path: str):
    openapi_schema = app.openapi()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"OpenAPI JSON has been written to {output_path}")


if __name__ == "__main__":
    output_file = Path("d:/SoftwareDevelopement/BlobSim/web-ui/openapi.json")
    generate_openapi_json(output_file)
