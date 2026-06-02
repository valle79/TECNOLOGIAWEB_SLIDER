let hasShownPreviewToast = false;

function applyTheme(color) {
    document.documentElement.style.setProperty('--theme-color', color);
    document.documentElement.style.setProperty('--theme-color-dark', color + 'dd');
    document.documentElement.style.setProperty('--theme-color-darker', color + 'bb');
}

function previewThemeColor(input) {
    const color = input.value;

    if (input.dataset.lastColor === color) return;
    input.dataset.lastColor = color;

    const textInput = input.parentElement.querySelector('[data-color-preview]');
    if (textInput) {
        textInput.value = color;
    }

    applyTheme(color);

    if (typeof AdminAlerts !== 'undefined' && !hasShownPreviewToast) {
        AdminAlerts.toast('Vista previa activada', 'info');
        hasShownPreviewToast = true;
    }
}

function resetColor(inputId, defaultColor) {
    const colorInput = document.getElementById(inputId);
    if (!colorInput) return;

    const textInput = colorInput.parentElement.querySelector('[data-color-preview]');

    colorInput.value = defaultColor;
    colorInput.dataset.lastColor = defaultColor;

    if (textInput) {
        textInput.value = defaultColor;
    }

    applyTheme(defaultColor);

    if (typeof AdminAlerts !== 'undefined') {
        AdminAlerts.toast('Color restablecido', 'success');
    }
}

window.previewThemeColor = previewThemeColor;
window.resetColor = resetColor;