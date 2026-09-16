# SOP: SMT Line Changeover Procedure

**Document ID:** SOP-OP-001
**Version:** 2.3
**Effective Date:** 2025-01-15
**Department:** Surface Mount Technology (SMT)
**Applies to:** SMT-1, SMT-2, SMT-3
**Review Cycle:** Annual

---

## 1. Purpose

This procedure establishes the standard steps for performing a line changeover on Surface Mount Technology (SMT) lines at BizLink Penang Manufacturing. Proper changeover ensures minimal downtime, prevents component mixing, and maintains product quality.

## 2. Scope

This SOP applies to all operators, line leaders, and maintenance technicians working on SMT lines SMT-1, SMT-2, and SMT-3. It covers changeovers between different PCB assemblies and product models.

## 3. Responsibilities

| Role | Responsibility |
|------|----------------|
| Line Leader | Authorize changeover, verify completion checklist |
| SMT Operator | Execute changeover steps, update machine programs |
| Quality Inspector | Verify first article after changeover |
| Maintenance Technician | Assist with feeder changes if required |

## 4. Prerequisites

- Production schedule confirmed for next product run
- New production traveler and work instructions available
- Required components verified in inventory system
- SMT program file loaded and verified

## 5. Procedure

### 5.1 Pre-Changeover (Est. time: 5 minutes)

1. Complete current production run and record final count on traveler
2. Run remaining components through placement machine to clear feeders
3. Print and review changeover checklist for target product
4. Retrieve new reel components from inventory using pick list

### 5.2 Machine Setup Changes (Est. time: 15-30 minutes)

1. **Program Load:**
   - Navigate to machine HMI > Program Management
   - Load target product program file (format: `BLM-[model]-[rev].prg`)
   - Verify program version matches current engineering release

2. **Feeder Changes:**
   - Identify feeders requiring position changes per setup sheet
   - Remove feeders from previous setup positions
   - Install feeders in new positions, ensuring proper alignment
   - Scan feeder barcode to confirm correct component placement

3. **Stencil Change:**
   - Remove current stencil from printer using stencil handling frame
   - Clean removed stencil with approved IPA solution
   - Store stencil in designated rack location
   - Retrieve new stencil for target product (verify part number on stencil frame)
   - Install new stencil, confirm alignment pins engaged

### 5.3 Solder Paste Application

1. Verify solder paste type matches work instruction (typically SAC305 Type 4)
2. Check paste temperature on arrival log (must be 20-25°C)
3. Apply paste to stencil using manual or automatic dispensing
4. Allow paste to stabilize for 3-5 minutes before first print

### 5.4 First Article Verification

1. Run first PCB through complete line cycle
2. Present first article to Quality Inspector
3. Inspector performs:
   - Visual inspection under 10x magnification
   - Component placement verification against assembly drawing
   - Solder paste print quality check (tombstone, bridging, insufficient paste)
4. Record results on First Article Inspection Report (FAIR-001)
5. If FAIL: Adjust parameters, repeat from 5.4.1
6. If PASS: Sign off FAIR, proceed with production run

## 6. Quality Checkpoints

| Checkpoint | Criteria | Action if Fail |
|------------|----------|----------------|
| Feeder barcode match | Scanned ID matches setup sheet | Stop, verify correct component |
| Stencil condition | No damage, apertures clear | Replace stencil |
| Paste print quality | >85% pad coverage, no bridging | Adjust print parameters |
| Component placement | Within 50% of pad center | Check nozzle condition |

## 7. Safety Considerations

- Wear ESD wrist strap when handling PCBs and components
- Use two-hand lift technique for stencil removal to prevent strain
- Ensure machine is in SAFE mode before reaching into work envelope
- Report any sharp edges on stencils to maintenance for dressing

## 8. Documentation

After successful changeover, complete and file:
- Changeover Checklist (CC-001) - retained at line station
- First Article Inspection Report (FAIR-001) - submitted to Quality
- Update production log with changeover start/end times

## 9. References

- SOP-OP-005: ESD Handling for PCB Assembly
- SOP-QA-002: First Article Inspection Procedure
- Work Instruction Archive: `\\fileserver\prod_docs\SMT\WI\`

## 10. Revision History

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | 2023-03-01 | Initial release | T. Wong |
| 2.0 | 2024-06-15 | Added feeder barcode scanning step | L. Chen |
| 2.3 | 2025-01-15 | Updated stencil handling procedure | A. Rahman |

---

**Document Owner:** Production Engineering Manager
**Next Review Date:** January 2026
