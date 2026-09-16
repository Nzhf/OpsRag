# SOP: PCB Visual Inspection

**Document ID:** SOP-QA-003
**Version:** 1.5
**Effective Date:** 2024-07-01
**Department:** Quality Assurance
**Applies to:** All production lines (SMT-1, SMT-2, SMT-3, Assembly-A, Assembly-B)
**Review Cycle:** Annual

---

## 1. Purpose

This procedure defines the requirements for visual inspection of printed circuit board assemblies (PCBAs) at BizLink Penang Manufacturing. Visual inspection catches defects before products proceed to functional testing or shipment.

## 2. Scope

This SOP covers:
- Post-reflow inspection (SMT)
- Post-wave inspection (through-hole)
- Final assembly inspection
- Inspection criteria based on IPC-A-610 Class 2

## 3. Responsibilities

| Role | Responsibility |
|------|----------------|
| Visual Inspector | Perform inspection, document defects, route rejects |
| Quality Engineer | Define inspection criteria, review borderline cases |
| Production Operator | Self-check own work, address defects found |
| Quality Manager | Oversee inspection program, approve sample size changes |

## 4. Inspection Stations

| Line | Station | Timing | Inspection Type |
|------|---------|--------|-----------------|
| SMT-1, SMT-2, SMT-3 | Post-reflow | Immediately after reflow oven | Visual + AOI |
| Assembly-A, Assembly-B | Post-wave | After wave solder and cleaning | Visual |
| All lines | Final QA | Before packing | Full visual per sampling plan |

## 5. Equipment

| Equipment | Purpose | Calibration |
|-----------|---------|-------------|
| Magnifying lamp (10x) | Detail inspection | Annual |
| Stereo microscope (10-40x) | Fine-pitch, BGA inspection | Annual |
| ESD wrist strap | Static protection | Daily |
| Inspection light (5000K) | Optimal lighting, color rendering | Verify at startup |
| AOI machine | Automated optical inspection | Per manufacturer PM schedule |

## 6. Inspection Criteria

### 6.1 Acceptable Workmanship (Class 2)

Per IPC-A-610 Class 2 (General Electronic Products):
- Products where continued performance and extended life are required
- Uninterrupted service is desired but not critical
- Examples: Computers, telecommunications equipment, industrial controls

### 6.2 Defect Categories

| Category | Defect | Accept/Reject |
|----------|--------|---------------|
| **Solder** | Insufficient solder | Reject |
| | Excess solder | Accept if no short,Reject if bulging |
| | Cold solder (dull,grainy for lead-free may be acceptable) | Reject |
| | Non-wetting | Reject |
| | Solder bridge | Reject |
| | Solder ball > 0.13mm | Reject |
| **Component** | Missing | Reject |
| | Wrong value/type | Reject |
| | Wrong polarity | Reject |
| | Cracked/chipped body (exceeds 50% of component) | Reject |
| | Tombstone | Reject |
| | Misaligned (exceeds 50% off pad) | Reject |
| **PCB** | Delamination | Reject |
| | Scratch exposing copper | Reject if on trace |
| | Measling (white spots in substrate) | Accept if < 2mm²,not on trace |
| | Pad lifting | Reject |

## 7. Inspection Procedure

### 7.1 Setup

1. Verify ESD protection (wrist strap tested and logged)
2. Turn on inspection light (5000K LED preferred)
3. Have reference documents ready:
   - Assembly drawing
   - BOM (Bill of Materials)
   - Sample board (golden sample) if available
4. Verify inspection aids (magnification) are clean and functional

### 7.2 General Inspection Sequence

Inspect each board in consistent order:

1. **Overall board condition:**
   - No obvious damage, contamination, or foreign material
   - Correct board revision (check silkscreen)
   - All expected components present (compare to drawing)

2. **Component placement:**
   - Correct orientation (check polarity marks, pin 1 indicators)
   - Components seated flat on pads
   - No missing components

3. **Solder quality (SMT):**
   - Good wetting on all joints
   - No bridges or solder balls
   - Fillet shape appropriate for termination type

4. **Solder quality (Through-hole):**
   - Solder fills barrel (fillet visible on solder side)
   - Leads trimmed to correct length
   - No bridges between adjacent pins

5. **Workmanship:**
   - No flux residue (or within spec for no-clean)
   - No fingerprints, contamination
   - Labels and markings legible

### 7.3 Fine-Pitch and BGA Inspection

For components with lead pitch ≤ 0.65mm and all BGA devices:

1. Use stereo microscope (minimum 20x)
2. For BGAs, visual inspection can only verify perimeter joints
3. Full BGA inspection requires X-ray (covered by SOP-QA-008)
4. Document any visible anomalies

### 7.4 Sampling Plans

| Inspection Point | Method | Sample Size |
|------------------|--------|-------------|
| Post-reflow (SMT) | 100% AOI + visual sample | 100% AOI, 10% visual verify |
| Post-wave | Visual sample | Per ANSI Z1.4, Level II |
| Final QA | Visual sample | Per ANSI Z1.4, Level II, AQL 1.0 |

## 8. Defect Documentation

### 8.1 Recording Defects

All defects must be recorded in the Quality Log with:
- Date and time
- Line and shift
- Board serial number (if serialized) or lot number
- Component reference designator
- Defect type (use standard defect codes)
- Inspector ID

### 8.2 Defect Codes

| Code | Defect Description |
|------|-------------------|
| S01 | Insufficient solder |
| S02 | Excess solder |
| S03 | Solder bridge |
| S04 | Cold solder joint |
| S05 | Solder ball |
| S06 | Non-wetting |
| C01 | Missing component |
| C02 | Wrong component |
| C03 | Wrong polarity/orientation |
| C04 | Component damaged |
| C05 | Tombstone |
| C06 | Misaligned component |
| P01 | PCB damage (delamination, scratch) |
| P02 | Foreign material/contamination |
| P03 | Pad defect |

### 8.3 Disposition

Defective boards must be:
1. Marked with red "HOLD" tag
2. Routed to rework station with Defect Report (DR-001)
3. Reworked by certified technician
4. Re-inspected after rework
5. If rework unsuccessful, route to Material Review Board (MRB)

## 9. AOI Operation (SMT Lines)

### 9.1 Program Setup

AOI programs are created and maintained by Process Engineering. Operators verify:
- Correct program loaded (check model name on HMI)
- Conveyor width set correctly
- Lighting conditions optimal (no external shadows)

### 9.2 Interpreting AOI Results

- **Green (Pass):** No action required
- **Yellow (Marginal):** Review manually, accept or reject
- **Red (Fail):** Manually verify, correct if confirmed defect

### 9.3 False Call Rate

Target: < 5% false call rate
- If false calls exceed target, notify Process Engineering
- Do not adjust AOI sensitivity without engineering approval

## 10. Metrics and Reporting

### 10.1 Daily Metrics

Record and post at inspection station:
- Total boards inspected
- Pass rate percentage
- Top 3 defect types
- First pass yield (FPY)

### 10.2 Weekly Review

Quality Engineer reviews:
- Defect Pareto by type, line, and component
- Trend analysis (improving or worsening)
- Rework effectiveness (rework success rate)

### 10.3 Monthly Report

Present at Quality Review Meeting:
- FPY by product and line
- Defect DPPM (defects per million opportunities)
- Comparison to target
- Improvement actions if below target

## 11. Training Requirements

| Role | Training | Certification |
|------|----------|---------------|
| Visual Inspector | IPC-A-610 CIS (Certified IPC Specialist) | 2-year validity |
| AOI Operator | Machine-specific training + IPC-A-610 CIS | Annual refresh |
| Quality Engineer | IPC-A-610 CIT (Certified IPC Trainer) | 2-year validity |

## 12. Reference Standards

- IPC-A-610: Acceptability of Electronic Assemblies (current revision)
- IPC J-STD-001: Requirements for Soldered Electrical and Electronic Assemblies
- ANSI/ASQ Z1.4: Sampling Procedures and Tables for Inspection by Attributes

## 13. Revision History

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | 2023-03-01 | Initial release | M. Tanaka |
| 1.3 | 2024-01-15 | Added defect codes | S. Lim |
| 1.5 | 2024-07-01 | Updated sampling plans,added AOI section | A. Rahman |

---

**Document Owner:** Quality Assurance Manager
**Next Review Date:** July 2025
