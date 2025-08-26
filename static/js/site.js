import { initNavToggle } from "./utils/nav-toggle.js";
import { adjustMainMargin } from "./utils/layout-utils.js";

document.addEventListener("DOMContentLoaded", () => {
  initNavToggle();
  adjustMainMargin();
});

// Run on resize to keep it responsive
window.addEventListener("resize", adjustMainMargin);