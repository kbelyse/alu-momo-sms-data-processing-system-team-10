# Transaction API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

This API uses **HTTP Basic Authentication**. All requests must include an `Authorization` header with valid credentials.

### Credentials
- **Username:** `admin`
- **Password:** `password123`

### Authentication Header Format
```
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

The value after "Basic" is the base64-encoded string of `username:password`.

---

## Endpoints

### 1. Get All Transactions

Retrieve a list of all transactions.

**Endpoint:** `GET /transactions`

**Authentication:** Required

**Parameters:** None

**Response:**

```json
{
  "success": true,
  "count": 150,
  "data": [
    {
      "id": 1,
      "protocol": "0",
      "address": "+250788123456",
      "date": "1609459200000",
      "type": "1",
      "subject": "null",
      "body": "Your transaction of RWF 5000 was successful",
      "toa": "null",
      "sc_toa": "null",
      "service_center": "null",
      "read": "1",
      "status": "-1",
      "locked": "0",
      "date_sent": "1609459200000",
      "readable_date": "2021-01-01 00:00:00",
      "contact_name": "Bank"
    },
    {
      "id": 2,
      "protocol": "0",
      "address": "+250788654321",
      "date": "1609545600000",
      "type": "2",
      "subject": "null",
      "body": "Payment received: RWF 3000",
      "toa": "null",
      "sc_toa": "null",
      "service_center": "null",
      "read": "1",
      "status": "-1",
      "locked": "0",
      "date_sent": "1609545600000",
      "readable_date": "2021-01-02 00:00:00",
      "contact_name": "MoMo"
    }
  ]
}
```

**Status Code:** `200 OK`

---

### 2. Get Transaction by ID

Retrieve a specific transaction by its ID.

**Endpoint:** `GET /transactions/{id}`

**Authentication:** Required

**Parameters:**

| Parameter | Type    | Location | Description                    |
|-----------|---------|----------|--------------------------------|
| id        | integer | Path     | Unique identifier of transaction |

**Example Request:**

```bash
curl -X GET http://localhost:8000/transactions/1 \
  -u admin:password123
```

**Success Response:**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "protocol": "0",
    "address": "+250788123456",
    "date": "1609459200000",
    "type": "1",
    "subject": "null",
    "body": "Your transaction of RWF 5000 was successful",
    "toa": "null",
    "sc_toa": "null",
    "service_center": "null",
    "read": "1",
    "status": "-1",
    "locked": "0",
    "date_sent": "1609459200000",
    "readable_date": "2021-01-01 00:00:00",
    "contact_name": "Bank"
  }
}
```

**Status Code:** `200 OK`

**Error Response (Not Found):**

```json
{
  "error": true,
  "message": "Transaction with ID 999 not found"
}
```

**Status Code:** `404 Not Found`

---

### 3. Create New Transaction

Create a new transaction record.

**Endpoint:** `POST /transactions`

**Authentication:** Required

**Request Body:**

```json
{
  "protocol": "0",
  "address": "+250788999888",
  "date": "1633024800000",
  "type": "1",
  "subject": "null",
  "body": "New transaction: RWF 10000",
  "toa": "null",
  "sc_toa": "null",
  "service_center": "null",
  "read": "1",
  "status": "-1",
  "locked": "0",
  "date_sent": "1633024800000",
  "readable_date": "2021-10-01 00:00:00",
  "contact_name": "Customer"
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "protocol": "0",
    "address": "+250788999888",
    "date": "1633024800000",
    "type": "1",
    "body": "New transaction: RWF 10000",
    "readable_date": "2021-10-01 00:00:00",
    "contact_name": "Customer"
  }'
```

**Success Response:**

```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "id": 151,
    "protocol": "0",
    "address": "+250788999888",
    "date": "1633024800000",
    "type": "1",
    "body": "New transaction: RWF 10000",
    "readable_date": "2021-10-01 00:00:00",
    "contact_name": "Customer"
  }
}
```

**Status Code:** `201 Created`

**Note:** The `id` field is automatically assigned by the server and should not be included in the request body.

---

### 4. Update Transaction

Update an existing transaction by ID.

**Endpoint:** `PUT /transactions/{id}`

**Authentication:** Required

**Parameters:**

| Parameter | Type    | Location | Description                    |
|-----------|---------|----------|--------------------------------|
| id        | integer | Path     | Unique identifier of transaction |

**Request Body:**

```json
{
  "protocol": "0",
  "address": "+250788123456",
  "date": "1609459200000",
  "type": "1",
  "subject": "null",
  "body": "Updated transaction: RWF 5500",
  "toa": "null",
  "sc_toa": "null",
  "service_center": "null",
  "read": "1",
  "status": "-1",
  "locked": "0",
  "date_sent": "1609459200000",
  "readable_date": "2021-01-01 00:00:00",
  "contact_name": "Bank"
}
```

**Example Request:**

```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "protocol": "0",
    "address": "+250788123456",
    "body": "Updated transaction: RWF 5500",
    "readable_date": "2021-01-01 00:00:00",
    "contact_name": "Bank"
  }'
```

**Success Response:**

```json
{
  "success": true,
  "message": "Transaction updated successfully",
  "data": {
    "id": 1,
    "protocol": "0",
    "address": "+250788123456",
    "body": "Updated transaction: RWF 5500",
    "readable_date": "2021-01-01 00:00:00",
    "contact_name": "Bank"
  }
}
```

**Status Code:** `200 OK`

**Note:** The entire transaction object is replaced. The `id` in the URL is preserved.

---

### 5. Delete Transaction

Delete a transaction by ID.

**Endpoint:** `DELETE /transactions/{id}`

**Authentication:** Required

**Parameters:**

| Parameter | Type    | Location | Description                    |
|-----------|---------|----------|--------------------------------|
| id        | integer | Path     | Unique identifier of transaction |

**Example Request:**

```bash
curl -X DELETE http://localhost:8000/transactions/1 \
  -u admin:password123
```

**Success Response:**

```json
{
  "success": true,
  "message": "Transaction 1 deleted successfully"
}
```

**Status Code:** `200 OK`

**Error Response (Not Found):**

```json
{
  "error": true,
  "message": "Transaction with ID 999 not found"
}
```

**Status Code:** `404 Not Found`

---

## Error Codes

### HTTP Status Codes

| Status Code | Description                                      |
|-------------|--------------------------------------------------|
| 200         | OK - Request succeeded                           |
| 201         | Created - Resource created successfully          |
| 204         | No Content - Preflight request succeeded         |
| 400         | Bad Request - Invalid input or malformed request |
| 401         | Unauthorized - Missing or invalid credentials    |
| 404         | Not Found - Resource doesn't exist               |
| 500         | Internal Server Error - Server-side error        |

### Common Error Responses

#### 401 Unauthorized

Occurs when authentication credentials are missing or invalid.

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing credentials"
}
```

#### 400 Bad Request

Occurs when the request contains invalid data.

```json
{
  "error": true,
  "message": "Invalid JSON data"
}
```

or

```json
{
  "error": true,
  "message": "Invalid transaction ID"
}
```

#### 404 Not Found

Occurs when the requested resource doesn't exist.

```json
{
  "error": true,
  "message": "Transaction with ID 123 not found"
}
```

or

```json
{
  "error": true,
  "message": "Endpoint not found"
}
```

#### 500 Internal Server Error

Occurs when an unexpected server error happens.

```json
{
  "error": true,
  "message": "Server error: [error details]"
}
```

---

## Transaction Object Schema

| Field           | Type   | Description                                    |
|-----------------|--------|------------------------------------------------|
| id              | int    | Unique identifier (auto-generated)             |
| protocol        | string | SMS protocol identifier                        |
| address         | string | Phone number or address                        |
| date            | string | Timestamp in milliseconds                      |
| type            | string | Message type (1=received, 2=sent)              |
| subject         | string | Message subject (usually "null")               |
| body            | string | Message content/transaction details            |
| toa             | string | Type of address                                |
| sc_toa          | string | Service center type of address                 |
| service_center  | string | Service center address                         |
| read            | string | Read status (0=unread, 1=read)                 |
| status          | string | Message status                                 |
| locked          | string | Lock status (0=unlocked, 1=locked)             |
| date_sent       | string | Sent timestamp in milliseconds                 |
| readable_date   | string | Human-readable date (YYYY-MM-DD HH:MM:SS)      |
| contact_name    | string | Contact name associated with transaction       |

---

## CORS Support

The API includes CORS headers to allow cross-origin requests:

- **Access-Control-Allow-Origin:** `*`
- **Access-Control-Allow-Methods:** `GET, POST, PUT, DELETE, OPTIONS`
- **Access-Control-Allow-Headers:** `Content-Type, Authorization`

---

## Usage Examples

### Python Example

```python
import requests
from requests.auth import HTTPBasicAuth

# Base URL
base_url = "http://localhost:8000"

# Authentication
auth = HTTPBasicAuth('admin', 'password123')

# Get all transactions
response = requests.get(f"{base_url}/transactions", auth=auth)
print(response.json())

# Get specific transaction
response = requests.get(f"{base_url}/transactions/1", auth=auth)
print(response.json())

# Create new transaction
new_transaction = {
    "address": "+250788999888",
    "body": "Test transaction",
    "readable_date": "2024-01-01 12:00:00",
    "contact_name": "Test User"
}
response = requests.post(f"{base_url}/transactions", json=new_transaction, auth=auth)
print(response.json())

# Update transaction
updated_data = {
    "address": "+250788999888",
    "body": "Updated transaction",
    "readable_date": "2024-01-01 12:00:00",
    "contact_name": "Test User"
}
response = requests.put(f"{base_url}/transactions/1", json=updated_data, auth=auth)
print(response.json())

# Delete transaction
response = requests.delete(f"{base_url}/transactions/1", auth=auth)
print(response.json())
```
## Notes

- All endpoints require authentication using HTTP Basic Auth
- The server runs on port 8000 by default
- Transaction IDs are auto-incremented and cannot be manually set
- The API uses JSON for all request and response bodies
- CORS is enabled for all origins
- The server loads transaction data from `../data/modified_sms_v2.xml` on startup
- Changes are stored in memory and will be lost when the server restarts