# 🔒 Seguridad y Rendimiento - PyLink

## Características de Seguridad Implementadas

### 1. Headers de Seguridad HTTP ✅

Implementados en `pyenterprise/security.py`:

- **Content-Security-Policy (CSP)**: Protege contra ataques XSS
- **Strict-Transport-Security (HSTS)**: Fuerza conexiones HTTPS
- **X-Frame-Options**: Previene clickjacking
- **X-Content-Type-Options**: Previene MIME-sniffing
- **Referrer-Policy**: Controla información de referencia
- **Permissions-Policy**: Restringe APIs del navegador
- **Cross-Origin Policies**: Protección contra ataques cross-origin

### 2. Sistema de Cookies GDPR Compliant ✅

Implementado en `pyenterprise/components/cookie_banner.py`:

- **Banner de consentimiento**: Visible hasta que el usuario acepte
- **Categorías de cookies**:
  - 🔒 Esenciales (siempre activas)
  - 📊 Analíticas (opcionales)
  - 🎯 Marketing (opcionales)
- **Configuración personalizada**: El usuario puede elegir qué cookies aceptar
- **Persistencia**: Las preferencias se guardan en localStorage

### 3. Validación y Sanitización de Inputs ✅

Funciones en `pyenterprise/security.py`:

```python
# Sanitiza inputs para prevenir XSS
sanitize_input(text, input_type)

# Valida tokens CSRF
validate_csrf_token(token, session_token)

# Genera tokens seguros
generate_csrf_token()
```

### 4. Políticas de Privacidad ✅

Páginas implementadas:

- `/privacidad` - Política de Privacidad completa (RGPD/LOPD)
- `/cookies` - Política de Cookies detallada

Incluyen:

- Derechos del usuario (acceso, rectificación, supresión, etc.)
- Base legal del tratamiento
- Información sobre cookies utilizadas
- Datos de contacto del DPO

---

## Optimizaciones de Rendimiento

### 1. Resource Hints ✅

Implementado en `pyenterprise/performance.py`:

- **DNS Prefetch**: Resolución anticipada de dominios
- **Preconnect**: Conexión temprana a orígenes críticos
- **Preload**: Carga anticipada de recursos críticos

### 2. Caché Estratégica ✅

Configuración en `CACHE_CONFIG`:

- **Assets estáticos**: 1 año (immutable)
- **Imágenes**: 30 días
- **HTML**: 1 hora con revalidación

### 3. Compresión ✅

- **Gzip**: Nivel 6, archivos > 1KB
- **Brotli**: Calidad 6, archivos > 1KB

### 4. Lazy Loading ✅

Funciones implementadas:

```python
# Imagen con lazy loading
lazy_image(src, alt, **kwargs)

# Imagen responsive optimizada
responsive_image(src, alt, widths=[320, 640, 960, 1280])
```

### 5. Critical CSS Inline ✅

CSS crítico incluido inline en `CRITICAL_CSS` para renderizado rápido inicial.

### 6. Web Vitals Tracking ✅

Configurado para medir:

- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

---

## Configuración para Producción

### Paso 1: Variables de Entorno

Crear archivo `.env`:

```bash
# Seguridad
SECRET_KEY=tu_clave_secreta_muy_larga_y_aleatoria
CSRF_SECRET=otra_clave_secreta_para_csrf
SESSION_SECRET=clave_para_sesiones

# Base de datos (si aplica)
DATABASE_URL=postgresql://user:password@localhost/pylink

# APIs externas
GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX-X
FACEBOOK_PIXEL_ID=XXXXXXXXXXXXXXXXX

# CDN (opcional)
CDN_URL=https://cdn.pylink.com
CDN_ENABLED=true

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=contacto@pylink.com
SMTP_PASSWORD=tu_contraseña_smtp
```

### Paso 2: Configurar Servidor Web

#### Nginx (Recomendado)

```nginx
server {
    listen 443 ssl http2;
    server_name pylink.com www.pylink.com;

    # SSL Certificate
    ssl_certificate /etc/letsencrypt/live/pylink.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pylink.com/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;

    # Brotli (si está disponible)
    brotli on;
    brotli_comp_level 6;
    brotli_types text/plain text/css text/xml text/javascript application/javascript application/json;

    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|svg|css|js|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Reflex app
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name pylink.com www.pylink.com;
    return 301 https://$server_name$request_uri;
}
```

### Paso 3: Configurar SSL/TLS

#### Let's Encrypt (Gratis)

```bash
# Instalar Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d pylink.com -d www.pylink.com

# Renovación automática
sudo certbot renew --dry-run
```

### Paso 4: Rate Limiting

Configurar en Nginx:

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=contact_limit:10m rate=5r/h;

server {
    # ...
    
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        # ...
    }
    
    location /contact {
        limit_req zone=contact_limit burst=2 nodelay;
        # ...
    }
}
```

### Paso 5: Firewall y Protección DDoS

```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS

# Fail2ban para protección contra ataques de fuerza bruta
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
```

---

## Checklist de Seguridad Pre-Producción

- [ ] Certificado SSL/TLS configurado (Let's Encrypt o comercial)
- [ ] Headers de seguridad HTTP implementados
- [ ] CORS configurado correctamente
- [ ] Rate limiting activo
- [ ] Firewall configurado (UFW/iptables)
- [ ] Fail2ban instalado y configurado
- [ ] Variables de entorno en `.env` (NO en código)
- [ ] Logs de seguridad activados
- [ ] Backups automáticos configurados
- [ ] Política de privacidad y cookies publicada
- [ ] Banner de cookies funcionando
- [ ] Validación de inputs en todos los formularios
- [ ] CSRF tokens en formularios
- [ ] Sesiones seguras (httponly, secure, samesite)

## Checklist de Rendimiento Pre-Producción

- [ ] Compresión Gzip/Brotli activa
- [ ] Caché de assets estáticos configurada
- [ ] CDN configurado (opcional pero recomendado)
- [ ] Lazy loading en imágenes
- [ ] Critical CSS inline
- [ ] Resource hints implementados
- [ ] Minificación de JS/CSS
- [ ] Imágenes optimizadas (WebP, tamaños correctos)
- [ ] HTTP/2 o HTTP/3 activo
- [ ] Monitoreo de Web Vitals
- [ ] Google Analytics o alternativa configurada

---

## Monitoreo y Mantenimiento

### Herramientas Recomendadas

1. **Google PageSpeed Insights**: https://pagespeed.web.dev/
2. **SSL Labs Test**: https://www.ssllabs.com/ssltest/
3. **SecurityHeaders.com**: https://securityheaders.com/
4. **WebPageTest**: https://www.webpagetest.org/

### Actualizaciones Regulares

```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Verificar vulnerabilidades
pip-audit

# Revisar logs de seguridad
tail -f /var/log/security.log
```

---

## Contacto de Seguridad

Para reportar vulnerabilidades de seguridad:

- **Email**: security@pylink.com
- **PGP Key**: [Opcional - añadir clave pública]

Responderemos en un plazo máximo de 48 horas.

---

**Última actualización**: Octubre 2025
**Próxima revisión**: Enero 2026
