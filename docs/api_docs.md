# MoMo Transactions API Documentation

## Base URL

```text
http://localhost:3030
```

## Authentication

All endpoints require Basic Authentication.

```text
Username: admin
Password: momo2024
```

This tells whoever tests your API that they must include login credentials.

For example:

```bash
curl -u admin:momo2024 http://localhost:3030/transactions
```
---

## GET /transactions

Returns all available transactions stored in the system.

### Method

GET

### Endpoint

```text
/transactions
```

### Request Example

```bash
curl -u admin:momo2024 http://localhost:3030/transactions
```
### Response Example

```json
{
  "total": 1693,
  "limit": 50,
  "offset": 0,
  "count": 50,
  "data": [
    {
      "id": 1,
      "address": "M-Money",
      "date": "1715351458724",
      "readable_date": "10 May 2024 4:30:58 PM",
      "body": "You have received 2000 RWF from Jane Smith...",
      "type": "1",
      "read": "1"
    }
  ]
}
```

### Success Code

| Code | Description |
|--------|-------------|
| 200 OK | Transactions retrieved successfully |

### Error Codes

| Code | Description |
|--------|-------------|
| 401 Unauthorized | Missing or invalid username/password |
| 404 Not Found | Endpoint does not exist |
| 500 Internal Server Error | Unexpected server error |
---

## POST /transactions

Creates a new transaction.

### Method

POST

### Endpoint

```text
/transactions
```

### Request Example

```bash
curl -u admin:momo2024 -X POST http://localhost:3030/transactions \
-H "Content-Type: application/json" \
-d '{
  "address": "M-Money",
  "date": "1715351458724",
  "readable_date": "30 May 2026 10:00 AM",
  "body": "Test transaction of 5000 RWF",
  "type": "1",
  "read": "1"
}'
```

### Response Example

```json
{
  "id": 1694,
  "address": "M-Money",
  "date": "1715351458724",
  "readable_date": "30 May 2026 10:00 AM",
  "body": "Test transaction of 5000 RWF",
  "type": "1",
  "read": "1"
}
```

### Success Code

| Code | Description |
|--------|-------------|
| 201 Created | Transaction created successfully |

### Error Codes

| Code | Description |
|--------|-------------|
| 400 Bad Request | Invalid JSON body |
| 401 Unauthorized | Missing or invalid credentials |
| 404 Not Found | Endpoint does not exist |
---

## PUT /transactions/{id}

Updates an existing transaction.

### Method

PUT

### Endpoint

```text
/transactions/{id}
```

### Request Example

```bash
curl -u admin:momo2024 -X PUT http://localhost:3030/transactions/1 \
-H "Content-Type: application/json" \
-d '{
  "body": "Updated transaction body"
}'
```

### Response Example

```json
{
  "id": 1,
  "address": "M-Money",
  "date": "1715351458724",
  "readable_date": "10 May 2024 4:30:58 PM",
  "body": "Updated transaction body",
  "type": "1",
  "read": "1"
}
```

### Success Code

| Code | Description |
|--------|-------------|
| 200 OK | Transaction updated successfully |

### Error Codes

| Code | Description |
|--------|-------------|
| 400 Bad Request | Invalid JSON body |
| 401 Unauthorized | Missing or invalid credentials |
| 404 Not Found | Transaction not found |
---

## DELETE /transactions/{id}

Deletes a transaction.

### Method

DELETE

### Endpoint

```text
/transactions/{id}
```

### Request Example

```bash
curl -u admin:momo2024 -X DELETE http://localhost:3030/transactions/1
```

### Response Example

```json
{
  "message": "Transaction 1 deleted successfully"
}
```

### Success Code

| Code | Description |
|--------|-------------|
| 200 OK | Transaction deleted successfully |

### Error Codes

| Code | Description |
|--------|-------------|
| 401 Unauthorized | Missing or invalid credentials |
| 404 Not Found | Transaction not found |