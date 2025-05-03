import pyshark
import json
from common.logger.logger import get_logger
from trace_decoder.app.parser.protocols.base_packet import BasePacket
from trace_decoder.app.parser.protocols.sip_packet import SipPacket
from trace_decoder.app.parser.protocols.diameter_packet import DiameterPacket

logger = get_logger("pcap_parser", service_name="trace_decoder")

def decode_sip_packet(pkt) -> SipPacket:
    try:
        timestamp = pkt.sniff_time.isoformat()
    except AttributeError:
        timestamp = "unknown"

    sip = getattr(pkt, "sip", None)
    logger.debug(f"[PCAP Parser] Full SIP Packet:\n{str(sip)}")

    if not sip:
        logger.warning("[PCAP Parser] SIP layer not found in packet")
        return SipPacket(timestamp=timestamp)

    try:
        return SipPacket(
            timestamp=timestamp,
            call_id=getattr(sip, "call_id", None),
            cseq=getattr(sip, "cseq", None),
            from_tag=getattr(sip, "from_tag", None) or getattr(sip, "from_tag_id", None),
            to_tag=getattr(sip, "to_tag", None) or getattr(sip, "to_tag_id", None),
            sip_instance=getattr(sip, "contact_header", None),
            method=getattr(sip, "method", None),
            via=getattr(sip, "via", None),
            p_asserted_identity=getattr(sip, "p_asserted_identity", None),
            request_uri=getattr(sip, "request_uri", None),
            user_agent=getattr(sip, "user_agent", None),
            contact=getattr(sip, "contact_header", None)
        )
    except Exception as e:
        logger.warning(f"[PCAP Parser] Failed to decode SIP packet: {e}")
        return SipPacket(timestamp=timestamp)

    
def decode_diameter_packet(pkt) -> DiameterPacket:
    try:
        timestamp = pkt.sniff_time.isoformat()
    except AttributeError:
        timestamp = "unknown"

    diameter = getattr(pkt, "diameter", None)
    if not diameter:
        logger.warning("[PCAP Parser] DIAMETER layer not found in packet")
        return DiameterPacket(timestamp=timestamp)

    try:
        return DiameterPacket(
            timestamp=timestamp,
            session_id=getattr(diameter, "session_id", None),
            origin_host=getattr(diameter, "origin_host", None),
            origin_realm=getattr(diameter, "origin_realm", None),
            destination_host=getattr(diameter, "destination_host", None),
            destination_realm=getattr(diameter, "destination_realm", None),
            command_code=getattr(diameter, "cmd_code", None),
            application_id=getattr(diameter, "application_id", None),
            result_code=getattr(diameter, "result_code", None)
        )
    except Exception as e:
        logger.warning(f"[PCAP Parser] Failed to decode DIAMETER packet: {e}")
        return DiameterPacket(timestamp=timestamp)


def decode_packet(pkt) -> BasePacket:
    try:
        timestamp = pkt.sniff_time.isoformat()
    except AttributeError:
        timestamp = "unknown"

    source = getattr(pkt.ip, "src", "unknown") if hasattr(pkt, "ip") else "unknown"
    destination = getattr(pkt.ip, "dst", "unknown") if hasattr(pkt, "ip") else "unknown"

    raw_proto = pkt.highest_layer.upper() if pkt.highest_layer else "UNKNOWN"
    protocol = "DIAMETER" if "DIAMETER" in raw_proto else "SIP" if "SIP" in raw_proto else raw_proto
    '''
    # Only extract application-layer protocol payload (e.g., SIP, DIAMETER)
        payload_lines = []
        try:
            layer = getattr(pkt, protocol.lower(), None)
            if layer and hasattr(layer, "_all_fields"):
                for field in layer._all_fields:
                    showname = getattr(field, "showname", None)
                    if showname:
                        payload_lines.append(showname)
        except Exception as e:
            logger.warning(f"[PCAP Parser] Error extracting payload for {protocol}: {e}")

        payload = "\n".join(payload_lines) if payload_lines else pkt._pretty_print()
        logger.debug(f"[PCAP Parser] {protocol} payload lines count: {len(payload_lines)}")
        logger.debug(f"[PCAP Parser] Payload preview:{payload[:300]}...")
    '''
    payload = ""
    return BasePacket(
        timestamp=timestamp,
        source=source,
        destination=destination,
        protocol=protocol,
        payload=payload
    )


def parse_pcap_file(file_path: str) -> list[dict]:
    logger.info(f"[PCAP Parser] Starting to parse file: {file_path}")
    packets = []
    sip_packets = []
    diameter_packets = []

    try:
        cap = pyshark.FileCapture(
            file_path,
            use_json=True,
            include_raw=True,
            display_filter="sip || diameter"  # Filter to load only SIP and Diameter packets
        )
    except Exception as e:
        logger.exception(f"[PCAP Parser] Failed to open PCAP file: {e}")
        return []

    for index, pkt in enumerate(cap):
        try:
            base_packet = decode_packet(pkt)
            packets.append(base_packet.model_dump())

            # Decode protocol-specific packet details
            if base_packet.protocol == "SIP":
                sip_packet = decode_sip_packet(pkt)
                sip_packets.append(sip_packet.model_dump())
            elif base_packet.protocol == "DIAMETER":
                diameter_packet = decode_diameter_packet(pkt)
                diameter_packets.append(diameter_packet.model_dump())
            logger.debug(f"[PCAP Parser] Parsed base packet #{index+1}:")
            logger.debug(json.dumps(base_packet.model_dump(), indent=2, default=str))

            if base_packet.protocol == "SIP":
                logger.debug(f"[PCAP Parser] SIP Packet #{index+1}:")
                logger.debug(json.dumps(sip_packet.model_dump(), indent=2, default=str))
            elif base_packet.protocol == "DIAMETER":
                logger.debug(f"[PCAP Parser] DIAMETER Packet #{index+1}:")
                logger.debug(json.dumps(diameter_packet.model_dump(), indent=2, default=str))
        except Exception as e:
            logger.warning(f"[PCAP Parser] Failed to parse packet #{index+1}: {e}")
            continue

    cap.close()
    for idx, sip_packet in enumerate(sip_packets):
        logger.debug(f"[PCAP Parser] SIP Packet #{idx+1}:")
        logger.debug(json.dumps(sip_packet, indent=2, default=str))

    for idx, diameter_packet in enumerate(diameter_packets):
        logger.debug(f"[PCAP Parser] DIAMETER Packet #{idx+1}:")
        logger.debug(json.dumps(diameter_packet, indent=2, default=str))

    logger.info(f"[PCAP Parser] Finished parsing. \n\
                  Total base packets: {len(packets)},\n\
                  SIP packets: {len(sip_packets)},\n\
                  DIAMETER packets: {len(diameter_packets)}")
    return packets