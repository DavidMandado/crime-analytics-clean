# Australia Shark Incidents Visualization

This project visualizes historical shark incidents around Australia. It uses **Mapbox GL JS** for the map, **Chart.js** for charts, and **noUiSlider** for range sliders. The user can:

- **Hover** over states to see aggregated incident counts (heatmap view).  
- Toggle to a **dot** view with a Bluetooth-style toggle switch.  
- **Filter** incidents by year, month, state, shark type, etc.  
- **Click** a state (in heatmap mode) to open a modal with a line chart (incidents over time) and bar chart (incidents by shark type) specifically for that state.  
- View **analysis** charts (body part distribution, monthly fatal vs. non-fatal trends) in a separate analysis window.

---

## 1) How to Run

1. **Clone or download** this repository to your machine.  
2. Confirm you have an **internet connection**, because the project references Mapbox’s CDN and requires a valid **Mapbox token** in the code (already provided in `index.html`).  
3. **Open** the file `index.html` in a modern browser (Chrome or Firefox recommended).  
   - If your browser blocks local resources, run a simple local server (e.g. `python -m http.server`) and then navigate to `http://localhost:8000/index.html`.  
4. A map of Australia should load.  
5. Toggle between **heatmap** and **dot** layers via the “Toggle View” switch (bottom right).  
6. In **dot** mode, you can show/hide filters and the analysis window.  
7. In **heatmap** mode, clicking a state pops up a modal with state-specific charts.

---

## 2) Files in This Project

- **`index.html`**  
  - Contains all the HTML, JavaScript, and CSS for the main page.  
  - Loads the `sharkdataset.json` from the same directory (or an `assets/` folder, depending on your structure).  
  - Integrates libraries (Mapbox GL, Chart.js, noUiSlider) via `<script>` tags.

- **`sharkdataset.json`**  
  - The JSON data file containing shark incidents.  

- **(Optional) README.md (this file)**  
  - Explains how to run the project, what code is ours, how we used libraries, etc.

Because we designed this as a **single-page application**, everything is self-contained in `index.html` (aside from the data file). This simplifies deployment: just open the HTML file in a browser.

---

## 3) What We Implemented vs. Libraries/Existing Code

- **Our own implementation**:
  - The **filtering logic** (building `filterArray` from year/month sliders, state checkboxes, etc.).  
  - The **aggregation** for state-level charts (counts by year, by shark type).  
  - The **UI** code for the filter window, analysis window, toggling layers, showing modals, etc.  
  - The **map interactions** (clicking a state, toggling between heatmap/dots).

- **From external sources**:
  - **Mapbox GL JS** for base map rendering and layers.  
  - **Chart.js** for line/bar charts.  
  - **noUiSlider** for the dual-handle range sliders.  
  - Small snippets from official examples (e.g., how to initialize a map, set up a bar chart).

We combined these libraries in a custom way to meet our project’s requirements.

---

## 4) Does It Run?

- **Yes**: The code has been tested in Chrome/Firefox.  
- If you encounter issues with local file access or a missing Mapbox token, run a simple server or check network logs.

---

## 5) Code Comments & Structure

- The code is organized into logical blocks:
  1. **Map & global setup** (Mapbox token, layer IDs).  
  2. **Chart.js references** and helper functions for creating charts.  
  3. **Map load** event logic (initial heatmap, legend creation).  
  4. **Dot hover** logic.  
  5. **Click on a state** to show a modal with charts.  
  6. **Filter logic** (sliders, checkboxes, etc.).  
  7. **Toggle** between heatmap and dots.  
  8. **Analysis** charts in a separate window.

We’ve added comments in each section explaining what it does, to ensure the code is readable and not “spaghetti.”

---

## 6) Matching Our Screencast / Demo

If there is a screencast demonstration, this code replicates exactly what’s shown (the map, filters, toggles, and charts).

---

## 7) Complexity Level

We label this as **medium** complexity because:

- It integrates multiple libraries (Mapbox, Chart.js, noUiSlider).  
- It has a custom multi-step filtering system.  
- It displays multiple chart types (bar, line) and dynamic modals.  

It’s still a single-page front-end (no separate back-end), so we’re not calling it “high” complexity.

---

## 8) How Much Code We Wrote Ourselves

We estimate we wrote around **70–80%** of the final JS logic. The rest are boilerplate or library integrations:

- We heavily customized the event handling, data filtering, and chart data logic.  
- We used official library docs/examples for initial set-up.

---

## 9) Framework?

We did **not** use React, Angular, or D3. We relied on **Mapbox GL** for mapping, **Chart.js** for charting, and **noUiSlider** for the dual sliders. Plain JavaScript ties everything together.

---

## Summary

- **Documents**: This README fulfills the requirement for describing how to run the tool and indicating what code we wrote vs. library usage.  
- **Code**: Runs fully in a modern browser.  
- **Comments**: Our `index.html` is well-commented in each functional block.  
- **Complexity**: Medium.  
- **Implementation**: Mostly ours, with some library-based boilerplate.  
    