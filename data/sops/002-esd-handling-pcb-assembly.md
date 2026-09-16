# SOP: ESD Handling for PCB Assembly

**Document ID:** SOP-OP-005
**Version:** 3.1
**Effective Date:** 2024-09-01
**Department:** All Production Areas
**Applies to:** SMT Lines, Assembly-A, Assembly-B, Inspection Stations
**Review Cycle:** Annual

---

## 1. Purpose

This procedure defines Electrostatic Discharge (ESD) control measures for all personnel handling printed circuit boards (PCBs), electronic components, and assemblies at BizLink Penang Manufacturing. ESD damage is invisible but can cause latent failures in finished products.

## 2. Scope

This SOP applies to all employees, contractors, and visitors entering ESD Protected Areas (EPAs). EPAs include:
- SMT production floor (SMT-1, SMT-2, SMT-3)
- Manual assembly lines (Assembly-A, Assembly-B)
- Quality inspection stations
- Rework and repair benches
- Component storage areas

## 3. ESD Fundamentals

### 3.1 What is ESD?

Electrostatic discharge is the sudden flow of electricity between two objects at different electrical potentials. Common sources:
- Human body: Can generate 500-25,000 volts walking on carpet
- Synthetic clothing: Generates charge through friction
- Plastic packaging: Non-conductive materials trap charge

### 3.2 Damage Types

| Damage Type | Description | Detection |
|-------------|-------------|-----------|
| Catastrophic | Immediate failure, visible damage | Functional test |
| Latent | Partial damage, fails later in service | Difficult to detect, reliability risk |

**Key point:** Most ESD damage is latent and not detectable until products reach customers.

## 4. ESD Protected Area (EPA) Requirements

### 4.1 Flooring and Surfaces

- All EPA flooring is conductive or dissipative vinyl tile
- Workbenches have static-dissipative laminate surfaces (resistance: 10⁶ to 10⁹ ohms)
- Floor maintenance: Use only approved ESD floor cleaner (do not wax)

### 4.2 Grounding Points

- Common point ground terminals at each workstation (green/yellow标识)
- Verify ground connection daily using workstation checklist
- Report any damaged or missing ground points to Facilities

### 4.3 Environmental Controls

- Relative humidity: Maintain 40-60% RH
- Temperature: 22±3°C (72±5°F)
- Ionizers required at manual handling stations

## 5. Personal ESD Equipment

### 5.1 Wrist Straps

**When required:** All personnel handling exposed PCBs or components

**Procedure:**
1. Place conductive band snugly against bare skin on wrist
2. Connect coiled cord to common point ground terminal BEFORE handling ESDS items
3. Test wrist strap using daily wrist strap tester at station entrance
4. Record test result in daily log (pass/fail)

**Testing frequency:** At the start of each shift, after breaks

**Failed test actions:**
- Adjust band tension, retest
- If still fails, replace wrist strap
- Log replacement in equipment maintenance record

### 5.2 ESD Footwear

**When required:** Personnel standing at EPA workstations without wrist strap connection

**Types:**
- ESD heel straps (one on each foot)
- ESD shoes (full shoe, not just insoles)

**Testing:** Use sole resistance tester at entrance to production floor
- Pass: Resistance between 10⁵ and 10⁸ ohms

### 5.3 ESD Garments

**Required:** All personnel in EPA
- Wear provided ESD smocks (conductive fiber weave)
- Button smock fully, no exposed street clothing underneath
- Do not take smocks outside EPA (lunchroom, restrooms are non-EPA)

## 6. Handling Procedures

### 6.1 Receiving Components

1. Verify ESDS labeling on incoming packaging
2. Handle components only at grounded workstation
3. Remove from packaging only when ready to use
4. Return unused components to ESD-safe packaging immediately

### 6.2 PCB Handling

**DO:**
- Handle PCBs by edges only
- Place PCBs only on ESD-safe surfaces
- Use grounded test equipment
- Keep PCBs in ESD bags during transport between stations

**DO NOT:**
- Stack PCBs directly on top of each other
- Place PCBs on non-ESD surfaces (regular tables, plastic bins)
- Touch component leads or pads directly
- Pass PCBs hand-to-hand without both parties grounded

### 6.3 Transport and Storage

- Use ESD tote bins for inter-station transport
- Ensure all storage shelves have conductive/dissipative surfaces
- Desiccant and humidity indicator cards required for long-term storage

## 7. Equipment and Packaging

### 7.1 ESD-Safe Packaging Materials

| Material | Use Case |
|----------|----------|
| Pink poly bags | Short-term storage, transport within EPA |
| Shielding bags | Long-term storage, shipping outside EPA |
| Conductive tote bins | WIP storage, inter-station transport |
| Black conductive foam | IC/component storage in trays |

### 7.2 Test Equipment Grounding

- All test equipment chassis connected to protective earth
- Test leads and probes checked for insulation damage weekly
- Use ESD-safe soldering stations with grounded tips

## 8. Ionizer Use

### 8.1 Purpose

Ionizers neutralize static charges on insulators and isolated conductors that cannot be grounded.

### 8.2 Locations

- Manual inspection stations (Assembly-A, Assembly-B)
- Rework benches
- Component counting areas

### 8.3 Maintenance

- Clean emitter points weekly using ionizer cleaning kit
- Verify ion balance monthly using charged plate monitor
- Target ion balance: ±50 volts or better
- Log calibration results in preventive maintenance record

## 9. Training Requirements

| Personnel | Initial Training | Refresher |
|-----------|------------------|-----------|
| Production operators | 2-hour ESD awareness | Annual, 30 minutes |
| Technicians | 4-hour ESD control | Annual, 1 hour |
| Visitors | 10-minute briefing | Each visit |
| Contractors | 1-hour site-specific | Each project |

## 10. Audit and Compliance

- Daily: Workstation grounding verification, wrist strap testing logs
- Weekly: Ionizer cleanliness check, ESD garment condition
- Monthly: EPA compliance walk-through by Quality
- Quarterly: Full ESD audit per ANSI/ESD S20.20

**Non-compliance consequences:**
- First occurrence: Verbal reminder and re-training
- Repeated occurrences: Documented in personnel record, discussed in performance review

## 11. References

- ANSI/ESD S20.20: ESD Association Standard
- IEC 61340-5-1: ESD Control Program
- SOP-OP-001: SMT Line Changeover Procedure
- Company Quality Manual, Section 7.5.3

## 12. Revision History

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | 2022-01-10 | Initial release | M. Tanaka |
| 2.0 | 2023-05-20 | Added ionizer section | S. Lim |
| 3.0 | 2024-03-15 | Updated training matrix | A. Rahman |
| 3.1 | 2024-09-01 | Clarified footwear testing | L. Chen |

---

**Document Owner:** Quality Assurance Manager
**Next Review Date:** September 2025
