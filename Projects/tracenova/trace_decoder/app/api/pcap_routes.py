from fastapi import APIRouter, UploadFile, File, HTTPException
import os, time
from common.logger.logger import get_logger
from trace_decoder.app.parser.pcap_parser import parse_pcap_file
from trace_decoder.app.services.tracenova_db_client import tracenova_db_client

# ✅ Fix for missing router definition
router = APIRouter()
logger = get_logger("pcap_routes", service_name="trace_decoder")

@router.post("/file")
async def decode_pcap(file: UploadFile = File(...)):
    try:
        tmp_path = f"/tmp/{file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"Saved to temp path: {tmp_path}")

        packets = parse_pcap_file(tmp_path)
        if packets:
            tracenova_db_client.insert_bulk_packets(packets)
            logger.info(f"Inserted {len(packets)} packets to tracenova_db")

        return {"status": "success", "packet_count": len(packets)}
    except Exception as e:
        logger.exception("Error processing PCAP")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
