document.addEventListener('DOMContentLoaded', () => {
    
    // === 1. SEARCH LOGIC ===
    const searchInput = document.getElementById('toolSearch');
    const toolCards = document.querySelectorAll('.tool-card');
    const noResultsMessage = document.getElementById('noResults');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchValue = e.target.value.toLowerCase();
            let visibleCount = 0;

            toolCards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const tag = card.querySelector('.category-tag').textContent.toLowerCase();

                if (title.startsWith(searchValue) || tag.startsWith(searchValue) || title.includes(searchValue)) {
                    card.style.display = "block"; 
                    visibleCount++;
                } else {
                    card.style.display = "none";
                }
            });

            if (noResultsMessage) {
                noResultsMessage.style.display = (visibleCount === 0 && searchValue !== "") ? "block" : "none";
            }
        });
    }

    // === 2. HAMBURGER MENU LOGIC ===
    const menuToggle = document.getElementById('menuToggle');
    const menuClose = document.getElementById('menuClose');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.add('active');
            console.log("Menu Opened"); // For debugging
        });
    }

    if (menuClose && navLinks) {
        menuClose.addEventListener('click', () => {
            navLinks.classList.remove('active');
            console.log("Menu Closed"); // For debugging
        });
    }

    // === 3. CONTACT FORM ===
    const contactForm = document.getElementById("contactForm");
    if (contactForm) {
        contactForm.addEventListener("submit", function (e) {
            e.preventDefault();
            alert("Contact system is under development. Email integration will be available soon.");
            contactForm.reset();
        });
    }

    // === 4. REQUEST TOOL FORM ===
    const requestForm = document.getElementById("requestToolForm");
    if (requestForm) {
        requestForm.addEventListener("submit", function (e) {
            e.preventDefault();
            alert("Tool request system is under development. Full submission system will be available soon.");
            requestForm.reset();
        });
    }
});