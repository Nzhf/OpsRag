# SOP: Reflow Solder Profile Setup and Verification

**Document ID:** SOP-OP-002
**Version:** 1.8
**Effective Date:** 2025-03-01
**Department:** Surface Mount Technology (SMT)
**Applies to:** SMT-1, SMT-2, SMT-3
**Review Cycle:** Annual

---

## 1. Purpose

This procedure establishes the requirements for setting up, verifying, and maintaining reflow soldering profiles on SMT lines. Proper reflow profiles ensure reliable solder joints while preventing thermal damage to components.

## 2. Scope

This SOP applies to all reflow ovens on SMT lines (SMT-1, SMT-2, SMT-3) and covers:
- Initial profile development for new products
- Daily profile verification
- Profile adjustment for quality issues
- Documentation requirements

## 3. Responsibilities

| Role | Responsibility |
|------|----------------|
| Process Engineer | Develop and approve profiles, investigate profile-related defects |
| SMT Operator | Run daily verification, log results |
| Quality Inspector | Report solder quality issues requiring profile review |
| Maintenance Technician | Oven calibration, conveyor maintenance |

## 4. Equipment

| Line | Oven Model | Number of Zones |
|------|------------|-----------------|
| SMT-1 | Heller 1913 MK5 | 13 zones |
| SMT-2 | Heller 1913 MK5 | 13 zones |
| SMT-3 | Vitronics Soltec XPM2 | 10 zones |

Profile measurement equipment:
- KIC DQ-10 data logger with 10 thermocouples
- KIC AutoFocus software (version 2024.2)

## 5. Reflow Profile Parameters

### 5.1 Standard SAC305 Profile Requirements

| Zone | Temperature Range | Duration |
|------|-------------------|----------|
| Preheat (Ramp) | 25°C to 150°C | 60-90 seconds |
| Soak | 150°C to 180°C | 60-120 seconds |
| Reflow (Peak) | 230°C to 245°C | 30-60 seconds above 217°C |
| Cooling | Peak to 150°C | < 60 seconds |

**Critical limits:**
- Maximum peak temperature: 250°C (to prevent component damage)
- Time above liquidus (217°C): 30-90 seconds
- Ramp rate: 1-3°C/second (max 4°C/second)

### 5.2 Lead-Free Paste Considerations

For SAC305 and similar lead-free alloys:
- Higher peak temperature required compared to Sn63Pb37
- Verify component temperature ratings in BOM (most modern components rated 260°C max)
- Nitrogen atmosphere recommended for complex boards with fine-pitch components

## 6. Profile Development Procedure

### 6.1 New Product Profile Setup

1. **Gather requirements:**
   - PCB material and thickness (standard FR4: 1.6mm)
   - Component temperature sensitivity (check BOM for special requirements)
   - Solder paste specification (alloy, particle size, flux type)
   - Board size and thermal mass

2. **Select baseline profile:**
   - Use existing profile for similar board as starting point
   - If new product class, use standard SAC305 baseline

3. **Instrument test board:**
   - Attach thermocouples to critical locations:
     - Large component (high thermal mass)
     - Small passive component (low thermal mass)
     - BGA center (if applicable)
     - BGA corner
     - Board edge
   - Use high-temperature solder or Kapton tape for attachment
   - Ensure thermocouple bead contacts the solder joint location, not component body

4. **Run and measure profile:**
   - Pass instrumented board through oven
   - Record profile using KIC software
   - Export data to PDF and native format

5. **Analyze and adjust:**
   - Compare measured profile to requirements
   - Adjust zone temperatures, conveyor speed as needed
   - Document all changes in Profile Change Log

6. **First article inspection:**
   - Run 5 production boards through with new profile
   - Quality inspects for:
     - Solder joint quality (wetting, fillet shape)
     - Tombstones, bridging, insufficient solder
     - Component damage (cracking, discoloration)
     - Board warpage
   - X-ray inspection for BGA joints

7. **Approval:**
   - Process Engineer reviews profile data and FAI results
   - Sign off on Profile Approval Form (PAF-001)
   - Save approved profile to server: `\\fileserver\process\reflow_profiles\`

### 6.2 Profile Naming Convention

Format: `BLM-[model]-[rev]_[paste_type]_[date].prf`

Example: `BLM-MC200-A1_SAC305_20250301.prf`

## 7. Daily Verification Procedure

### 7.1 Morning Startup Check (Before Production)

1. Power on oven at least 30 minutes before production start
2. Verify all zone temperatures reach setpoints (green indicators on HMI)
3. Check nitrogen flow rate (if applicable): 500-800 CFH
4. Verify conveyor belt tracking centered
5. Run profile verification using production board with embedded thermocouple or profile test coupon
6. Compare to approved baseline profile:
   - Peak temperature within ±5°C of baseline
   - Time above liquidus within ±15 seconds
7. Record results in Daily Reflow Log (DRL-001)

### 7.2 In-Process Monitoring

Every 4 hours during production:
- Record zone temperatures from HMI
- Check conveyor speed setting
- Note any alarms or warnings
- Visual check of solder quality on sample boards

### 7.3 End of Shift

- Download profile data from oven controller
- Save to daily production folder
- Note any anomalies in shift report

## 8. Profile Adjustment for Quality Issues

### 8.1 Common Defects and Adjustments

| Defect | Possible Cause | Profile Adjustment |
|--------|----------------|-------------------|
| Tombstones | Rapid heating, uneven wetting | Reduce ramp rate, extend soak |
| Solder balls | Excessive flux outgassing | Reduce preheat ramp, check paste |
| Insufficient solder | Low peak temp, short TAL | Increase peak zone temps |
| Bridging | Excessive solder paste, overprinting | Reduce peak temp, check stencil |
| Cold joints | Peak temp too low | Increase peak zones 5-10°C |
| Component cracking | Thermal shock, too fast cooling | Reduce cooling rate |

### 8.2 Adjustment Process

1. Document current defect and rate (defects per million opportunities)
2. Propose adjustment with rationale
3. Make single adjustment at a time (change one parameter)
4. Run verification profile
5. Produce sample lot (minimum 25 boards)
6. Inspect for defect improvement
7. If improved, update profile documentation
8. If not improved, revert and try alternative adjustment

**Note:** All adjustments require Process Engineer approval before implementation.

## 9. Maintenance and Calibration

### 9.1 Preventive Maintenance Schedule

| Frequency | Task |
|-----------|------|
| Daily | Clean flux residue from oven interior, check filters |
| Weekly | Inspect conveyor belt, clean cooling fans |
| Monthly | Clean all zone heating elements, verify thermocouples |
| Quarterly | Full calibration by certified technician |

### 9.2 Calibration Requirements

- All zone thermocouples: ±2°C accuracy
- Conveyor speed: ±1% of setpoint
- Profile logger: Calibrate annually against NIST-traceable standard

Calibration records maintained in Equipment Master file.

## 10. Documentation

| Document | Purpose | Retention |
|----------|---------|-----------|
| Profile Approval Form (PAF-001) | New profile sign-off | Life of product + 3 years |
| Daily Reflow Log (DRL-001) | Daily verification records | 2 years |
| Profile Change Log | History of all adjustments | Life of product + 3 years |
| Profile data files (PDF, native) | Measured profiles | Server backup |

## 11. Safety

- Oven exterior reaches high temperatures during operation
- Allow oven to cool to < 50°C before internal maintenance
- Use heat-resistant gloves when handling oven components
- Emergency stop buttons located at oven entrance and exit
- Ensure exhaust system is operational before starting oven

## 12. References

- IPC J-STD-001: Requirements for Soldered Electrical and Electronic Assemblies
- IPC-A-610: Acceptability of Electronic Assemblies
- Solder paste manufacturer datasheet
- Oven manufacturer operation manual

## 13. Revision History

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | 2022-05-01 | Initial release | R. Kumar |
| 1.5 | 2024-01-15 | Added nitrogen requirements | T. Wong |
| 1.8 | 2025-03-01 | Updated profile naming convention | A. Rahman |

---

**Document Owner:** Process Engineering Manager
**Next Review Date:** March 2026
