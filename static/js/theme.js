/**
 * Site Theme Handler
 * Aplica el tema dinámico al sitio público
 */

(function() {
    'use strict';
    
    // Aplicar tema dinámico desde data attribute
    const themeColor = document.body.dataset.themeColor;
    
    if (themeColor) {
        document.documentElement.style.setProperty('--theme-color', themeColor);
        document.documentElement.style.setProperty('--theme-color-light', themeColor + 'ee');
        document.documentElement.style.setProperty('--theme-color-dark', themeColor + 'dd');
    }
    
})();
