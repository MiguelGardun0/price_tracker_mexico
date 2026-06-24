# CLAUDE.md — Price Tracker MX (rastreador de precios con alertas predictivas)

> Este archivo da contexto a Claude Code sobre el proyecto. Resume la idea, la
> arquitectura, las decisiones técnicas ya tomadas y el estado actual. El autor
> es un estudiante en México que apunta a una carrera de data engineering / ML
> engineering, y está construyendo esto **para aprender**: prefiere recibir
> instrucciones, explicaciones del *porqué* y guía paso a paso en lugar de código
> entregado ya resuelto. Respeta ese estilo de trabajo.

---

## 1. Qué es el proyecto

Una web app que rastrea precios de productos en marketplaces mexicanos, guarda el
**historial** de precios a lo largo del tiempo, predice cuándo bajará un precio y
envía alertas al usuario. El diferenciador frente a lo existente (CamelCamelCamel
solo cubre Amazon US) es enfocarse en el mercado mexicano: **MercadoLibre,
Amazon MX, Walmart MX y Liverpool**, que es lo que la gente usa aquí. Competencia
local casi nula.

### Objetivo doble
1. **Aprender** ingeniería de datos y ML de forma práctica (pipeline ETL real,
   modelado de series de tiempo, infraestructura, deploy).
2. **Monetizar** vía suscripciones (freemium) + links de afiliados.

---

## 2. Arquitectura objetivo (visión completa)

El sistema se organiza en 4 capas:

**Capa de ingestión**
- Scrapers para MercadoLibre / Amazon MX (luego Walmart MX, Liverpool).
- Scheduler (cron al inicio → Airflow en producción) que dispara el scraping
  cada ~6 horas.
- Salida: datos crudos (precio, stock, fecha, URL).

**Capa de almacenamiento**
- PostgreSQL: historial de precios (fuente de verdad).
- Redis: cache de precios actuales (fase posterior).
- S3 / object storage: snapshots históricos (fase posterior).

**Capa de ML**
- Prophet / ARIMA: predicción de precio a 7–30 días.
- Detección de anomalías: identificar bajadas inesperadas (>10%).
- "Buy score" 0–100: ¿conviene comprar hoy? (basado en percentil histórico).

**Capa de entrega**
- Alertas por email (SendGrid) y WhatsApp (Twilio).
- API REST (FastAPI recomendado sobre Django para este caso).
- Dashboard web en Next.js.
- Links de afiliados (Amazon Associates MX) para monetizar.

---

## 3. Stack técnico

| Componente        | Tecnología                          | Notas                                    |
|-------------------|-------------------------------------|------------------------------------------|
| Lenguaje          | Python 3.10+                        | Backend, scrapers, ML                    |
| Scraping          | `requests` + `beautifulsoup4`       | Selenium/Playwright solo si hace falta JS|
| Base de datos     | PostgreSQL (en Docker)              | Driver: `psycopg2-binary`; luego SQLAlchemy |
| Orquestación      | cron (MVP) → Airflow (prod)         | Airflow se despliega con docker-compose  |
| Modelo predictivo | Prophet, scikit-learn, NumPy        | Series de tiempo                         |
| Cache             | Redis                               | Fase posterior                           |
| Frontend          | Next.js                             | Vercel para deploy                       |
| Auth              | NextAuth                            | Fase 3                                    |
| Pagos             | Stripe o MercadoPago                | Fase 3                                    |
| Alertas           | SendGrid (email), Twilio (WhatsApp) | Fase 2 y 4                               |
| Infra local       | Docker + Docker Compose             | Decisión confirmada (ver sección 6)      |
| Deploy            | Railway/Render (backend) + Vercel   | Costo inicial < $20/mes                  |

---

## 4. Roadmap por fases

### Fase 1 — MVP: scraper + base de datos (semanas 1–2) ← FASE ACTUAL
- Scraper de MercadoLibre con requests + BeautifulSoup.
- Schema PostgreSQL: productos, precios, historial.
- Script ETL básico (extract → transform → load).
- Scheduling cada 6 h (cron local / Airflow simple).

### Fase 2 — Modelo predictivo + alertas (semanas 3–4)
- Prophet para predecir precio 7–14 días.
- Detección de anomalías (bajadas >10%).
- Alertas por email con SendGrid.
- "Buy score" 0–100 por percentil histórico.

### Fase 3 — Web pública + suscripciones (semanas 5–6)
- Frontend Next.js: búsqueda + gráficas de historial.
- Autenticación (NextAuth).
- Pagos (Stripe / MercadoPago).
- Deploy: Railway/Render + Vercel.

### Fase 4 — Escalar y monetizar (semanas 7–8)
- Ampliar a Amazon MX, Walmart MX, Liverpool.
- Alertas por WhatsApp (Twilio).
- Links de afiliados (Amazon Associates MX).
- SEO técnico: páginas de producto indexables.

---

## 5. Modelo de negocio

**Proyección de ingresos (escenario realista):**
- Mes 2: $0 (lanzamiento)
- Mes 4: ~$120/mes (~30 usuarios Pro)
- Mes 6: ~$500/mes (afiliados + suscripciones)
- Mes 12: $1,500+/mes (si escala bien)

**Tiers de precio:**
- **Free** — $0: 5 productos, alertas semanales.
- **Pro** — $79 MXN/mes: 50 productos, alertas instantáneas, predicciones.
- **Business** — $299 MXN/mes: ilimitado + API + reportes.

---

## 6. Decisiones técnicas ya tomadas (y su porqué)

Estas decisiones ya se discutieron y se cerraron. No re-litigar sin razón nueva.

1. **Docker para PostgreSQL en lugar de instalación local.**
   *Por qué:* reproducibilidad (la config vive en un `docker-compose.yml` versionable
   en Git), aislamiento (romper y recrear en segundos sin ensuciar el sistema),
   es como se trabaja en producción, y Airflow (Fase 4) se despliega con
   docker-compose de todos modos. Único costo: curva de aprendizaje inicial de
   Docker, que se paga una sola vez.

2. **CUIDADO con la persistencia en Docker.** Los contenedores son efímeros: si se
   destruye el contenedor sin un **volumen** configurado, los datos se pierden.
   El historial de precios ES el valor del proyecto, así que el volumen para
   persistencia es obligatorio y es la pieza que la gente olvida.

3. **Dos tablas, no una.** Separar datos estables (`productos`: id, título, URL,
   marketplace, fecha de alta) de datos que cambian (`precios`/`historial_precios`:
   timestamp de observación, precio, stock). Cada scraping inserta una fila nueva
   en `precios`. NUNCA sobrescribir el precio — se perdería el historial, que es
   lo que alimenta el modelo de la Fase 2. Relación vía primary key (en productos)
   y foreign key (en precios).

4. **`NUMERIC`/`DECIMAL` para el precio, NUNCA float.** Los tipos de punto flotante
   introducen errores de redondeo en dinero.

5. **Idempotencia diferenciada.** Correr el script N veces NO debe duplicar
   productos (usar `ON CONFLICT DO NOTHING` en la tabla productos), pero SÍ debe
   insertar una fila nueva en precios cada corrida (cada corrida es una observación
   temporal distinta).

6. **Empezar con scraping, no con la API oficial.** MercadoLibre tiene API oficial
   para desarrolladores (alternativa robusta si el scraping se complica), pero el
   objetivo es aprender scraping. Tenerla en el radar.

7. **FastAPI sobre Django** para la API (más pythónico y ligero para este caso).

---

## 7. Estado actual

**Fase actual: Fase 1, en el arranque (Etapa 0 — preparación de entorno).**

Nada construido todavía. El siguiente paso concreto es montar el entorno de
desarrollo con Docker:
- Instalar Docker Desktop (incluye Docker + Docker Compose).
- Entender conceptos base: imagen vs contenedor, volumen, mapeo de puertos.
- Escribir un `docker-compose.yml` con un servicio PostgreSQL + volumen para
  persistencia.

### Plan detallado de la Fase 1 (orden de ataque)

0. **Entorno:** Python 3.10+ con entorno virtual (venv); Docker Desktop;
   PostgreSQL en contenedor vía docker-compose con volumen; un cliente gráfico
   (pgAdmin o DBeaver) para inspeccionar la base.
1. **Reconocimiento (detective):** abrir DevTools en una página de producto de
   MercadoLibre, identificar etiqueta + clase de cada dato (precio, título, stock).
   Revisar `/robots.txt`. Ojo: si el dato lo inyecta JavaScript, buscar bloque
   JSON-LD en el HTML; si no, considerar Selenium/Playwright (dejar para después).
2. **Schema:** diseñar en papel las dos tablas con tipos correctos, crearlas con
   `CREATE TABLE`, verificar que existen vacías.
3. **Scraper:** `requests.get()` con headers (User-Agent de navegador), revisar
   status code (200 ok / 403-429 bloqueo), parsear con BeautifulSoup (`.find()`,
   `.find_all()`), limpiar el texto del precio a número, manejar errores sin
   reventar, `time.sleep()` entre peticiones, probar con 3–4 URLs.
4. **ETL/Load:** conectar con `psycopg2`, cursor, upsert en productos
   (`ON CONFLICT`), insert siempre en precios, `commit`, cerrar. Correr a mano y
   verificar en pgAdmin/DBeaver; correr otra vez y confirmar que no se duplican
   productos pero sí entran precios nuevos.
5. **Automatización:** cron (`crontab -e`, sintaxis con `*/6` para cada 6 h, usar
   el Python del venv por ruta completa, redirigir logs con `>> ... 2>&1`).
   En Windows: Task Scheduler. Nota: solo corre con la máquina encendida; mover a
   VM en la nube en fases posteriores.

---

## 8. Cómo trabajar con el autor (IMPORTANTE)

- **No entregar código resuelto a menos que lo pida explícitamente.** Prefiere
  instrucciones paso a paso, explicaciones del *qué*, el *porqué* y el *cómo*, para
  escribir el código él mismo. Mencionar nombres de librerías/métodos/cláusulas
  está bien (para saber qué buscar en la documentación), pero no hacer el trabajo
  por él.
- No dar nada por hecho ni saltarse pasos.
- Comunicación directa y sin filtros; bienvenido el análisis honesto aunque
  contradiga al autor (de hecho lo pidió así explícitamente).
- Prosa explicativa, no listas de bullets escuetas.
- Sugerencia que le di y vale mantener: llevar un **diario de decisiones** (por qué
  dos tablas, por qué NUMERIC, por qué pausas entre peticiones). Son justo las
  preguntas de una entrevista de data engineering.
