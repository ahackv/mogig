# MOGIG: Micro-meteorite and Other General Information Gatherer

## Project Overview

MOGIG is a high-altitude balloon project by Year 9 students from Cambridge, UK.

Our mission is to launch a scientific payload into the Earth's upper atmosphere to conduct a series of experiments, gather data, and capture breathtaking footage of our planet from near space.

We aim to explore:
- atmospheric changes
- the effects of extreme environments on biological matter
- fundamental physics principles
- and attempt to collect elusive micrometeorites

This project combines elements of physics, chemistry, biology, computer science, and engineering, challenging us to design, build, test, and analyze a complex system with a limited budget.

## Experiments

Our payload will carry the following key experiments:

### 1. Chemistry: The Great Gas Detective
*   **Objective:** To profile the concentration of Carbon Dioxide (CO2) as altitude increases and correlate this with changes in air pressure and temperature.
*   **Method:** A CO2 sensor (MH-Z19B), pressure, and temperature sensor (BME280) will continuously log data. We expect to see a decrease in CO2 concentration and pressure with increasing altitude.
*   **Expected Significance:** Direct measurement and visualization of atmospheric composition changes, confirming the "thinning" of gases high above the Earth.

### 2. Biology A: The Incredible Expanding/Shrinking Food (Tiered Exposure)
*   **Objective:** To observe and quantify the physical effects of varying degrees of high-altitude exposure (low pressure, extreme cold, UV radiation) on different food items (e.g., marshmallow, grape, apple slice, dry sponge).
*   **Method:** Identical sets of samples will be subjected to:
    *   **Tier 1 (Full Harsh Exposure):** Mounted externally to the payload.
    *   **Tier 2 (Sheltered Low-Pressure Exposure):** Housed in a vented, clear container offering some protection from wind/direct cold but exposed to low pressure.
    *   **Tier 3 (Payload Internal Control):** Kept inside the insulated main payload.
    *   **Tier 4 (Ground Control):** An identical set remaining at ground level.
    Pre- and post-flight observations (visual, mass) will be recorded.
*   **Expected Significance:** Visual and quantitative demonstration of how extreme environmental stressors impact cellular structures and water content.

### 3. Biology B: Enzyme Activity Under Pressure (and Cold)
*   **Objective:** To investigate whether exposure to the extreme cold and low-pressure conditions at high altitude affects the activity of a biological enzyme (e.g., catalase).
*   **Method:** Two samples of an enzyme solution will be prepared. One (experimental) will be flown exposed to the external environment (within a sealed vial), while the other (control) will remain on the ground or inside the insulated payload. Post-flight, the activity of both samples will be compared.
*   **Expected Significance:** Provides insight into the resilience of complex biological molecules to near-space conditions.

### 4. Physics: UV Radiation Shield Showdown
*   **Objective:** To visually demonstrate the increased intensity of UV radiation at high altitudes and test the effectiveness of various materials as UV shields.
*   **Method:** UV color-changing beads will be mounted on an external panel. Different batches will be left uncovered or shielded by various materials (e.g., glass, plastic, sunscreen-coated film). The intensity of color change post-flight will indicate UV exposure and shield effectiveness.
*   **Expected Significance:** Tangible demonstration of an invisible but important atmospheric property and material science application.

### 5. Micrometeorite Collection
*   **Objective:** To attempt the collection of micrometeorites.
*   **Method:** A specialized collection surface will be deployed on the payload, designed to open at high altitude and close before descent to minimize terrestrial contamination.

## Tech Stack

*   **Primary Controller:** Raspberry Pi (Model TBD, likely Pi Zero 2 W)
*   **Programming Language:** Python
*   **Sensors:**
    *   GPS Module (for location and altitude)
    *   BME280 (Temperature, Pressure, Humidity)
    *   MH-Z19B (CO2 Sensor)
    *   (Potential for O2 sensor if budget/complexity allows)
*   **Camera:** Raspberry Pi Camera Module
*   **Data Storage:** High Endurance MicroSD Card

## Team & Approach

We are Year 9 students from Chesterton Community College in Cambridge, UK.

Our approach involves:
*   Iterative design and prototyping.
*   Thorough testing of individual components and integrated systems, including smaller test launches.
*   Careful data logging and analysis.
*   Adherence to safety regulations and best practices for high-altitude ballooning.

## Stretch Goals
If time and resources permit, we aim to:
*   Attempt live data telemetry (short-range or via amateur radio if feasible and licensed)
*   Challenge ourselves with Machine Learning to identify landmarks from flight footage
*   Maybe, just maybe, set some silly world record (highest flying marshmallow anyone? :)
