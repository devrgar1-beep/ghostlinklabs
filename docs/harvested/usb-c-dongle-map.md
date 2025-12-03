# USB-C Dongle Device Map
## Integrated Engineering USB-C Hub Analysis

---

## Hub Overview
**Manufacturer:** GenesysLogic  
**Device Type:** USB-C Multi-Port Hub  
**USB Standard:** USB 3.1 (SuperSpeed+) & USB 2.1 (High-Speed)

---

## Device Topology

```
MacBook USB-C Port (01000000)
│
├─── USB3.1 Hub (GenesysLogic GL3523) @ 01200000
│    │  Vendor ID: 0x05E3 (1507)
│    │  Product ID: 0x0626 (1574)
│    │  Location ID: 0x01200000 (18874368)
│    │  USB Version: 3.1 (0x0800)
│    │  Device Version: 6.22 (0x0656)
│    │
│    ├─── USB 10/100/1000 LAN @ 01240000
│    │    │  Vendor: Realtek
│    │    │  Vendor ID: 0x0BDA (3034)
│    │    │  Product ID: 0x8153 (33107)
│    │    │  Serial: 000001
│    │    │  Location: 0x01240000 (19136512)
│    │    │  Type: Gigabit Ethernet Adapter
│    │    │  USB Version: 3.0 (0x0300)
│    │    │  Device Version: 48.0 (0x3000)
│    │    └─── Power: 288mA
│    │
│    └─── ADATA USB Flash Drive @ 01210000
│         │  Vendor: ADATA
│         │  Vendor ID: 0x125F (4703)
│         │  Product ID: 0x312B (12587)
│         │  Serial: 1421201361250000
│         │  Location: 0x01210000 (18939904)
│         │  USB Version: 3.0 (0x0300)
│         │  Device Version: 17.0 (0x1100)
│         └─── Power: 504mA
│
└─── USB2.1 Hub (GenesysLogic GL3520) @ 01100000
     │  Vendor ID: 0x05E3 (1507)
     │  Product ID: 0x0610 (1552)
     │  Location ID: 0x01100000 (17825792)
     │  USB Version: 2.1 (0x0210)
     │  Device Version: 6.22 (0x0656)
     │
     └─── Mass Storage Device @ 01120000
          │  Vendor: Generic
          │  Vendor ID: 0x14CD (5325)
          │  Product ID: 0x1212 (4626)
          │  Serial: 121220160204
          │  Location: 0x01120000 (17956864)
          │  USB Version: 2.0 (0x0200)
          │  Device Version: 1.0 (0x0100)
          │  Type: USB Flash Drive / Card Reader
          └─── Power: Standard USB 2.0
```

---

## Device Details

### 1. **Primary Hub - GenesysLogic GL3523**
- **Function:** USB 3.1 Gen 1 Hub Controller
- **Ports:** 4-port USB 3.1 SuperSpeed hub
- **Container ID:** f0564b9f-f61d-e011-ac64-0800200c9a66
- **Features:** 
  - Supports USB 3.1 SuperSpeed (5 Gbps)
  - Backward compatible with USB 2.0
  - Hot-swap capable

### 2. **Realtek Gigabit Ethernet Adapter**
- **Model:** RTL8153 Chipset
- **Speed:** 10/100/1000 Mbps
- **Serial Number:** 000001
- **Configuration:** Active Configuration 2
- **Features:**
  - USB 3.0 to Gigabit Ethernet
  - Link Power Management (LPM) capable
  - Low latency network interface

### 3. **ADATA USB Flash Drive**
- **Model:** ADATA C008
- **Capacity:** Unknown (detected as mass storage)
- **Serial:** 1421201361250000
- **USB Speed:** SuperSpeed (USB 3.0)
- **Interface:** Mass Storage Class

### 4. **Secondary Hub - GenesysLogic GL3520**
- **Function:** USB 2.1 High-Speed Hub Controller
- **Ports:** 4-port USB 2.0 hub
- **Container ID:** Same as primary hub (linked device)
- **Purpose:** Provides USB 2.0 backward compatibility

### 5. **Generic Mass Storage Device**
- **Type:** USB 2.0 Flash Drive or Card Reader
- **Serial:** 121220160204
- **Interface:** Bulk-Only Transport (BOT)
- **Format:** Likely FAT32 or exFAT

---

## Connection Map

| Device | Location ID | Port | USB Version | Power Draw |
|--------|-------------|------|-------------|------------|
| USB3.1 Hub | 0x01200000 | Root | USB 3.1 | Bus-powered |
| Ethernet Adapter | 0x01240000 | Hub Port 4 | USB 3.0 | 288mA |
| ADATA Flash | 0x01210000 | Hub Port 1 | USB 3.0 | 504mA |
| USB2.1 Hub | 0x01100000 | Root | USB 2.1 | Bus-powered |
| Mass Storage | 0x01120000 | Hub Port 2 | USB 2.0 | Standard |

---

## Technical Specifications

### Hub Chipset: GenesysLogic GL3523
- **Data Rate:** 5 Gbps (USB 3.1 Gen 1)
- **Architecture:** Dual-hub design (separate USB 3.1 and USB 2.1 controllers)
- **Compliance:** USB-IF certified
- **Power Management:** USB Link Power Management (LPM)

### Network Adapter: Realtek RTL8153
- **Interface:** USB 3.0 to Gigabit Ethernet
- **Chipset Generation:** RTL8153 Series
- **Wake-on-LAN:** Supported
- **Jumbo Frames:** Supported

---

## Notes

1. **Dual-Hub Architecture**: This dongle uses a dual-hub design with separate USB 3.1 and USB 2.1 controllers for maximum compatibility
2. **Power Delivery**: The hub appears to be bus-powered (no external power adapter detected)
3. **Device Detection**: All devices are properly enumerated and recognized by macOS
4. **Driver Status**: Native drivers in use - no third-party drivers required

---

## USB Device IDs Reference

| Vendor | Vendor ID | Product | Product ID |
|--------|-----------|---------|------------|
| GenesysLogic | 0x05E3 | USB3.1 Hub | 0x0626 |
| GenesysLogic | 0x05E3 | USB2.1 Hub | 0x0610 |
| Realtek | 0x0BDA | RTL8153 Ethernet | 0x8153 |
| ADATA | 0x125F | USB Flash | 0x312B |
| Generic | 0x14CD | Mass Storage | 0x1212 |

---

*Generated from ioreg USB device tree analysis*  
*System: macOS 15 (Sequoia)*  
*Date: October 12, 2025*
