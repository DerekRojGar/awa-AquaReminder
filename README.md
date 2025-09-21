# awa (AquaReminder)

**Versión MVP para Android**

Aplicación móvil desarrollada con **Flet (Python + Flutter)** para ayudar al usuario a recordar que debe beber agua, registrar su consumo, ver métricas y recibir recordatorios locales aun cuando la app esté cerrada.

---

## Tabla de contenidos

1. [Objetivo y alcance](#objetivo-y-alcance)  
2. [Visión general de la arquitectura](#visión-general-de-la-arquitectura)  
3. [Estructura de carpetas](#estructura-de-carpetas)  
4. [Patrones de UI: páginas en Flet (sin UserControl)](#patrones-de-ui-páginas-en-flet-sin-usercontrol)  
5. [Estado y flujo entre páginas](#estado-y-flujo-entre-páginas)  
6. [Servicios y separación de responsabilidades](#servicios-y-separación-de-responsabilidades)  
7. [Notificaciones locales: estrategia y limitaciones](#notificaciones-locales-estrategia-y-limitaciones)  
8. [Flujo de desarrollo y checklist de validación](#flujo-de-desarrollo-y-checklist-de-validación)  
9. [Convenciones y buenas prácticas](#convenciones-y-buenas-prácticas)  
10. [Futuro / features fase 2](#futuro--features-fase-2)  
11. [Referencias clave](#referencias-clave)  

---

## Objetivo y alcance

- Desarrollar un MVP para **Android**, gestionado por una sola persona (sin cuentas de usuario, independiente por dispositivo).  
- Funciones principales:
  1. Registrar ingestas de agua de forma rápida (botones + entrada personalizada).  
  2. Ver métricas: total diario, promedio semanal, streaks, gráficas.  
  3. Perfil con peso, altura, cálculo de IMC.  
  4. Recordatorios locales confiables, incluso cuando la app esté cerrada.  
- UX minimalista y directa: pocas pantallas, pocos botones, interfaz clara.

---

## Visión general de la arquitectura

Arquitectura en capas, simple y mantenible:

- **UI**  
  Páginas (Views) construidas como funciones y retornadas directamente; navegación por rutas (`page.go()`), sin `UserControl` ni carpeta de componentes.

- **Estado de UI**  
  Estado mínimo, local por página o por módulo (por ejemplo, onboarding por rutas `/onboarding/1..3`)

- **Servicios (business logic)**  
  Lógica de métricas, persistencia (base de datos local), recordatorios, notificaciones.

- **Modelos de datos**  
  Estructuras que representan ingesta, usuario, configuraciones, etc.

- **Parte nativa / extensiones**  
  Código Android necesario para notificaciones locales confiables en background.

---

## Estructura de carpetas
```bash
awa-aquareminder/
├─ app/
│ ├─ main.py
│ ├─ config.py
│ ├─ models/
│ │ ├─ intake.py
│ │ ├─ user.py
│ │ └─ reminder_settings.py
│ ├─ services/
│ │ ├─ db.py
│ │ ├─ metrics.py
│ │ ├─ reminders.py
│ │ └─ notifications.py
│ └─ ui/
│   └─ pages/
│      ├─ onboarding.py
│      ├─ home.py
│      ├─ history.py
│      ├─ profile.py
│      └─ settings.py
├─ assets/
│ ├─ icons/
│ └─ images/
├─ native/
│ └─ android_ext_code/
├─ tests/
├─ requirements.txt
├─ README.md
└─ .gitignore
```
**Explicaciones de carpetas clave:**

| Carpeta | Contenido / responsabilidad |
|--------|-----------------------------|
| `app` | Código fuente principal de la aplicación. |
| `config.py` | Constantes y estilos (paleta de colores, tamaños, etc.). |
| `models/` | Definición de estructuras de datos: ingesta, usuario, ajustes de recordatorio. |
| `services/db.py` | Persistencia local (SQLite): agregar ingesta, leer datos. |
| `services/metrics.py` | Lógica de cálculo de IMC, promedios, streaks, etc. |
| `services/reminders.py` | Lógica que decide cuándo debe recordarse beber agua. |
| `services/notifications.py` | Interfaz/adapter para programar notificaciones (dev y nativa). |
| `ui/pages/` | Páginas de la app (Views) renderizadas directamente; sin componentes separados. |
| `native/android_ext_code/` | Código Android para manejar notificaciones locales confiables. |

---

## Patrones de UI: páginas en Flet (sin UserControl)

- Construir cada pantalla como una función que retorna un `ft.View` o controles que se agregan a la `page`.
- Sin `UserControl` ni carpeta de componentes; mantener la UI simple y directa por página.
- Estilos compartidos desde `config.py` (colores, tamaños, espaciados) para consistencia visual.
- Navegación con `page.go("/ruta")` y rutas claras (ej. `/`, `/onboarding/1..3`, `/settings`).
- Mantener el layout sencillo (Column/Row/Container) y reutilizar patrones dentro de la misma página cuando sea necesario.

---

## Estado y flujo entre páginas

- Estado mínimo y local por página; evitar estados globales complejos cuando no sean necesarios.
- Onboarding manejado por rutas (`/onboarding/1`, `/onboarding/2`, `/onboarding/3`) y lógica de botones siguiente/atrás.
- Cuando se complete el onboarding, redirigir a `/` (home). Persistencia futura opcional si se requiere recordar la finalización entre sesiones.
- Para casos más complejos (perfil, métricas), delegar lectura/escritura a `services/` y mantener la UI reactiva solo a datos cargados.

---

## Servicios y separación de responsabilidades

- **DB**: todas las operaciones de lectura/escritura se hacen en `services/db.py` — la UI no accede directamente a la base de datos.  
- **Metrics**: funciones puras para calcular IMC, promedios, streaks, valores históricos para gráficas.  
- **Reminders**: lógica para calcular cuándo se debe disparar una notificación según configuración y última ingesta.  
- **NotificationService**: adapter con implementación de desarrollo y otra nativa para Android.

---

## Notificaciones locales: estrategia y limitaciones

- **Objetivo**: recordatorios funcionales incluso si la app está cerrada.  
- **En desarrollo**: usar implementación de desarrollo para validar lógica, horarios, snooze.  
- **Producción (Android)**: extensión nativa con `flutter_local_notifications` para programar notificaciones locales.  
- **Permisos**: solicitar permisos al instalar o al iniciar app.  
- **Limitaciones**: restricciones de batería, OEMs agresivos, permisos. Probar en dispositivos reales.

---

## Flujo de desarrollo y checklist de validación

1. Diseñar UI minimalista (páginas) + perfil + lógica de métricas.  
2. Persistir datos con SQLite local.  
3. Implementar recordatorios automáticos basados en la última ingesta (adapter dev).  
4. Pantalla de “Ajustes” para intervalos, horarios permitidos, snooze, on/off.  
5. Extensión Android y reemplazar adapter dev por implementación nativa.  
6. Probar en dispositivo real: notificaciones con app cerrada/abierta + snooze.

**Checklist mínimo:**

- [ ] Registro de agua rápido (botones y entrada custom).  
- [ ] Perfil con cálculo de IMC.  
- [ ] Métricas: promedio semanal, streaks, gráfica.  
- [ ] Progreso diario visible (barra + valor).  
- [ ] Recordatorios locales con app cerrada.  
- [ ] Permisos solicitados correctamente.  
- [ ] Datos persistentes entre cierres / reinicios.

---

## Convenciones y buenas prácticas

- **Nomenclatura**: archivos en `snake_case`.  
- **Páginas**: funciones simples que retornan Views/controles (sin `UserControl`).  
- **Lógica fuera de UI**: UI para presentación + eventos; servicios hacen cálculos y persistencia.  
- **Constantes/estilos** centralizados en `config.py`.  
- **Estilo coherente**: colores, tipografía, márgenes uniformes.  
- **Pruebas** mínimas para servicios/DB/metrics.  
- **Documentación**: docstrings + comentarios clave.

---

## Futuro / features fase 2

- Sincronización / respaldo en la nube.  
- Recordatorios push remotos o ajustes vía servidor.  
- Personalización avanzada de notificaciones.  
- Más visuales y recomendaciones basadas en hábitos.

---

## Referencias clave

- Flet — rutas y navegación (`page.go`).  
- Flet — build / publish Android (APK / AAB).  
- `flutter_local_notifications` — notificaciones locales en Android.  
- Librerías dev para notificaciones como fallback.

---

**Licencia / privacidad**

- Datos locales, sin cuentas de usuario.  
- Permisos de notificación solicitados con una explicación clara del beneficio.

---

*Fin del README*
