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
    document.getElementById(tabName).classList.add("active");


    // Make clicked button active
    button.classList.add("active");
}