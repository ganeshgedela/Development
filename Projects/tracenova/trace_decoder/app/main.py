from fastapi import FastAPI
from trace_decoder.app.api.pcap_routes import router as pcap_router

app = FastAPI(title="Trace Decoder")
app.include_router(pcap_router, prefix="/decode/pcap")
