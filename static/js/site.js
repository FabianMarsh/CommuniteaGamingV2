import { initNavToggle } from "./nav-toggle.js";
import { adjustMainMargin } from "./layout-utils.js";

document.addEventListener("DOMContentLoaded", () => {
  initNavToggle();
  adjustMainMargin();
});

// Run on resize to keep it responsive
window.addEventListener("resize", adjustMainMargin);