document.getElementById('navToggle').addEventListener('click', function() {
    document.getElementById('navLinks').classList.toggle('open');

    //Toggle to x icon
    this.classList.toggle('active');
});

