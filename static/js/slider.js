let currentIndex = 0;
const slides = document.querySelectorAll(".slide");
const totalSlides = slides.length;

const prevBtn = document.querySelector(".prev-button");
const nextBtn = document.querySelector(".next-button");
const indicatorsContainer = document.querySelector(".indicators-container");
const currentSlideEl = document.querySelector(".current-slide");
const totalSlidesEl = document.querySelector(".total-slides");
const themeToggle = document.getElementById("theme-toggle");

let interval;

// Mostrar total
if (totalSlidesEl) totalSlidesEl.textContent = totalSlides;

// Crear indicadores (dots)
if (indicatorsContainer) {
    slides.forEach((_, index) => {
        const dot = document.createElement("button");
        dot.classList.add("w-3", "h-3", "rounded-full", "bg-white/50");
        dot.addEventListener("click", () => goToSlide(index));
        indicatorsContainer.appendChild(dot);
    });
}

// Obtener dots
const dots = indicatorsContainer ? indicatorsContainer.querySelectorAll("button") : [];

// Mostrar slide
function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.remove("opacity-100", "z-10");
        slide.classList.add("opacity-0", "z-0");

        if (dots[i]) {
            dots[i].classList.remove("bg-white");
            dots[i].classList.add("bg-white/50");
        }
    });

    if (slides[index]) {
        slides[index].classList.remove("opacity-0", "z-0");
        slides[index].classList.add("opacity-100", "z-10");
    }

    if (dots[index]) {
        dots[index].classList.remove("bg-white/50");
        dots[index].classList.add("bg-white");
    }

    if (currentSlideEl) currentSlideEl.textContent = index + 1;
}

// Navegación
function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    showSlide(currentIndex);
    if (interval) restartAutoplay();
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    showSlide(currentIndex);
    if (interval) restartAutoplay();
}

function goToSlide(index) {
    currentIndex = index;
    showSlide(currentIndex);
    if (interval) restartAutoplay();
}

// Botones
if (nextBtn) nextBtn.addEventListener("click", nextSlide);
if (prevBtn) prevBtn.addEventListener("click", prevSlide);

// Autoplay
function startAutoplay() {
    if (totalSlides > 1) {
        interval = setInterval(nextSlide, 5000);
    }
}

function stopAutoplay() {
    clearInterval(interval);
}

function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
}

// Pausa en hover
const slider = document.getElementById("slider-container");
if (slider) {
    slider.addEventListener("mouseenter", stopAutoplay);
    slider.addEventListener("mouseleave", startAutoplay);
    
    // Swipe (móvil)
    let startX = 0;

    slider.addEventListener("touchstart", (e) => {
        startX = e.touches[0].clientX;
    });

    slider.addEventListener("touchend", (e) => {
        let endX = e.changedTouches[0].clientX;

        if (startX - endX > 50) {
            nextSlide();
        } else if (endX - startX > 50) {
            prevSlide();
        }
    });
}

// Tema oscuro/claro
let darkMode = true;

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        darkMode = !darkMode;

        if (darkMode) {
            document.body.classList.remove("bg-white");
            document.body.classList.add("bg-black");
        } else {
            document.body.classList.remove("bg-black");
            document.body.classList.add("bg-white");
        }
    });
}

// Navbar mobile toggle - REMOVEIDO PARA EVITAR CONFLICTO
// Este código está en main.js dentro del DOMContentLoaded
// No modificar aquí para evitar conflictos

// Iniciar autoplay cuando hay slides
if (slides.length > 0) {
    showSlide(0);
    startAutoplay();
}

// Inicializar
showSlide(currentIndex);
startAutoplay();