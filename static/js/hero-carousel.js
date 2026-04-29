// Hero Carousel for Mobile
(function () {
    const container = document.getElementById('hero-carousel-container');
    if (!container || window.innerWidth >= 768) return; // Only run on mobile

    const slides = document.querySelectorAll('.hero-slide');
    const prevBtn = document.getElementById('hero-prev');
    const nextBtn = document.getElementById('hero-next');
    const indicatorsContainer = document.getElementById('hero-indicators');

    if (!slides.length) return;

    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoplayInterval;

    // Create indicator dots
    slides.forEach((_, index) => {
        const dot = document.createElement('button');
        dot.className = `w-2.5 h-2.5 rounded-full transition-all duration-300 ${index === 0 ? 'bg-white' : 'bg-white/50'}`;
        dot.addEventListener('click', () => goToSlide(index));
        dot.setAttribute('aria-label', `Ir a la imagen ${index + 1}`);
        indicatorsContainer.appendChild(dot);
    });

    const dots = indicatorsContainer.querySelectorAll('button');

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.opacity = i === index ? '1' : '0';
            slide.style.zIndex = i === index ? '10' : '0';
        });

        dots.forEach((dot, i) => {
            if (i === index) {
                dot.classList.remove('bg-white/50');
                dot.classList.add('bg-white');
            } else {
                dot.classList.remove('bg-white');
                dot.classList.add('bg-white/50');
            }
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        showSlide(currentIndex);
        resetAutoplay();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        showSlide(currentIndex);
        resetAutoplay();
    }

    function goToSlide(index) {
        currentIndex = index;
        showSlide(currentIndex);
        resetAutoplay();
    }

    function startAutoplay() {
        autoplayInterval = setInterval(nextSlide, 5000);
    }

    function resetAutoplay() {
        clearInterval(autoplayInterval);
        startAutoplay();
    }

    // Event listeners
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);

    // Initial state
    showSlide(0);
    if (totalSlides > 1) startAutoplay();

    // Pause on hover
    const carouselWrapper = container.querySelector('.relative');
    if (carouselWrapper) {
        carouselWrapper.addEventListener('mouseenter', () => clearInterval(autoplayInterval));
        carouselWrapper.addEventListener('mouseleave', startAutoplay);
    }
})();
