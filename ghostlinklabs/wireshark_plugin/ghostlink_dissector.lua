-- GhostLink Protocol Dissector for Wireshark
-- This Lua script dissects GhostLink protocol packets
-- Place this file in Wireshark's plugins directory or load it manually

-- Define the protocol
ghostlink_proto = Proto("ghostlink", "GhostLink Protocol")

-- Define fields
local f_magic = ProtoField.string("ghostlink.magic", "Magic Header")
local f_version = ProtoField.uint16("ghostlink.version", "Protocol Version", base.DEC)
local f_msg_type = ProtoField.uint16("ghostlink.msg_type", "Message Type", base.DEC)
local f_payload_len = ProtoField.uint32("ghostlink.payload_len", "Payload Length", base.DEC)
local f_payload = ProtoField.bytes("ghostlink.payload", "Payload")
local f_checksum = ProtoField.uint32("ghostlink.checksum", "Checksum", base.HEX)

-- Add fields to protocol
ghostlink_proto.fields = {f_magic, f_version, f_msg_type, f_payload_len, f_payload, f_checksum}

-- Message type names
local msg_types = {
    [1] = "HANDSHAKE",
    [2] = "HEARTBEAT",
    [3] = "DATA_TRANSFER",
    [4] = "COMMAND",
    [5] = "RESPONSE",
    [6] = "EVOLUTION_UPDATE",
    [7] = "CONSCIOUSNESS_SYNC",
    [8] = "AGENT_ASSIGNMENT",
    [9] = "HARDWARE_DISCOVERY",
    [10] = "DARWIN_INTEGRATION"
}

-- Dissector function
function ghostlink_proto.dissector(buffer, pinfo, tree)
    -- Check if buffer is long enough for header
    if buffer:len() < 16 then
        return 0
    end

    -- Check magic header
    local magic = buffer(0, 8):string()
    if magic ~= "GHOSTLINK" then
        return 0
    end

    -- Set protocol column
    pinfo.cols.protocol = "GHOSTLINK"

    -- Create subtree
    local subtree = tree:add(ghostlink_proto, buffer(), "GhostLink Protocol")

    -- Dissect header
    local offset = 0
    subtree:add(f_magic, buffer(offset, 8))
    offset = offset + 8

    local version = buffer(offset, 2):uint()
    subtree:add(f_version, buffer(offset, 2))
    offset = offset + 2

    local msg_type = buffer(offset, 2):uint()
    local msg_name = msg_types[msg_type] or "UNKNOWN"
    subtree:add(f_msg_type, buffer(offset, 2)):append_text(" (" .. msg_name .. ")")
    offset = offset + 2

    local payload_len = buffer(offset, 4):uint()
    subtree:add(f_payload_len, buffer(offset, 4))
    offset = offset + 4

    -- Set info column
    pinfo.cols.info = "GhostLink " .. msg_name

    -- Dissect payload if present
    if payload_len > 0 and buffer:len() >= offset + payload_len then
        subtree:add(f_payload, buffer(offset, payload_len))
        offset = offset + payload_len
    end

    -- Dissect checksum if present
    if buffer:len() >= offset + 4 then
        subtree:add(f_checksum, buffer(offset, 4))
    end

    return buffer:len()
end

-- Register dissector
local tcp_port = DissectorTable.get("tcp.port")
tcp_port:add(9999, ghostlink_proto)  -- Default GhostLink port

local udp_port = DissectorTable.get("udp.port")
udp_port:add(9999, ghostlink_proto)  -- Default GhostLink port

-- Also register by name for manual dissection
local data_dissector = DissectorTable.get("data")
data_dissector:add("ghostlink", ghostlink_proto)
