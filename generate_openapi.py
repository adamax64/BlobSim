from pathlib import Path
from fastapi.openapi.utils import get_openapi
from main import app


def generate_openapi_json(output_file: Path):
    with open(output_file, "w") as f:
        import json
        json.dump(get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        ), f, indent=2)


if __name__ == "__main__":
    output_file = Path("web-ui/openapi.json")
    generate_openapi_json(output_file)
