# Authentication

This section describes how to authenticate with the API.

## Login Endpoint

**URL:** `/api/login`

**Method:** `POST`

**Sample Request:**

```json
{
  "username": "sampleuser",
  "password": "samplepassword"
}
```

**Response:**

```json
{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
```
