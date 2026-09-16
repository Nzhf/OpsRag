# SOP: Manual Soldering and Rework Procedure

**Document ID:** SOP-OP-006
**Version:** 2.1
**Effective Date:** 2024-11-01
**Department:** Production (Assembly-A, Assembly-B), Rework Station
**Applies to:** All manual soldering operations
**Review Cycle:** Annual

---

## 1. Purpose

This procedure establishes requirements for manual soldering and rework operations at BizLink Penang Manufacturing. Proper soldering technique ensures reliable connections and prevents damage to components and PCBs.

## 2. Scope

This SOP applies to:
- Through-hole component soldering
- SMT component rework and touch-up
- Wire termination and cable assembly
- Repair of solder defects

Exclusions:
- Wave solder operations (covered by SOP-OP-003)
- BGA rework (requires specialized equipment, covered by SOP-OP-009)

## 3. Responsibilities

| Role | Responsibility |
|------|----------------|
| Rework Technician | Perform soldering/rework, maintain equipment |
| Quality Inspector | Verify rework quality, approve first article |
| Production Supervisor | Authorize non-standard rework |
| Process Engineer | Define temperature profiles, approve rework methods |

## 4. Equipment and Materials

### 4.1 Soldering Stations

| Station Type | Use Case | Temperature Range |
|--------------|----------|-------------------|
| Weller WES51 | General soldering, through-hole | 200-480°C |
| Hakko FX-951 | Fine-pitch SMT, precision work | 200-500°C |
| Metcal MX-5200 | Heavy ground planes, high thermal demand | Auto-adjusting |

### 4.2 Solder Materials

| Type | Specification | Application |
|------|---------------|-------------|
| Solder wire | Sn96.5/Ag3.0/Cu0.5 (SAC305), 0.5mm | General lead-free soldering |
| Solder wire | Sn96.5/Ag3.0/Cu0.5 (SAC305), 0.3mm | Fine-pitch SMT |
| Solder paste | SAC305 Type 4 | SMT rework (dispense) |
| Flux | No-clean, ROL0 per J-STD-004 | Improve wetting |
| Desoldering braid | 1.0mm, 2.0mm widths | Solder removal |

### 4.3 Tip Selection

| Tip Type | Application |
|----------|-------------|
| Chisel (1.2mm, 2.0mm) | Through-hole, general work |
| Conical (fine) | SMT touch-up, precision work |
| Knife | Drag soldering, multi-lead components |
| Hoof | SMT rework, paste dispensing |

## 5. Soldering Fundamentals

### 5.1 Heat Transfer Principles

Successful soldering requires:
1. **Clean surfaces:** Oxidation prevents wetting
2. **Proper temperature:** Hot enough to melt solder, not damage components
3. **Thermal bridge:** Molten solder conducts heat from iron to joint
4. **Adequate time:** 2-5 seconds typical for lead-free

### 5.2 Solder Joint Criteria (per IPC-A-610 Class 2)

**Good solder joint characteristics:**
- Shiny or satin appearance (lead-free may be grainier)
- Concave fillet shape (wetting angle < 90°)
- Complete coverage of pad and lead
- No cracks, voids, or inclusions
- Lead outline visible through fillet

**Acceptable vs. Defect:**
- Minor voids in through-hole barrel: Acceptable if < 25% of barrel
- Slightly dull surface for lead-free: Acceptable
- Insufficient wetting on pad: Defect - requires rework

## 6. Soldering Procedure

### 6.1 Preparation

1. **Verify ESD protection:**
   - Wear grounded wrist strap
   - Work on ESD-safe mat
   - Use ionizer if handling components removed from packaging

2. **Inspect PCB and components:**
   - Verify correct component per work instruction
   - Check for damage (bent leads, contamination)
   - Clean pads if oxidized (use flux or gentle abrasion)

3. **Set up soldering station:**
   - Select appropriate tip for job
   - Set temperature per solder manufacturer recommendation:
     - SAC305 wire: 350-380°C typical
     - Fine-pitch: Lower end to avoid damage
     - Heavy thermal mass: Higher temperature or preheat

4. **Clean and tin tip:**
   - Wipe tip on damp sponge or brass wool
   - Apply fresh solder to tip (tinning improves heat transfer)
   - Verify tip is clean and shiny

### 6.2 Through-Hole Soldering

1. Insert component, verify orientation (polarized components)
2. Secure component (bend leads slightly if needed)
3. Place soldering iron tip to contact both pad and lead simultaneously
4. Feed solder to opposite side of joint (not directly to tip)
5. Allow solder to flow around lead and fill barrel
6. Remove solder wire, then iron (1-2 seconds apart)
7. Inspect joint immediately
8. Trim leads to 1.0-2.0mm above solder surface (if required)

**Timing:** Complete joint in 3-5 seconds maximum

### 6.3 SMT Touch-Up and Rework

**For solder bridges:**
1. Apply flux to bridged area
2. Use fine chisel or knife tip with clean face
3. Touch tip to bridge, allow surface tension to draw solder to iron
4. Use desoldering braid if bridge persists

**For insufficient solder:**
1. Apply flux to joint
2. Touch tip with small solder amount to joint
3. Allow solder to flow onto pad and lead
4. Remove iron, allow to cool undisturbed

**For tombstones (billboarding):**
1. Apply flux to both pads
2. Use tweezers to align component
3. Touch iron to one end, allow solder to reflow
4. Solder second end
5. Verify component is seated flat

### 6.4 Component Removal (Rework)

**Through-hole removal:**
1. Apply flux to joints
2. Use desoldering pump or braid to remove bulk solder
3. Heat each lead while gently rocking component
4. Remove component once all leads are free
5. Clean holes using desoldering braid or pump
6. Verify holes are clear for new component insertion

**SMT removal (2-lead and chip components):**
1. Apply flux to both ends
2. Use two irons (one each end) or single iron with wide tip
3. Simultaneously heat both ends, lift component with tweezers
4. Clean pads using braid and flux
5. Apply fresh solder paste or tin pads for new component

## 7. Post-Soldering

### 7.1 Cleaning

For no-clean flux:
- Typically no cleaning required
- If flux residue is excessive, clean with approved no-clean flux remover

For rosin-based flux (if used):
- Clean with isopropyl alcohol (IPA) or flux remover
- Verify no residue remains per visual inspection

### 7.2 Inspection

Inspect all soldered joints for:
- Proper wetting and fillet formation
- No bridges, cold joints, or insufficient solder
- Component orientation correct
- No damage to PCB or adjacent components

Use 10x magnification for critical joints.

### 7.3 Documentation

Complete Rework Traveler with:
- Component reference designators reworked
- Technician ID and date
- Quantity of units reworked
- Any non-conformances noted

## 8. Temperature Limits and Thermal Sensitivity

### 8.1 Component Temperature Limits

| Component Type | Max Soldering Temp | Max Duration |
|----------------|-------------------|--------------|
| Standard ICs | 260°C | 10 seconds per joint |
| Temperature-sensitive ICs | 250°C | 5 seconds per joint |
| Electrolytic capacitors | 250°C | 5 seconds (avoid heating body) |
| LEDs | 260°C | 3 seconds (avoid heating lens) |
| Connectors | 260°C | 10 seconds per pin |

**Note:** Check component datasheet for specific limits. Some automotive-grade components have stricter requirements.

### 8.2 Thermal Shock Prevention

- Do not apply iron directly to component body
- Allow joint to cool naturally (do not blow on joint)
- For repeated rework on same joint, allow 30-second cooling between attempts
- Use preheat (hot air or preheater) for boards with large ground planes

## 9. Safety

### 9.1 Personal Protection

- Safety glasses required at all times
- Avoid inhaling flux fumes (use fume extraction)
- Do not touch soldering iron tip or heated components
- Wash hands after handling solder (lead-free still contains metals)

### 9.2 Fire Prevention

- Keep soldering iron in holder when not in use
- Never leave hot iron unattended
- Keep flammable materials away from soldering area
- Know location of fire extinguisher

### 9.3 Fume Extraction

- Use benchtop fume extractor or overhead extraction arm
- Maintain filter per manufacturer schedule
- Replace activated carbon filters when odor detected

## 10. Equipment Maintenance

### 10.1 Daily Checks

- [ ] Station powers on and reaches set temperature
- [ ] Tip is clean and properly tinned
- [ ] Sponge is damp (not soaking wet)
- [ ] Extraction system operating

### 10.2 Weekly Maintenance

- Clean tip shank and heating element contact area
- Check and tighten tip retention collar
- Clean sponge, replace if degraded
- Verify temperature calibration using tip thermometer

### 10.3 Tip Care

- Always tin tip before storing
- Use tip tinner/cleaner (type T18) for oxidized tips
- Replace tips when pitted or not accepting solder
- Typical tip life: 3-6 months with proper care

## 11. Training and Certification

| Level | Training | Skills Demonstrated |
|-------|----------|---------------------|
| Level 1 | 8-hour course + practical test | Basic through-hole soldering |
| Level 2 | Level 1 + 16-hour advanced course | SMT rework, fine-pitch soldering |
| Level 3 | Level 2 + 8-hour specialist course | IPC-A-610 CIS certification, training others |

**Recertification:** Every 2 years or when major process changes occur

## 12. References

- IPC J-STD-001: Requirements for Soldered Electrical and Electronic Assemblies
- IPC-A-610: Acceptability of Electronic Assemblies
- J-STD-004: Requirements for Soldering Fluxes
- Solder manufacturer technical datasheet

## 13. Revision History

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | 2023-01-15 | Initial release | K. Singh |
| 2.0 | 2024-06-01 | Added SMT rework procedures | L. Chen |
| 2.1 | 2024-11-01 | Updated temperature limits table | A. Rahman |

---

**Document Owner:** Production Manager
**Next Review Date:** November 2025
