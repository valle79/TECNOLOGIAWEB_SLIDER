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
totalSlidesEl.textContent = totalSlides;

// Crear indicadores (dots)
slides.forEach((_, index) => {
    const dot = document.createElement("button");
    dot.classList.add("w-3", "h-3", "rounded-full", "bg-white/50");
    dot.addEventListener("click", () => goToSlide(index));
    indicatorsContainer.appendChild(dot);
});

// Obtener dots
const dots = indicatorsContainer.querySelectorAll("button");

// Mostrar slide
function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.remove("opacity-100", "z-10");
        slide.classList.add("opacity-0", "z-0");

        dots[i].classList.remove("bg-white");
        dots[i].classList.add("bg-white/50");
    });

    slides[index].classList.remove("opacity-0", "z-0");
    slides[index].classList.add("opacity-100", "z-10");

    dots[index].classList.remove("bg-white/50");
    dots[index].classList.add("bg-white");

    currentSlideEl.textContent = index + 1;
}

// Navegación
function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    showSlide(currentIndex);
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    showSlide(currentIndex);
}

function goToSlide(index) {
    currentIndex = index;
    showSlide(currentIndex);
}

// Botones
nextBtn.addEventListener("click", nextSlide);
prevBtn.addEventListener("click", prevSlide);

// Autoplay
function startAutoplay() {
    interval = setInterval(nextSlide, 4000);
}

function stopAutoplay() {
    clearInterval(interval);
}

// Pausa en hover
const slider = document.getElementById("slider-container");

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

// Tema oscuro/claro
let darkMode = true;

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

// Navbar mobile toggle
const menuBtn = document.getElementById("menu-btn");
const mobileMenu = document.getElementById("mobile-menu");

menuBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("hidden");
});

// Inicializar
showSlide(currentIndex);
startAutoplay();