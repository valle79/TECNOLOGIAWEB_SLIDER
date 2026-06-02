// Hero Carousel for Mobile - Optimizado PRO
(function () {
    const container = document.getElementById('hero-carousel-container');

    // Validación inicial
    if (!container || window.innerWidth >= 768) return;

    const slides = container.querySelectorAll('.hero-slide');
    const prevBtn = document.getElementById('hero-prev');
    const nextBtn = document.getElementById('hero-next');
    const indicatorsContainer = document.getElementById('hero-indicators');

    if (!slides.length || !indicatorsContainer) return;

    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoplayInterval = null;
    let isAnimating = false;

    // Crear indicadores
    slides.forEach((_, index) => {
        const dot = document.createElement('button');
        dot.className = `w-2.5 h-2.5 rounded-full transition-all duration-300 ${index === 0 ? 'bg-white' : 'bg-white/50'}`;
        dot.setAttribute('aria-label', `Ir a la imagen ${index + 1}`);
        dot.addEventListener('click', () => goToSlide(index));
        indicatorsContainer.appendChild(dot);
    });

    const dots = indicatorsContainer.querySelectorAll('button');

    function showSlide(index) {
        if (isAnimating) return;
        isAnimating = true;

        slides.forEach((slide, i) => {
            slide.style.transition = 'opacity 0.5s ease';
            slide.style.opacity = i === index ? '1' : '0';
            slide.style.zIndex = i === index ? '10' : '0';
        });

        dots.forEach((dot, i) => {
            dot.classList.toggle('bg-white', i === index);
            dot.classList.toggle('bg-white/50', i !== index);
        });

        setTimeout(() => {
            isAnimating = false;
        }, 500);
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
        if (autoplayInterval) return;
        autoplayInterval = setInterval(nextSlide, 5000);
    }

    function stopAutoplay() {
        clearInterval(autoplayInterval);
        autoplayInterval = null;
    }

    function resetAutoplay() {
        stopAutoplay();
        startAutoplay();
    }

    // Eventos botones (con validación)
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);

    // Hover (por si usan tablet)
    const wrapper = container.querySelector('.relative');
    if (wrapper) {
        wrapper.addEventListener('mouseenter', stopAutoplay);
        wrapper.addEventListener('mouseleave', startAutoplay);
    }

    // 👉 Swipe para mobile (MUY IMPORTANTE)
    let startX = 0;

    container.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
    });

    container.addEventListener('touchend', (e) => {
        const endX = e.changedTouches[0].clientX;
        const diff = startX - endX;

        if (Math.abs(diff) > 50) {
            diff > 0 ? nextSlide() : prevSlide();
        }
    });

    // 👉 Reiniciar si cambia tamaño de pantalla
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 768) {
            stopAutoplay();
        }
    });

    // Inicializar
    showSlide(0);
    if (totalSlides > 1) startAutoplay();
})();