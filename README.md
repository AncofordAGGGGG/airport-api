# Airport Delay Analytics API

"COMP3011_Coursework1"

A RESTful API built with FastAPI for managing flight data, analysing delay patterns, and exploring airport connectivity using real-world flight datasets.

---

## Overview

This project implements a data-driven web API that allows users to:

- Manage flight records (CRUD operations)
- Discover reachable destinations from a given airport
- Analyse flight delay rates
- Analyse delay patterns by departure hour

The system is powered by real-world US flight data (2018–2024), ensuring realistic and meaningful analytics.

---

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy

---

## How to Run

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the API
```bash
python -m uvicorn app.main:app --reload
```
### 4. Open API documentation

http://127.0.0.1:8000/docs


---

## Data Source

The dataset is based on the US DOT On-Time Performance dataset (2018–2024). 
https://www.kaggle.com/datasets/shubhamsingh42/flight-delay-dataset-2018-2024?resource=download

It contains real flight-level records including:

Origin and destination airports

Scheduled and actual departure times

Delay durations

Flight numbers

This dataset enables realistic delay analysis and airport connectivity insights.

---

## Dataset Setup

This project uses a real-world flight dataset based on the US DOT On-Time Performance data (2018–2024).

Due to GitHub file size limitations, the dataset is **not included in the repository**.

### How to use the dataset

1. Download the dataset manually (e.g. from Kaggle or provided source)

2. Place the CSV file in the project root directory:
```
airport-api/
├── app/
├── scripts/
├── flight_data_2018_2024.csv ← place it here
```
3. Run the import script:

```bash
PYTHONPATH=. python scripts/import_flights.py
```
### Notes

The dataset file (~275MB) is excluded from GitHub to comply with file size limits.

Only a subset of the dataset (e.g. 30,000–50,000 rows) is recommended for performance during development.

The import script automatically:

converts time fields into datetime format

determines flight status (delayed or on_time) based on delay minutes

---

##API Endpoints

Flights CRUD

- POST /flights

- GET /flights/{flight_id}

- PUT /flights/{flight_id}

- DELETE /flights/{flight_id}

---

##Airport Connectivity

GET /airports/{iata}/destinations

Returns all reachable destinations from a given airport.

---

##Delay Analytics

###1. Delay Rate
GET /analytics/delay-rate?origin=XXX

Returns:

total flights

delayed flights

delay rate

###2. Delay by Hour
GET /analytics/delay-by-hour?origin=XXX

Returns delay statistics grouped by departure hour.

---

##Parameters

Some endpoints accept query parameters:

origin (string): IATA airport code (e.g. ATL, LAX, JFK)

---

##Response Format

All responses are returned in JSON format.

Example:
```json
{
  "origin": "ATL",
  "total_flights": 300,
  "delayed_flights": 120,
  "delay_rate": 0.4
}
```
---

##Error Handling

The API returns standard HTTP status codes:

200 OK – request successful

404 Not Found – resource not found

500 Internal Server Error – server error

---

##Data Processing

The dataset is imported into a SQLite database using a custom script:

PYTHONPATH=. python scripts/import_flights.py

During import:

Time fields are converted to datetime format

Delay minutes are used to determine flight status:

delayed

on_time

---

#Author

Mingxuan Zhang
