# TEAM 7 
# MoMo SMS Data Processing System

## Project Overview
This system processes MTN Mobile Money (MoMo) SMS transaction data. It parses XML-formatted SMS messages, extracts transaction details, and stores them in a structured MySQL database for querying and analysis.

# Team Members
- Divin Semana  
- Butera Irebe Asnath  
- Rusanganwa Arnaud Bertrand

# System Architecture
[View System Architecture](https://drive.google.com/file/d/1cMTkPHRwWionifNjws3VCFswhx6vTrAZ/view?usp=sharing)
![image](momo.jpg)
# ScrumBoard - Project
[View Project scrumboard here](https://github.com/users/dsemana/projects/3/views/1)

## Database Design

### How to Run the SQL Script
1. Make sure MySQL is installed and running
2. Open your terminal or MySQL Workbench
3. Run: `mysql -u root -p < database/database_setup.sql`
4. The database `momo_sms` will be created with all tables and sample data

# ERD Design
![image_erd](docs/erd_diagram.png)

# REST API Extension (Assignment 2)

## Overview

Building upon the MoMo SMS Data Processing System developed in the previous assignment, this phase introduces a secure REST API that allows external applications to interact with transaction data through standard HTTP requests.

The API parses transaction records from the XML dataset, exposes CRUD operations, secures endpoints using Basic Authentication, and demonstrates the application of Data Structures and Algorithms (DSA) through search performance comparisons.

## New Features Added

### XML Parsing

The system reads transaction records from the provided `modified_sms_v2.xml` dataset and converts them into JSON objects that can be processed by the API.

### REST API Endpoints

| Method | Endpoint           | Description                     |
| ------ | ------------------ | ------------------------------- |
| GET    | /transactions      | Retrieve all transactions       |
| GET    | /transactions/{id} | Retrieve a specific transaction |
| POST   | /transactions      | Create a new transaction        |
| PUT    | /transactions/{id} | Update an existing transaction  |
| DELETE | /transactions/{id} | Delete a transaction            |

### Authentication

The API uses Basic Authentication to restrict access to authorized users.

**Credentials**

```text
Username: admin
Password: momo2024
```

Unauthorized requests return:

```json
{
  "error": "Unauthorized: invalid or missing credentials"
}
```

## API Project Structure

```text
MoMo-SMS/
├── api/
│   └── server.py
├── dsa/
│   ├── parse_xml.py
│   └── search_compare.py
├── docs/
│   └── api_docs.md
├── screenshots/
├── modified_sms_v2.xml
├── database/
│   └── database_setup.sql
├── README.md
└── transactions.json
```

## Running the API

Start the server:

```bash
python api/server.py
```

The API runs at:

```text
http://localhost:3030
```

## API Documentation

Detailed API documentation can be found in:

```text
docs/api_docs.md
```

The documentation includes:

* Endpoint descriptions
* Request examples
* Response examples
* Error codes
* Authentication requirements

## DSA Integration

To evaluate search efficiency, two search methods were implemented and compared:

### Linear Search

Linear search scans each transaction one at a time until a matching transaction ID is found.

**Time Complexity**

```text
O(n)
```

### Dictionary Lookup

Dictionary lookup stores transactions using transaction IDs as keys, allowing direct access.

**Time Complexity**

```text
O(1)
```

### Results

Testing demonstrated that dictionary lookup performs significantly faster than linear search because records can be accessed directly without scanning the entire collection.

## Security Discussion

Although Basic Authentication was implemented successfully, it has several limitations:

* Credentials are transmitted with every request.
* Credentials may be exposed if HTTPS is not used.
* No token expiration mechanism exists.
* Limited scalability for larger systems.

For production systems, stronger authentication methods such as JWT (JSON Web Tokens) or OAuth 2.0 are recommended.

## Testing

The API was tested using curl/Postman with the following scenarios:

* Successful authenticated GET request
* Unauthorized request with invalid credentials
* Successful POST request
* Successful PUT request
* Successful DELETE request



