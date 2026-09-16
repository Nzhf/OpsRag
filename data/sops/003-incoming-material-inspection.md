# SOP: Incoming Material Inspection

**Document ID:** SOP-QA-010
**Version:** 2.0
**Effective Date:** 2025-02-01
**Department:** Quality Assurance / Warehouse
**Applies to:** All incoming components, raw materials
**Review Cycle:** Annual

---

## 1. Purpose

This procedure establishes the requirements and methods for inspecting incoming materials at BizLink Penang Manufacturing. Incoming inspection prevents defective or non-conforming materials from entering production.

## 2. Scope

This SOP applies to:
- Electronic components (ICs, passives, connectors)
- PCB blanks
- Solder paste, flux, and other consumables
- Mechanical parts (enclosures, fasteners, cables)
- Packaging materials (ESD bags, foam, boxes)

Exclusions:
- Direct-ship items to production (managed by Engineering with supplier certification)
- Office supplies (not production-related)

## 3. Responsibilities

| Role | Responsibility |
|------|----------------|
| Receiving Clerk | Log incoming shipments, verify packing list |
| IQC Inspector | Perform inspection per sampling plan, record results |
| Quality Engineer | Review rejected lots, approve/reject disposition |
| Warehouse Staff | Store accepted materials, segregate rejected materials |
| Purchasing | Communicate with suppliers on rejected materials |

## 4. Inspection Levels

### 4.1 Sampling Plan

Use ANSI/ASQ Z1.4 (Single Sampling Plans for Normal Inspection) unless otherwise specified on drawing or specification.

| Material Category | Inspection Level | AQL |
|-------------------|------------------|-----|
| Critical components (ICs, processors) | Level II | 0.65% |
| Standard components (resistors, capacitors) | Level I | 1.0% |
| Mechanical parts | Level I | 2.5% |
| Consumables (solder paste) | 100% (date/lot check) | N/A |
| PCB blanks | Level II | 1.0% |

### 4.2 Skip-Lot Program

Suppliers with sustained quality performance may qualify for skip-lot inspection:
- Requirement: 10 consecutive lots passed with zero defects
- Skip ratio: Inspect 1 of every 3 lots
- Disqualification: Any reject returns supplier to 100% inspection

## 5. Inspection Procedure

### 5.1 Receiving and Identification

1. Verify shipment matches purchase order (PO number, part number, quantity)
2. Log receipt in ERP system with:
   - Date received
   - Supplier name
   - PO number
   - Part number and description
   - Quantity received
   - Lot/batch number
   - Supplier C of C (Certificate of Conformance) attached
3. Apply "HOLD - AWAITING INSPECTION" label with date
4. Route to incoming inspection area within 2 hours of receipt

### 5.2 Document Review

Before physical inspection, verify:
- [ ] Certificate of Conformance present and matches lot
- [ ] Material date code within acceptable age (see Section 6)
- [ ] Packaging intact, no visible damage
- [ ] Correct part number per PO
- [ ] RoHS/REACH compliance declaration (if applicable)

If any document check fails: **REJECT** and notify Purchasing.

### 5.3 Physical Inspection

#### 5.3.1 Electronic Components

**Visual Inspection (per sampling plan):**
- Component marking legibility and correctness
- Lead condition (no bent, damaged, or oxidized leads)
- Package integrity (no cracks, chipping, contamination)
- Correct orientation markers present
- ESD packaging intact for ESDS items

**Dimensional Check (if required):**
- Use calibrated calipers or micrometer
- Compare to drawing or datasheet dimensions
- Record measurements on Inspection Data Sheet (IDS-001)

**Functional Test (if required per specification):**
- Use in-circuit tester or specified test fixture
- Verify parametric values within datasheet limits
- Record all test data

#### 5.3.2 PCB Blanks

**Visual Inspection:**
- Copper trace integrity (no scratches, exposed substrate)
- Solder mask coverage (no pinholes, delamination)
- Silkscreen legibility
- Board flatness (no warping > 1% of diagonal length)
- Hole quality (no burrs, correct plating)

**Dimensional Check:**
- Overall dimensions
- Hole diameters (sample critical holes)
- Board thickness

#### 5.3.3 Solder Paste and Consumables

**Solder Paste:**
1. Verify temperature indicator on packaging (should show no heat exposure)
2. Check expiration date (must have ≥3 months shelf life remaining)
3. Record lot number and refrigeration requirement
4. Verify correct alloy and particle size per specification

**Other Consumables:**
- Verify lot number, expiration date
- Check packaging integrity
- Confirm material matches specification

### 5.4 Recording Results

1. Complete Inspection Data Sheet (IDS-001) for each lot
2. Calculate defects per million (DPPM) for statistical tracking
3. Enter result in ERP system:
   - **PASS**: Green "ACCEPTED" label applied, move to warehouse
   - **FAIL**: Red "REJECTED" label applied, move to quarantine area

## 6. Material Age Requirements

| Material Type | Maximum Age at Receipt | Maximum Shelf Life |
|---------------|------------------------|-------------------|
| Solder paste (refrigerated) | 6 months from manufacture | 12 months from manufacture |
| IC components | 24 months from date code | 36 months typical |
| PCB blanks | 12 months from manufacture | 24 months typical |
| Moisture-sensitive devices (MSD) | 12 months from date code | Per JEDEC J-STD-033 |

**Note:** MSD components must be verified for dry pack integrity. If dry pack indicator shows exposure, bake per J-STD-033 before use.

## 7. Rejection and Disposition

### 7.1 Rejection Process

1. Complete Non-Conformance Report (NCR-001)
2. Attach photos of defects (required for all rejections)
3. Notify Purchasing within 4 hours of rejection decision
4. Purchasing contacts supplier for return material authorization (RMA)
5. Material held in quarantine pending disposition

### 7.2 Disposition Options

| Disposition | Criteria | Approval Required |
|-------------|----------|-------------------|
| Return to Supplier | Quality does not meet specification | Quality Engineer |
| Use-As-Is | Minor deviation, no functional impact | Quality Manager + Engineering |
| Rework/Sort | Can be corrected to meet spec | Quality Engineer |
| Scrap | Unusable, no supplier recourse | Quality Manager |

### 7.3 Supplier Corrective Action

For repetitive failures (≥3 rejections in 90 days from same supplier):
1. Issue Supplier Corrective Action Request (SCAR)
2. Supplier must respond with root cause and corrective action within 10 business days
3. Verify effectiveness of supplier's corrective action
4. Consider alternative supplier if issues persist

## 8. Inspection Equipment

| Equipment | Calibration Frequency | Use |
|-----------|----------------------|-----|
| Digital calipers | Annual | Dimensional measurement |
| Micrometer | Annual | Thickness measurement |
| Magnifying lamp (10x) | Daily check | Visual inspection |
| Optical comparator | Annual | Complex profile measurement |
| LCR meter | Semi-annual | Component parametric test |
| Refrigerator thermometer | Quarterly | Solder paste storage temp |

## 9. Training Requirements

| Role | Initial Training | Refresher |
|------|------------------|-----------|
| IQC Inspector | 8-hour incoming inspection course | Annual, 2 hours |
| Receiving Clerk | 4-hour receiving and documentation | Annual, 1 hour |
| Quality Engineer | Full SOP training + statistical methods | Annual, 4 hours |

## 10. Metrics and Reporting

Monthly IQC Report includes:
- Total lots inspected
- Pass rate percentage
- DPPM by supplier and material category
- Top 5 suppliers by rejection rate
- SCAR status and effectiveness

Present at monthly Quality Review Meeting.

## 11. References

- ANSI/ASQ Z1.4: Sampling Procedures
- JEDEC J-STD-033: Handling of Moisture Sensitive Devices
- IPC-A-610: Acceptability of Electronic Assemblies
- Company Quality Manual, Section 7.4.3

## 12. Revision History

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | 2023-06-01 | Initial release | K. Yamamoto |
| 2.0 | 2025-02-01 | Added skip-lot program, updated AQL table | A. Rahman |

---

**Document Owner:** Quality Assurance Manager
**Next Review Date:** February 2026
