/* ══════════════════════════════════════════════════════════════
   Aliança de IA para a Educação — Interatividade
   ══════════════════════════════════════════════════════════════ */

(function () {
    "use strict";

    /* ── TOC Scroll Spy ──────────────────────────────────────── */
    function initScrollSpy() {
        var tocLinks = document.querySelectorAll(".toc-link");
        if (!tocLinks.length) return;

        var headings = [];
        tocLinks.forEach(function (link) {
            var id = link.getAttribute("href").slice(1);
            var el = document.getElementById(id);
            if (el) headings.push({ el: el, link: link });
        });

        if (!headings.length) return;

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        tocLinks.forEach(function (l) {
                            l.classList.remove("active");
                        });
                        var match = headings.find(function (h) {
                            return h.el === entry.target;
                        });
                        if (match) {
                            match.link.classList.add("active");
                            // Scroll TOC into view if needed
                            var sidebar = document.getElementById("doc-sidebar");
                            if (sidebar && sidebar.scrollHeight > sidebar.clientHeight) {
                                match.link.scrollIntoView({ block: "nearest", behavior: "smooth" });
                            }
                        }
                    }
                });
            },
            {
                rootMargin: "-80px 0px -65% 0px",
                threshold: 0,
            }
        );

        headings.forEach(function (h) {
            observer.observe(h.el);
        });
    }

    /* ── Smooth Scroll for TOC links ─────────────────────────── */
    function initSmoothScroll() {
        document.querySelectorAll(".toc-link").forEach(function (link) {
            link.addEventListener("click", function (e) {
                var targetId = this.getAttribute("href").slice(1);
                var target = document.getElementById(targetId);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                    // Close sidebar on mobile after clicking
                    var sidebar = document.getElementById("doc-sidebar");
                    if (sidebar) sidebar.classList.remove("open");
                }
            });
        });
    }

    /* ── TOC Toggle (mobile) ─────────────────────────────────── */
    function initTocToggle() {
        var toggle = document.getElementById("toc-toggle");
        var sidebar = document.getElementById("doc-sidebar");
        var close = document.getElementById("sidebar-close");

        if (!toggle || !sidebar) return;

        toggle.addEventListener("click", function (e) {
            e.stopPropagation();
            sidebar.classList.toggle("open");
        });

        if (close) {
            close.addEventListener("click", function () {
                sidebar.classList.remove("open");
            });
        }

        // Close on click outside
        document.addEventListener("click", function (e) {
            if (
                sidebar.classList.contains("open") &&
                !sidebar.contains(e.target) &&
                e.target !== toggle &&
                !toggle.contains(e.target)
            ) {
                sidebar.classList.remove("open");
            }
        });
    }

    /* ── Mobile Header Menu ──────────────────────────────────── */
    function initMobileMenu() {
        var btn = document.getElementById("mobile-menu-toggle");
        var nav = document.getElementById("header-nav");
        if (!btn || !nav) return;

        btn.addEventListener("click", function () {
            var isOpen = nav.classList.toggle("open");
            btn.classList.toggle("is-open", isOpen);
            btn.setAttribute("aria-expanded", isOpen);
        });

        // Close when clicking a nav link
        nav.querySelectorAll("a").forEach(function (a) {
            a.addEventListener("click", function () {
                nav.classList.remove("open");
                btn.classList.remove("is-open");
                btn.setAttribute("aria-expanded", "false");
            });
        });

        // Close on outside click
        document.addEventListener("click", function (e) {
            if (
                nav.classList.contains("open") &&
                !nav.contains(e.target) &&
                !btn.contains(e.target)
            ) {
                nav.classList.remove("open");
                btn.classList.remove("is-open");
                btn.setAttribute("aria-expanded", "false");
            }
        });
    }

    /* ── Interactive Checkboxes ──────────────────────────────── */
    function initCheckboxes() {
        var pageKey = window.location.pathname;
        var saved = {};
        try {
            saved = JSON.parse(localStorage.getItem("cb_" + pageKey) || "{}");
        } catch (e) { /* ignore */ }

        var checkboxes = document.querySelectorAll(
            '.markdown-body input[type="checkbox"]'
        );
        checkboxes.forEach(function (cb, i) {
            var key = "cb_" + i;
            // Restore saved state
            if (saved[key] !== undefined) {
                cb.checked = saved[key];
            }
            // Enable interaction
            cb.removeAttribute("disabled");
            cb.addEventListener("change", function () {
                saved[key] = cb.checked;
                try {
                    localStorage.setItem("cb_" + pageKey, JSON.stringify(saved));
                } catch (e) { /* ignore */ }

                // Brief visual feedback
                var li = cb.closest("li");
                if (li) {
                    li.style.transition = "opacity 0.15s";
                    li.style.opacity = cb.checked ? "0.6" : "1";
                    setTimeout(function () { li.style.opacity = "1"; }, 200);
                }
            });
        });

        // Update checked visual style
        updateCheckboxVisuals(checkboxes);
    }

    function updateCheckboxVisuals(checkboxes) {
        checkboxes.forEach(function (cb) {
            var li = cb.closest("li");
            if (li && cb.checked) {
                li.style.opacity = "0.65";
            }
        });
    }

    /* ── Staggered entrance for cards ────────────────────────── */
    function initCardAnimations() {
        if (!("IntersectionObserver" in window)) return;

        var cards = document.querySelectorAll(".material-card, .outra-card");
        if (!cards.length) return;

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry, idx) {
                    if (entry.isIntersecting) {
                        entry.target.style.animationDelay = (idx * 0.04) + "s";
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
        );

        cards.forEach(function (card) {
            card.style.opacity = "0";
            card.style.transform = "translateY(8px)";
            card.style.transition = "opacity 0.4s cubic-bezier(0.22,1,0.36,1), transform 0.4s cubic-bezier(0.22,1,0.36,1)";
            observer.observe(card);
        });
    }

    // Handle the is-visible class
    var style = document.createElement("style");
    style.textContent = ".is-visible { opacity: 1 !important; transform: translateY(0) !important; }";
    document.head.appendChild(style);

    /* ── Reading progress bar (document pages) ───────────────── */
    function initReadingProgress() {
        var content = document.querySelector(".doc-body");
        if (!content) return;

        var bar = document.createElement("div");
        bar.setAttribute("aria-hidden", "true");
        bar.style.cssText =
            "position:fixed;top:0;left:0;height:3px;background:var(--persona-color,#2b6cb0);z-index:101;transition:width 0.1s linear;width:0;pointer-events:none;opacity:0.7;";
        document.body.appendChild(bar);

        function updateBar() {
            var rect = content.getBoundingClientRect();
            var total = content.scrollHeight;
            var scrolled = -rect.top;
            var visible = window.innerHeight;
            var progress = Math.min(Math.max(scrolled / (total - visible), 0), 1);
            bar.style.width = (progress * 100) + "%";
        }

        window.addEventListener("scroll", updateBar, { passive: true });
        updateBar();
    }

    /* ── Scroll automático para item ativo na journey sidebar ── */
    function initJourneyActiveScroll() {
        var active = document.querySelector(".journey-item--active");
        if (!active) return;
        setTimeout(function () {
            active.scrollIntoView({ block: "nearest", behavior: "auto" });
        }, 60);
    }

    /* ── Navegação por teclado: ← anterior / → próximo ──────── */
    function initKeyboardNav() {
        var prevBtn = document.querySelector(".doc-nav-btn--prev");
        var nextBtn = document.querySelector(".doc-nav-btn--next");
        if (!prevBtn && !nextBtn) return;

        document.addEventListener("keydown", function (e) {
            var tag = document.activeElement && document.activeElement.tagName;
            if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
            if (e.altKey || e.ctrlKey || e.metaKey) return;

            if (e.key === "ArrowLeft" && prevBtn) {
                e.preventDefault();
                window.location.href = prevBtn.getAttribute("href");
            } else if (e.key === "ArrowRight" && nextBtn) {
                e.preventDefault();
                window.location.href = nextBtn.getAttribute("href");
            }
        });
    }

    /* ── Critérios: abas ET/AP/CC + acordeão + deep-link ─────── */
    function initCriterios() {
        var tabs = document.querySelectorAll(".crit-tab");
        if (!tabs.length) return;

        function activateBloco(bloco) {
            tabs.forEach(function (t) {
                var on = t.getAttribute("data-bloco") === bloco;
                t.classList.toggle("active", on);
                t.setAttribute("aria-selected", on ? "true" : "false");
            });
            document.querySelectorAll(".crit-painel").forEach(function (p) {
                var on = p.id === "painel-" + bloco;
                p.classList.toggle("hidden", !on);
                if (on) { p.removeAttribute("hidden"); }
                else { p.setAttribute("hidden", ""); }
            });
        }

        tabs.forEach(function (tab) {
            tab.addEventListener("click", function () {
                activateBloco(tab.getAttribute("data-bloco"));
            });
        });

        // Acordeão (abrir/fechar critério)
        function setOpen(card, toggle, corpo, open) {
            toggle.setAttribute("aria-expanded", open ? "true" : "false");
            card.classList.toggle("is-open", open);
            if (open) { corpo.removeAttribute("hidden"); }
            else { corpo.setAttribute("hidden", ""); }
        }

        document.querySelectorAll(".crit-card").forEach(function (card) {
            var toggle = card.querySelector(".crit-card-toggle");
            var corpo = card.querySelector(".crit-card-corpo");
            if (!toggle || !corpo) return;
            toggle.addEventListener("click", function () {
                var open = toggle.getAttribute("aria-expanded") === "true";
                setOpen(card, toggle, corpo, !open);
            });
            var fechar = corpo.querySelector(".crit-fechar");
            if (fechar) {
                fechar.addEventListener("click", function () {
                    setOpen(card, toggle, corpo, false);
                    card.scrollIntoView({ block: "nearest", behavior: "smooth" });
                });
            }
        });

        // Deep-link: abrir aba + critério a partir de #id
        function openFromHash() {
            var id = (window.location.hash || "").slice(1);
            if (!id) return;
            var card = document.getElementById(id);
            if (!card || !card.classList.contains("crit-card")) return;
            var painel = card.closest(".crit-painel");
            if (painel) { activateBloco(painel.id.replace("painel-", "")); }
            var toggle = card.querySelector(".crit-card-toggle");
            var corpo = card.querySelector(".crit-card-corpo");
            if (toggle && corpo) { setOpen(card, toggle, corpo, true); }
            card.classList.add("crit-card--target");
            setTimeout(function () {
                card.scrollIntoView({ block: "start", behavior: "smooth" });
            }, 80);
            setTimeout(function () {
                card.classList.remove("crit-card--target");
            }, 2400);
        }

        openFromHash();
        window.addEventListener("hashchange", openFromHash);
    }

    /* ── Init ────────────────────────────────────────────────── */
    document.addEventListener("DOMContentLoaded", function () {
        initCriterios();
        initScrollSpy();
        initSmoothScroll();
        initTocToggle();
        initMobileMenu();
        initCheckboxes();
        initCardAnimations();
        initReadingProgress();
        initJourneyActiveScroll();
        initKeyboardNav();
    });
})();
