// Carrusel imágenes promocionales
let currentSlide = 0;
const slides = document.querySelectorAll(".slide");

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove("active"));
    slides[index].classList.add("active");
}

function moveSlide(step) {
    currentSlide = (currentSlide + step + slides.length) % slides.length;
    showSlide(currentSlide);
}

document.addEventListener("DOMContentLoaded", () => {
    showSlide(currentSlide);
});

// Slider productos nuevos
function scrollSlider(direction) {
    const slider = document.getElementById('slider-productos');
    const cardWidth = slider.querySelector('.producto-card').offsetWidth + 20;
    slider.scrollBy({
        left: cardWidth * direction,
        behavior: 'smooth'
    });
}

