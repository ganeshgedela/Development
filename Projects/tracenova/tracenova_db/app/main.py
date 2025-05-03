from fastapi import FastAPI
from app.database.engine import init_db
from contextlib import asynccontextmanager
from app.routers import packet_routes
from app.routers import network_trace_routes
from app.routers import sip_packet_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan, title="Tracenova DBService")


# Register packet endpoints
app.include_router(packet_routes.router, prefix="/packet", tags=["Packet"])
app.include_router(network_trace_routes.router, prefix="/trace-file", tags=["Trace Files"])
app.include_router(sip_packet_routes.router, prefix="/sip-packet", tags=["SIP Packets"])


@app.get("/")
def root():
    return {"message": "Tracenova DBService is running 🚀"}
