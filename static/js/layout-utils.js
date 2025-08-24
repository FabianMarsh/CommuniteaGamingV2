export function adjustMainMargin() {
  const header = document.querySelector("header");
  const main = document.querySelector("main");

  if (header && main) {
    const headerHeight = header.offsetHeight -1;
    main.style.marginTop = `${headerHeight}px`;
  }
}