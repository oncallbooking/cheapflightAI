from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, JSON, Float, Date, ForeignKey

Base = declarative_base()

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    origin = Column(String(8), nullable=False)
    destination = Column(String(8), nullable=False)
    depart_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    cabin = Column(String(16), nullable=False, default="economy")
    flex_days = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default="now()")

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    status = Column(String(32), nullable=False, default="active")
    last_latency_ms = Column(Integer)
    error_rate = Column(Float)
    last_checked = Column(TIMESTAMP)

class RawFlight(Base):
    __tablename__ = "raw_flights"
    id = Column(BigInteger, primary_key=True)
    search_params = Column(JSON, nullable=False)
    scraped_at = Column(TIMESTAMP, nullable=False)
    source = Column(String(128), nullable=False)
    raw_payload = Column(JSON)

class NormalizedFlight(Base):
    __tablename__ = "normalized_flights"
    id = Column(BigInteger, primary_key=True)
    raw_id = Column(BigInteger, ForeignKey("raw_flights.id"), nullable=False)
    origin = Column(String(8), nullable=False)
    destination = Column(String(8), nullable=False)
    depart_date = Column(Date)
    return_date = Column(Date)
    airline = Column(String(64))
    flight_numbers = Column(JSON)
    departure_time = Column(TIMESTAMP)
    arrival_time = Column(TIMESTAMP)
    duration_minutes = Column(Integer)
    stops = Column(Integer)
    price_inr = Column(Float, nullable=False)
    booking_url = Column(String(1024))
    scraped_at = Column(TIMESTAMP, nullable=False)

class Deal(Base):
    __tablename__ = "deals"
    id = Column(BigInteger, primary_key=True)
    normalized_id = Column(BigInteger, ForeignKey("normalized_flights.id"), nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(BigInteger, primary_key=True)
    route_key = Column(String(64), nullable=False)
    date = Column(Date)
    cabins = Column(JSON)
    median_price_inr = Column(Float)
    recorded_at = Column(TIMESTAMP, server_default="now()")
