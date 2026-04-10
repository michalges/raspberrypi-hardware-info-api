import json
from fastapi import Request, Response

# Middleware to convert JSON keys from snake_case to camelCase


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.capitalize() for x in components[1:])


def convert_keys_to_camel_case(obj):
    if isinstance(obj, dict):
        return {
            to_camel_case(key): convert_keys_to_camel_case(value)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [convert_keys_to_camel_case(item) for item in obj]
    else:
        return obj


async def change_to_camel_case(request: Request, call_next):
    response = await call_next(request)

    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            data = json.loads(body.decode())
            camel_case_data = convert_keys_to_camel_case(data)
            modified_body = json.dumps(camel_case_data).encode()

            new_headers = dict(response.headers)
            new_headers["content-length"] = str(len(modified_body))

            return Response(
                content=modified_body,
                status_code=response.status_code,
                headers=new_headers,
                media_type="application/json",
            )
        except json.JSONDecodeError:
            pass

    return Response(
        content=body, status_code=response.status_code, headers=dict(response.headers)
    )
