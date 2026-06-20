function confirmerAnnulation() {
    return confirm("Voulez-vous vraiment annuler cette réservation ?");
}

function confirmerSuppression() {
    return confirm("Voulez-vous vraiment supprimer cet élément ?");
}

document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // DARK MODE
    // ==========================
    const themeToggle = document.getElementById("themeToggle");
    const html = document.documentElement;

    function updateThemeIcon() {
        if (!themeToggle) return;

        const icon = themeToggle.querySelector("i");

        if (html.getAttribute("data-theme") === "dark") {
            icon.className = "bi bi-sun-fill";
        } else {
            icon.className = "bi bi-moon-stars-fill";
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener("click", function () {

            const currentTheme = html.getAttribute("data-theme");

            if (currentTheme === "dark") {
                html.setAttribute("data-theme", "light");
                localStorage.setItem("transport_theme", "light");
            } else {
                html.setAttribute("data-theme", "dark");
                localStorage.setItem("transport_theme", "dark");
            }

            updateThemeIcon();
        });

        updateThemeIcon();
    }

    // ==========================
    // GREETING SYSTEM
    // ==========================
    const greetingElements = document.querySelectorAll("[data-dynamic-greeting]");

    if (greetingElements.length > 0) {

        const hour = new Date().getHours();

        let greeting = "Bonjour";

        if (hour >= 18) {
            greeting = "Bonsoir";
        } else if (hour >= 12) {
            greeting = "Bon après-midi";
        }

        greetingElements.forEach(el => {
            el.textContent = greeting;
        });
    }

});