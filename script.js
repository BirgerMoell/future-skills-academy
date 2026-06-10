/* Future Skills Academy — shared platform behavior */
(function () {
  "use strict";

  var STORAGE_KEY = "fsa-progress-v1";

  function loadProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function saveProgress(progress) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    } catch (e) {
      /* private mode — progress just won't persist */
    }
  }

  /* header scroll state */
  var header = document.querySelector("[data-header]");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* reveal on scroll */
  var revealed = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealed.length) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealed.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    revealed.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  var progress = loadProgress();

  /* track pages: mark-done buttons + progress bar */
  var lessons = document.querySelectorAll(".lesson[data-lesson]");
  var progressLabel = document.querySelector("[data-progress-label]");
  var progressFill = document.querySelector("[data-progress-fill]");

  function refreshTrackProgress() {
    if (!lessons.length) return;
    var done = 0;
    lessons.forEach(function (lesson) {
      if (progress[lesson.dataset.lesson]) done += 1;
    });
    if (progressLabel) {
      progressLabel.textContent = done + " of " + lessons.length + " lessons complete";
    }
    if (progressFill) {
      progressFill.style.width = (done / lessons.length) * 100 + "%";
    }
  }

  lessons.forEach(function (lesson) {
    var id = lesson.dataset.lesson;
    if (progress[id]) lesson.classList.add("is-done");

    var button = lesson.querySelector(".mark-done");
    if (!button) return;
    button.textContent = progress[id] ? "Completed ✓" : "Mark complete";
    button.addEventListener("click", function () {
      var isDone = !progress[id];
      if (isDone) {
        progress[id] = true;
      } else {
        delete progress[id];
      }
      lesson.classList.toggle("is-done", isDone);
      button.textContent = isDone ? "Completed ✓" : "Mark complete";
      saveProgress(progress);
      refreshTrackProgress();
    });
  });

  refreshTrackProgress();

  /* landing page: per-pillar progress counters */
  document.querySelectorAll("[data-track-progress]").forEach(function (el) {
    var prefix = el.dataset.trackProgress;
    var total = parseInt(el.dataset.trackTotal, 10) || 0;
    var done = Object.keys(progress).filter(function (key) {
      return key.indexOf(prefix + "-") === 0;
    }).length;
    if (done > 0 && total > 0) {
      el.textContent = done + " / " + total + " lessons";
    }
  });
})();
