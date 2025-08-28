# [API Name]

**Version:** 1.0  
**Last Updated:** YYYY-MM-DD  
**Status:** Draft | Review | Published

## Overview
Brief description of the API's purpose and functionality.

## Base URL
```
https://api.example.com/v1
```

## Authentication
Describe authentication method (API Key, OAuth, JWT, etc.)

## Endpoints

### [Endpoint Name]
**Method:** `GET | POST | PUT | DELETE`  
**Path:** `/endpoint/path/{parameter}`

#### Description
What this endpoint does.

#### Request Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | Yes | Description |
| param2 | integer | No | Description |

#### Request Headers
```http
Content-Type: application/json
Authorization: Bearer {token}
```

#### Request Body
```json
{
  "field1": "value",
  "field2": 123
}
```

#### Response
**Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "field1": "value"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Authentication failed
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

#### Example
```bash
curl -X GET "https://api.example.com/v1/endpoint" \
  -H "Authorization: Bearer {token}"
```

## Error Codes
| Code | Message | Description |
|------|---------|-------------|
| 1001 | Invalid input | The provided input is invalid |
| 1002 | Resource not found | The requested resource doesn't exist |

## Rate Limiting
- 100 requests per minute per API key
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Changelog
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial release |

## Support
Contact information for API support.