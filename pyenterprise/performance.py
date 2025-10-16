"""
Optimizaciones de Rendimiento para PyLink
Caché, compresión, lazy loading, etc.
"""

import reflex as rx


# Configuración de caché
CACHE_CONFIG = {
    # Caché de assets estáticos
    "static_assets": {
        "max_age": 31536000,  # 1 año
        "immutable": True,
        "types": [".js", ".css", ".woff", ".woff2", ".ttf", ".eot"],
    },
    
    # Caché de imágenes
    "images": {
        "max_age": 2592000,  # 30 días
        "types": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico"],
    },
    
    # Caché de páginas HTML
    "html": {
        "max_age": 3600,  # 1 hora
        "must_revalidate": True,
    },
}


# Configuración de compresión
COMPRESSION_CONFIG = {
    "gzip": {
        "enabled": True,
        "level": 6,  # Nivel de compresión (1-9)
        "min_size": 1024,  # Comprimir solo archivos > 1KB
    },
    "brotli": {
        "enabled": True,
        "quality": 6,  # Calidad (0-11)
        "min_size": 1024,
    },
}


# Configuración de lazy loading para imágenes
def lazy_image(src: str, alt: str, **kwargs) -> rx.Component:
    """
    Imagen con lazy loading optimizado.
    
    Args:
        src: URL de la imagen
        alt: Texto alternativo
        **kwargs: Propiedades adicionales
    
    Returns:
        Componente imagen optimizada
    """
    return rx.image(
        src=src,
        alt=alt,
        loading="lazy",  # Lazy loading nativo
        decoding="async",  # Decodificación asíncrona
        **kwargs,
    )


# Preload de recursos críticos
PRELOAD_RESOURCES = [
    {"href": "/fonts/inter-var.woff2", "as": "font", "type": "font/woff2", "crossorigin": "anonymous"},
    {"href": "/css/critical.css", "as": "style"},
]


# DNS Prefetch para recursos externos
DNS_PREFETCH = [
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
    "https://www.google-analytics.com",
]


# Preconnect para APIs críticas
PRECONNECT = [
    "https://api.pylink.com",
]


def add_performance_headers():
    """
    Genera headers de rendimiento optimizados.
    
    Returns:
        Dict de headers
    """
    headers = {}
    
    # Early Hints (103)
    headers["Link"] = ", ".join([
        f'<{resource["href"]}>; rel=preload; as={resource["as"]}'
        for resource in PRELOAD_RESOURCES
    ])
    
    # Cache-Control
    headers["Cache-Control"] = "public, max-age=3600, must-revalidate"
    
    # ETag para validación de caché
    headers["ETag"] = 'W/"hash-version-123"'
    
    return headers


def optimize_image_url(url: str, width: int = None, quality: int = 85) -> str:
    """
    Optimiza URL de imagen con parámetros de tamaño y calidad.
    
    Args:
        url: URL original
        width: Ancho deseado
        quality: Calidad (1-100)
    
    Returns:
        URL optimizada
    """
    # Si usas un CDN como Cloudinary, Imgix, etc.
    # Ejemplo con parámetros de query
    params = []
    if width:
        params.append(f"w={width}")
    if quality:
        params.append(f"q={quality}")
    
    if params:
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}{'&'.join(params)}"
    
    return url


# Componente de imagen responsive optimizada
def responsive_image(
    src: str,
    alt: str,
    widths: list = [320, 640, 960, 1280],
    **kwargs
) -> rx.Component:
    """
    Imagen responsive con srcset optimizado.
    
    Args:
        src: URL base de la imagen
        alt: Texto alternativo
        widths: Lista de anchos para srcset
        **kwargs: Props adicionales
    
    Returns:
        Componente imagen responsive
    """
    # Generar srcset
    srcset = ", ".join([
        f"{optimize_image_url(src, width=w)} {w}w"
        for w in widths
    ])
    
    return rx.image(
        src=optimize_image_url(src),
        alt=alt,
        loading="lazy",
        decoding="async",
        srcset=srcset,
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
        **kwargs,
    )


# Bundle splitting - Configuración para Reflex
BUNDLE_CONFIG = {
    "chunk_size_warning_limit": 500000,  # 500KB
    "vendor_chunk": True,  # Separar dependencias de vendors
    "common_chunk": True,  # Extraer código común
}


# Configuración de Service Worker para PWA
SERVICE_WORKER_CONFIG = {
    "enabled": False,  # Activar cuando esté listo
    "cache_name": "pylink-v1",
    "cache_files": [
        "/",
        "/index.html",
        "/css/main.css",
        "/js/main.js",
        "/manifest.json",
    ],
    "offline_page": "/offline.html",
}


# Critical CSS - Estilos críticos inline
CRITICAL_CSS = """
/* Critical CSS - Above the fold */
body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background: #1a1a2e;
    color: white;
}

.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: rgba(26, 26, 46, 0.95);
    backdrop-filter: blur(10px);
}

.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
"""


# Métricas Web Vitals
WEB_VITALS_CONFIG = {
    "track": True,
    "report_url": "/api/vitals",
    "thresholds": {
        "LCP": 2500,  # Largest Contentful Paint (ms)
        "FID": 100,   # First Input Delay (ms)
        "CLS": 0.1,   # Cumulative Layout Shift
    },
}


# Script para medir Web Vitals
WEB_VITALS_SCRIPT = """
<script type="module">
import {onCLS, onFID, onLCP} from 'https://unpkg.com/web-vitals@3/dist/web-vitals.js?module';

function sendToAnalytics(metric) {
    const body = JSON.stringify({
        name: metric.name,
        value: metric.value,
        id: metric.id,
    });
    
    // Enviar a tu endpoint
    if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/vitals', body);
    } else {
        fetch('/api/vitals', {
            method: 'POST',
            body,
            headers: {'Content-Type': 'application/json'},
            keepalive: true
        });
    }
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
</script>
"""


# Resource Hints Component
def resource_hints() -> rx.Component:
    """
    Añade resource hints para mejorar rendimiento.
    
    Returns:
        Componente con hints
    """
    return rx.html(
        f"""
        <!-- DNS Prefetch -->
        {''.join([f'<link rel="dns-prefetch" href="{url}">' for url in DNS_PREFETCH])}
        
        <!-- Preconnect -->
        {''.join([f'<link rel="preconnect" href="{url}">' for url in PRECONNECT])}
        
        <!-- Preload Critical Resources -->
        {''.join([
            f'<link rel="preload" href="{r["href"]}" as="{r["as"]}"' + (f' type="{r["type"]}"' if "type" in r else "") + '>'
            for r in PRELOAD_RESOURCES
        ])}
        
        <!-- Critical CSS Inline -->
        <style>{CRITICAL_CSS}</style>
        """
    )


# Función para minificar HTML
def minify_html(html: str) -> str:
    """
    Minifica HTML eliminando espacios innecesarios.
    
    Args:
        html: HTML original
    
    Returns:
        HTML minificado
    """
    import re
    
    # Remover comentarios HTML
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # Remover espacios múltiples
    html = re.sub(r'\s+', ' ', html)
    
    # Remover espacios entre tags
    html = re.sub(r'>\s+<', '><', html)
    
    return html.strip()


# Configuración de CDN
CDN_CONFIG = {
    "enabled": False,  # Activar en producción
    "base_url": "https://cdn.pylink.com",
    "assets_prefix": "/static",
}


def get_asset_url(path: str) -> str:
    """
    Obtiene URL de asset (local o CDN).
    
    Args:
        path: Ruta del asset
    
    Returns:
        URL completa
    """
    if CDN_CONFIG["enabled"]:
        return f"{CDN_CONFIG['base_url']}{CDN_CONFIG['assets_prefix']}{path}"
    return path
