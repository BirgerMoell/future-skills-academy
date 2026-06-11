/* Future Skills Academy — shared platform behavior */
(function () {
  "use strict";

  /* MailerLite email course form (account 2425863, form "MTS email course").
     While empty, all signup blocks stay hidden. */
  var SUBSCRIBE_URL =
    "https://assets.mailerlite.com/jsonp/2425863/forms/189985464562746867/subscribe";

  var STORAGE_KEY = "fsa-progress-v1";
  var SUBSCRIBED_KEY = "fsa-subscribed";

  function track(eventName) {
    if (window.goatcounter && window.goatcounter.count) {
      window.goatcounter.count({ path: eventName, event: true });
    }
  }

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

  function isSubscribed() {
    try {
      return localStorage.getItem(SUBSCRIBED_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function markSubscribed() {
    try {
      localStorage.setItem(SUBSCRIBED_KEY, "1");
    } catch (e) {
      /* ignore */
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

  /* email capture: enable blocks when Kit is configured */
  function wireCaptureForm(block) {
    var form = block.querySelector("form");
    if (!form) return;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var email = form.querySelector('input[name="email_address"]').value;
      var button = form.querySelector("button");
      button.disabled = true;
      button.textContent = "Signing you up…";
      var data = new FormData();
      data.append("fields[email]", email);
      data.append("ml-submit", "1");
      data.append("anticsrf", "true");
      fetch(SUBSCRIBE_URL, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: data,
      })
        .then(function (response) {
          if (!response.ok) throw new Error("subscribe failed");
          form.outerHTML =
            '<p class="email-capture-success">Almost there — check your inbox and confirm your email. Lesson one follows right after. (Not there? Check spam and drag us out.)</p>';
          markSubscribed();
          track("Email Signup");
        })
        .catch(function () {
          button.disabled = false;
          button.textContent = "Try again";
        });
    });
  }

  if (SUBSCRIBE_URL) {
    document.querySelectorAll("[data-email-capture]").forEach(function (block) {
      if (isSubscribed()) return;
      block.classList.add("is-enabled");
      wireCaptureForm(block);
    });
  }

  var progress = loadProgress();

  /* after the first lesson completion, offer the email course inline — once */
  function injectPostCompleteCapture(lesson) {
    if (!SUBSCRIBE_URL || isSubscribed()) return;
    if (document.querySelector("[data-post-complete-capture]")) return;
    var template = document.getElementById("post-complete-capture");
    if (!template) return;
    var body = lesson.querySelector(".lesson-body");
    if (!body) return;
    var clone = template.content.firstElementChild.cloneNode(true);
    clone.setAttribute("data-post-complete-capture", "");
    clone.classList.add("is-enabled");
    body.appendChild(clone);
    wireCaptureForm(clone);
  }

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
        track("Lesson Complete");
        injectPostCompleteCapture(lesson);
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

  /* outbound booking clicks (for-companies page) */
  document.querySelectorAll("[data-booking]").forEach(function (el) {
    el.addEventListener("click", function () {
      track("Booking Click");
    });
  });
})();
