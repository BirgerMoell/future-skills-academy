const header = document.querySelector("[data-header]");
const progress = document.querySelector(".progress");
const reveals = document.querySelectorAll(".reveal");
const heroLogo = document.querySelector(".hero-logo");

const setScrollState = () => {
  const scrollTop = window.scrollY;
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const percent = maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0;

  header.classList.toggle("is-scrolled", scrollTop > 16);
  progress.style.width = `${percent}%`;

  heroLogo?.style.setProperty("--drift", `${scrollTop * 0.025}px`);
};

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
      }
    });
  },
  { threshold: 0.22 }
);

reveals.forEach((element) => observer.observe(element));

window.addEventListener("scroll", setScrollState, { passive: true });
window.addEventListener("resize", setScrollState);
setScrollState();
