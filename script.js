const year = document.querySelector("[data-year]");
if (year) {
  year.textContent = String(new Date().getFullYear());
}

const links = Array.from(document.querySelectorAll('.nav a[href^="#"]'));
const sections = links
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

if ("IntersectionObserver" in window && sections.length > 0) {
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (!visible) {
        return;
      }

      links.forEach((link) => {
        link.classList.toggle("is-active", link.getAttribute("href") === `#${visible.target.id}`);
      });
    },
    { rootMargin: "-20% 0px -62% 0px", threshold: [0.1, 0.25, 0.5] }
  );

  sections.forEach((section) => observer.observe(section));
}
