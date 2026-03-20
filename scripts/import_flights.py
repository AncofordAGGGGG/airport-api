import csv
from datetime import datetime, timedelta
from pathlib import Path

from app.db import SessionLocal
from app.models import Flight


CSV_FILE = "flight_data_2018_2024.csv"   # CSV file name
IMPORT_LIMIT = 50000          # 50000 flight info，more stable


def parse_hhmm(value):
    """
    let "hhmm" to(hour, minute)
    such as:
    930 -> (9, 30)
    5 -> (0, 5)
    2400 / "" -> None
    """
    if value is None:
        return None

    value = str(value).strip()

    if value == "" or value.upper() == "NA":
        return None

    try:
        num = int(float(value))
    except ValueError:
        return None

    if num == 2400:
        return (0, 0)

    hour = num // 100
    minute = num % 100

    if hour > 23 or minute > 59:
        return None

    return (hour, minute)


def build_datetime(date_str, hhmm_value):
    """
    date_str: 2024-03-01 or 20240301
    hhmm_value: 930 / 1545
    """
    if not date_str:
        return None

    date_str = str(date_str).strip()

    base_date = None
    for fmt in ("%Y-%m-%d", "%Y%m%d"):
        try:
            base_date = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue

    if base_date is None:
        return None

    hm = parse_hhmm(hhmm_value)
    if hm is None:
        return None

    hour, minute = hm
    return base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)


def safe_float(value, default=0):
    if value is None:
        return default
    value = str(value).strip()
    if value == "" or value.upper() == "NA":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def main():
    csv_path = Path(CSV_FILE)

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return

    db = SessionLocal()
    imported = 0
    skipped = 0

    try:
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if imported >= IMPORT_LIMIT:
                    break

                flight_number = str(row.get("Flight_Number_Operating_Airline", "")).strip()
                origin = str(row.get("Origin", "")).strip()
                destination = str(row.get("Dest", "")).strip()
                flight_date = row.get("FlightDate")

                scheduled_departure = build_datetime(flight_date, row.get("CRSDepTime"))
                actual_departure = build_datetime(flight_date, row.get("DepTime"))
                dep_delay = safe_float(row.get("DepDelay"), 0)

                if not flight_number or not origin or not destination or scheduled_departure is None:
                    skipped += 1
                    continue

                status = "delayed" if dep_delay > 0 else "on_time"

                flight = Flight(
                    flight_number=flight_number,
                    origin=origin,
                    destination=destination,
                    scheduled_departure=scheduled_departure,
                    actual_departure=actual_departure,
                    status=status
                )

                db.add(flight)
                imported += 1

                if imported % 500 == 0:
                    db.commit()
                    print(f"Imported {imported} flights...")

            db.commit()

        print(f"Done. Imported: {imported}, Skipped: {skipped}")

    except Exception as e:
        db.rollback()
        print("Import failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()
