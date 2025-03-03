~~# API Responses

This document describes the common responses format that the API will return.

---

## Success

### Status: `201 Created`

### Sample Success Response:
```json
{
    "message": "Created message"
}
```

## Error

### Status: `400 Bad Request`

### Sample Error Response:
```json
{
    "message": "Error message"
}
```

## Not Found

### Status: `404 Not Found`

### Sample Not Found Response:
```json
{
    "message": "Not found message"
}
```

## Validation Error

### Status: `422 Unprocessable Entity`

### Sample Validation Error Response:
```json
{
    "data": {
        "field_1": "Field required",
        "field_2": "Field required"
    },
    "message": "Validation error"
}
```

## Rate Limit Error

### Status: `429 Too Many Requests`

### Sample Error Response:
```json
{
    "message": "Rate limit exceeded. Please try again later."
}
```

