/**
 * Team Carousel JavaScript
 * Carrusel circular animado para la sección de equipo
 * Soporta múltiples instancias en la misma página
 */

(function() {
    'use strict';

    // Team members data
    const teamMembers = [
        {
            name: "Luis Valle",
            role: "Product Manager",
            quote: "Nuestra pasión es crear vinos excepcionales que cuenten la historia de nuestros valles. Cada botella es una obra de arte que refleja años de dedicación y amor por la viticultura.",
            image: ""
        },
        {
            name: "Marta Clermont",
            role: "Design Team Lead",
            quote: "El diseño de cada etiqueta y presentación refleja la elegancia y sofisticación de nuestros vinos. Buscamos crear una experiencia visual memorable que complemente el sabor excepcional.",
            image: ""
        },
        {
            name: "Alice Melbourne",
            role: "Human Resources",
            quote: "Nuestro equipo es el corazón de San Roque. Cultivamos un ambiente de trabajo donde la pasión por el vino y el respeto mutuo impulsan la excelencia en cada proceso.",
            image: ""
        },
        {
            name: "John Doe",
            role: "Chief Guy",
            quote: "Lideramos con visión y compromiso hacia la sostenibilidad. Cada decisión está guiada por el respeto a la tierra, nuestros colaboradores y la tradición vinícola peruana.",
            image: ""
        }
    ];

    // Calculate gap based on container width
    function calculateGap(width) {
        const minWidth = 1024;
        const maxWidth = 1456;
        const minGap = 60;
        const maxGap = 86;

        if (width <= minWidth) return minGap;
        if (width >= maxWidth) {
            return Math.max(minGap, maxGap + 0.06018 * (width - maxWidth));
        }
        return minGap + (maxGap - minGap) * ((width - minWidth) / (maxWidth - minWidth));
    }

    // Initialize a single carousel instance
    function initCarousel(containerId) {
        let activeIndex = 0;
        let containerWidth = 1200;
        let autoplayInterval;

        // Elements with unique IDs
        const imagesContainer = document.getElementById(containerId.replace('teamCarousel', 'teamImagesContainer'));
        const teamName = document.getElementById(containerId.replace('teamCarousel', 'teamName'));
        const teamRole = document.getElementById(containerId.replace('teamCarousel', 'teamRole'));
        const teamQuote = document.getElementById(containerId.replace('teamCarousel', 'teamQuote'));
        const prevBtn = document.getElementById(containerId.replace('teamCarousel', 'teamPrevBtn'));
        const nextBtn = document.getElementById(containerId.replace('teamCarousel', 'teamNextBtn'));

        if (!imagesContainer) return;

        const images = Array.from(imagesContainer.querySelectorAll('.team-member-image'));

        // Get image transform style
        function getImageStyle(index) {
            const gap = calculateGap(containerWidth);
            const maxStickUp = gap * 0.8;

            const isActive = index === activeIndex;
            const isLeft = (activeIndex - 1 + teamMembers.length) % teamMembers.length === index;
            const isRight = (activeIndex + 1) % teamMembers.length === index;

            if (isActive) {
                return {
                    zIndex: '3',
                    opacity: '1',
                    pointerEvents: 'auto',
                    transform: 'translateX(0px) translateY(0px) scale(1) rotateY(0deg)'
                };
            }

            if (isLeft) {
                return {
                    zIndex: '2',
                    opacity: '1',
                    pointerEvents: 'auto',
                    transform: `translateX(-${gap}px) translateY(-${maxStickUp}px) scale(0.85) rotateY(15deg)`
                };
            }

            if (isRight) {
                return {
                    zIndex: '2',
                    opacity: '1',
                    pointerEvents: 'auto',
                    transform: `translateX(${gap}px) translateY(-${maxStickUp}px) scale(0.85) rotateY(-15deg)`
                };
            }

            // Hide other images
            return {
                zIndex: '1',
                opacity: '0',
                pointerEvents: 'none'
            };
        }

        // Update images positions
        function updateImages() {
            images.forEach((img, index) => {
                const style = getImageStyle(index);
                Object.assign(img.style, style);
            });
        }

        // Animate quote words
        function animateQuote(text) {
            const words = text.split(' ');
            teamQuote.innerHTML = '';
            
            words.forEach((word, index) => {
                const span = document.createElement('span');
                span.className = 'word';
                span.textContent = word;
                span.style.animationDelay = `${index * 0.025}s`;
                teamQuote.appendChild(span);
                
                // Add space after each word (except last)
                if (index < words.length - 1) {
                    teamQuote.appendChild(document.createTextNode(' '));
                }
            });
        }

        // Update content
        function updateContent() {
            const member = teamMembers[activeIndex];
            
            // Fade out
            teamName.style.opacity = '0';
            teamRole.style.opacity = '0';
            teamQuote.style.opacity = '0';

            setTimeout(() => {
                teamName.textContent = member.name;
                teamRole.textContent = member.role;
                animateQuote(member.quote);

                // Fade in
                teamName.style.opacity = '1';
                teamRole.style.opacity = '1';
                teamQuote.style.opacity = '1';
            }, 150);
        }

        // Navigate to index
        function goToIndex(index) {
            activeIndex = (index + teamMembers.length) % teamMembers.length;
            updateImages();
            updateContent();
            resetAutoplay();
        }

        // Navigation handlers
        function handleNext() {
            goToIndex(activeIndex + 1);
        }

        function handlePrev() {
            goToIndex(activeIndex - 1);
        }

        // Autoplay
        function startAutoplay() {
            autoplayInterval = setInterval(() => {
                handleNext();
            }, 5000);
        }

        function stopAutoplay() {
            if (autoplayInterval) {
                clearInterval(autoplayInterval);
            }
        }

        function resetAutoplay() {
            stopAutoplay();
            startAutoplay();
        }

        // Handle resize
        function handleResize() {
            if (imagesContainer) {
                containerWidth = imagesContainer.offsetWidth;
                updateImages();
            }
        }

        // Keyboard navigation
        function handleKeyboard(e) {
            if (e.key === 'ArrowLeft') handlePrev();
            if (e.key === 'ArrowRight') handleNext();
        }

        // Event listeners
        if (prevBtn) prevBtn.addEventListener('click', handlePrev);
        if (nextBtn) nextBtn.addEventListener('click', handleNext);
        
        window.addEventListener('resize', handleResize);
        window.addEventListener('keydown', handleKeyboard);

        // Image click
        images.forEach((img, index) => {
            img.addEventListener('click', () => {
                if (index !== activeIndex) {
                    goToIndex(index);
                }
            });
        });

        // Initialize
        handleResize();
        updateImages();
        animateQuote(teamMembers[0].quote);
        startAutoplay();

        // Cleanup on page unload
        window.addEventListener('beforeunload', stopAutoplay);
    }

    // Initialize all carousels on the page
    function initAllCarousels() {
        // Find all carousel containers
        const carousels = document.querySelectorAll('[id^="teamCarousel"]');
        carousels.forEach(carousel => {
            initCarousel(carousel.id);
        });
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAllCarousels);
    } else {
        initAllCarousels();
    }

})();
