from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from drf_spectacular.generators import SchemaGenerator

HTTP_METHOD_ORDER = ["get", "post", "put", "patch", "delete"]


def _schema_type_name(schema: dict[str, Any]) -> str:
    if not isinstance(schema, dict):
        return "-"
    if "$ref" in schema:
        return str(schema["$ref"]).split("/")[-1]
    type_name = schema.get("type")
    if type_name == "array":
        item_type = _schema_type_name(schema.get("items", {}))
        return f"array[{item_type}]"
    if type_name:
        return str(type_name)
    return "-"


def _render_parameter_table(parameters: list[dict[str, Any]]) -> list[str]:
    if not parameters:
        return ["- 无"]
    lines = [
        "| 参数 | 位置 | 必填 | 类型 | 说明 |",
        "|---|---|---|---|---|",
    ]
    for item in parameters:
        schema = item.get("schema") or {}
        lines.append(
            "| {name} | {location} | {required} | {type_name} | {description} |".format(
                name=item.get("name", "-"),
                location=item.get("in", "-"),
                required="是" if item.get("required") else "否",
                type_name=_schema_type_name(schema),
                description=(item.get("description") or "-").replace("\n", " ").strip(),
            )
        )
    return lines


def _render_request_body(request_body: dict[str, Any]) -> list[str]:
    if not request_body:
        return ["- 无"]
    content = request_body.get("content") or {}
    if not content:
        return ["- 无"]
    lines = []
    required = "是" if request_body.get("required") else "否"
    for content_type, schema_obj in content.items():
        schema = (schema_obj or {}).get("schema", {})
        lines.append(
            f"- `{content_type}`（必填：{required}，Schema：`{_schema_type_name(schema)}`）"
        )
    return lines


def _render_response_table(responses: dict[str, Any]) -> list[str]:
    if not responses:
        return ["- 无"]
    lines = [
        "| 状态码 | 说明 |",
        "|---|---|",
    ]
    sortable_items = []
    for code, payload in responses.items():
        try:
            sort_key = (0, int(code))
        except (TypeError, ValueError):
            sort_key = (1, str(code))
        sortable_items.append((sort_key, code, payload))
    sortable_items.sort(key=lambda item: item[0])
    for _, code, payload in sortable_items:
        description = "-"
        if isinstance(payload, dict):
            description = (payload.get("description") or "-").replace("\n", " ").strip()
        lines.append(f"| {code} | {description} |")
    return lines


class Command(BaseCommand):
    help = "Export API documentation markdown from drf-spectacular schema."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default=str(Path(settings.BASE_DIR).parent / "API_DOCS.md"),
            help="Target markdown file path. Defaults to repository root API_DOCS.md.",
        )
        parser.add_argument(
            "--schema-json",
            default=str(Path(settings.BASE_DIR) / "openapi-schema.json"),
            help="Target OpenAPI JSON output path.",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        schema_json_path = Path(options["schema_json"])
        project_root = Path(settings.BASE_DIR).parent

        generator = SchemaGenerator()
        schema = generator.get_schema(request=None, public=True)
        if not schema:
            raise CommandError("Failed to generate OpenAPI schema.")

        schema_dict = dict(schema)
        schema_json_path.parent.mkdir(parents=True, exist_ok=True)
        schema_json_path.write_text(
            json.dumps(schema_dict, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        grouped_operations: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for path, path_item in sorted(schema_dict.get("paths", {}).items(), key=lambda item: item[0]):
            if not isinstance(path_item, dict):
                continue
            for method in HTTP_METHOD_ORDER:
                operation = path_item.get(method)
                if not isinstance(operation, dict):
                    continue
                group = "管理端接口" if path.startswith("/api/admin/") else "用户端接口"
                grouped_operations[group].append(
                    {
                        "method": method.upper(),
                        "path": path,
                        "summary": operation.get("summary"),
                        "operation_id": operation.get("operationId") or "-",
                        "description": (operation.get("description") or "").strip(),
                        "tags": operation.get("tags") or [],
                        "parameters": operation.get("parameters") or [],
                        "request_body": operation.get("requestBody") or {},
                        "responses": operation.get("responses") or {},
                    }
                )

        info = schema_dict.get("info") or {}
        generated_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
        try:
            display_schema_path = str(schema_json_path.resolve().relative_to(project_root.resolve()))
        except ValueError:
            display_schema_path = str(schema_json_path)
        lines: list[str] = [
            f"# {info.get('title', 'API Documentation')}",
            "",
            f"- 版本：`{info.get('version', '-')}`",
            f"- 生成时间：`{generated_at}`",
            "- Schema 地址：`/api/schema/`",
            "- Swagger UI：`/api/docs/`",
            f"- OpenAPI JSON 文件：`{display_schema_path}`",
            "",
            "本文档由 `drf-spectacular` 生成的 OpenAPI Schema 自动整理。",
            "",
        ]

        for section_name in ["用户端接口", "管理端接口"]:
            operations = grouped_operations.get(section_name, [])
            lines.append(f"## {section_name}")
            lines.append("")
            lines.append(f"- 接口数量：`{len(operations)}`")
            lines.append("")
            for item in operations:
                description = item["description"] or "-"
                summary = item["summary"] or description.split(".")[0].strip() or item["operation_id"]
                lines.append(f"### `{item['method']} {item['path']}`")
                lines.append("")
                lines.append(f"- 概要：{summary}")
                lines.append(f"- 描述：{description}")
                if item["tags"]:
                    lines.append(f"- 标签：{', '.join(item['tags'])}")
                lines.append("- 查询/路径参数：")
                lines.extend(_render_parameter_table(item["parameters"]))
                lines.append("- 请求体：")
                lines.extend(_render_request_body(item["request_body"]))
                lines.append("- 响应：")
                lines.extend(_render_response_table(item["responses"]))
                lines.append("")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"OpenAPI JSON exported to: {schema_json_path}"))
        self.stdout.write(self.style.SUCCESS(f"Markdown API docs exported to: {output_path}"))
