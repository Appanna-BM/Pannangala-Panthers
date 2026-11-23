function showTab(tabName, button) {

    // Hide all tab contents
    const contents = document.querySelectorAll(".tab-content");

    contents.forEach(function(content) {
        content.classList.remove("active");
    });


    // Remove active from all buttons
    const buttons = document.querySelectorAll(".tab");

    buttons.forEach(function(tab) {
        tab.classList.remove("active");
    });


    // Show selected tab
    const targetContent = document.getElementById(tabName);
    if (targetContent) {
        targetContent.classList.add("active");
    }

    // Make clicked button active
    if (button) {
        button.classList.add("active");
    }
}

// Automatically activate tab if hash is present in URL (e.g., #results)
document.addEventListener("DOMContentLoaded", function() {
    if (window.location.hash) {
        const hash = window.location.hash.replace("#", "");
        const targetBtn = document.querySelector(`.detail-tabs .tab[onclick*="${hash}"]`);
        if (targetBtn) {
            showTab(hash, targetBtn);
        }
    }
});
