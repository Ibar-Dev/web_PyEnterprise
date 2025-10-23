/**
 * Sistema de Cookies con localStorage para versión estática
 * Funciona sin backend
 */

(function() {
    'use strict';
    
    const COOKIE_KEY = 'pylink_cookie_consent';
    const EXPIRY_DAYS = 365;
    
    // Verificar si ya hay consentimiento guardado
    function checkCookieConsent() {
        const consent = localStorage.getItem(COOKIE_KEY);
        if (consent) {
            const data = JSON.parse(consent);
            const now = new Date().getTime();
            
            // Verificar si no ha expirado
            if (data.expiry && now < data.expiry) {
                return true;
            } else {
                localStorage.removeItem(COOKIE_KEY);
            }
        }
        return false;
    }
    
    // Guardar consentimiento
    function saveCookieConsent(preferences) {
        const expiry = new Date().getTime() + (EXPIRY_DAYS * 24 * 60 * 60 * 1000);
        const data = {
            ...preferences,
            expiry: expiry,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem(COOKIE_KEY, JSON.stringify(data));
    }
    
    // Ocultar banner
    function hideBanner() {
        const banner = document.querySelector('[style*="position: fixed"][style*="bottom: 0"]');
        if (banner) {
            banner.style.display = 'none';
        }
    }
    
    // Inicializar cuando el DOM esté listo
    function init() {
        // Si ya hay consentimiento, ocultar banner
        if (checkCookieConsent()) {
            setTimeout(hideBanner, 100);
            return;
        }
        
        // Esperar a que el banner se renderice
        setTimeout(() => {
            attachEventListeners();
        }, 500);
    }
    
    // Adjuntar event listeners a los botones
    function attachEventListeners() {
        // Botón "Aceptar todas"
        const acceptAllBtns = Array.from(document.querySelectorAll('button')).filter(btn => 
            btn.textContent.includes('Aceptar todas') || btn.textContent.includes('Aceptar todos')
        );
        
        acceptAllBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                saveCookieConsent({
                    essential: true,
                    analytics: true,
                    marketing: true,
                    accepted: 'all'
                });
                hideBanner();
            });
        });
        
        // Botón "Rechazar"
        const rejectBtns = Array.from(document.querySelectorAll('button')).filter(btn => 
            btn.textContent.includes('Rechazar')
        );
        
        rejectBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                saveCookieConsent({
                    essential: true,
                    analytics: false,
                    marketing: false,
                    accepted: 'essential_only'
                });
                hideBanner();
            });
        });
        
        // Botón "Guardar preferencias"
        const savePrefBtns = Array.from(document.querySelectorAll('button')).filter(btn => 
            btn.textContent.includes('Guardar preferencias')
        );
        
        savePrefBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Obtener estado de los switches
                const switches = document.querySelectorAll('input[type="checkbox"], [role="switch"]');
                let analytics = false;
                let marketing = false;
                
                switches.forEach((sw, index) => {
                    if (index === 1) analytics = sw.checked || sw.getAttribute('data-state') === 'checked';
                    if (index === 2) marketing = sw.checked || sw.getAttribute('data-state') === 'checked';
                });
                
                saveCookieConsent({
                    essential: true,
                    analytics: analytics,
                    marketing: marketing,
                    accepted: 'custom'
                });
                hideBanner();
            });
        });
    }
    
    // Ejecutar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // También ejecutar en cada cambio de ruta (para SPAs)
    window.addEventListener('popstate', init);
    
})();

// Exportar funciones útiles globalmente
window.PyLinkCookies = {
    hasConsent: function() {
        const consent = localStorage.getItem('pylink_cookie_consent');
        return consent !== null;
    },
    getConsent: function() {
        const consent = localStorage.getItem('pylink_cookie_consent');
        return consent ? JSON.parse(consent) : null;
    },
    clearConsent: function() {
        localStorage.removeItem('pylink_cookie_consent');
        window.location.reload();
    }
};
