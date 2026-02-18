from sqlalchemy import text
from app.database import engine

print("Adding production indexes and constraints...")

queries = [

    # Route search optimization
    """
    CREATE INDEX IF NOT EXISTS idx_routes_source
    ON routes(source_city_id);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_routes_destination
    ON routes(destination_city_id);
    """,

    # Schedule search optimization
    """
    CREATE INDEX IF NOT EXISTS idx_schedules_route
    ON schedules(route_id);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_schedules_departure
    ON schedules(departure_time);
    """,

    # Ticket lookup
    """
    CREATE INDEX IF NOT EXISTS idx_tickets_user
    ON tickets(user_id);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_tickets_schedule
    ON tickets(schedule_id);
    """,

    # Prevent double seat booking
    """
    ALTER TABLE seats
    ADD CONSTRAINT unique_seat_per_schedule
    UNIQUE(schedule_id, seat_number);
    """,

]

with engine.connect() as conn:
    for query in queries:
        try:
            conn.execute(text(query))
        except Exception as e:
            print("Skipped (maybe already exists):", e)

print("Production upgrades applied.")
