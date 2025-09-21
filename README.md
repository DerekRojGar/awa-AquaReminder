# awa (AquaReminder)

**Versión MVP para Android**

Aplicación móvil desarrollada con **Flet (Python + Flutter)** para ayudar al usuario a recordar que debe beber agua, registrar su consumo, ver métricas y recibir recordatorios locales aun cuando la app esté cerrada.

---

## Tabla de contenidos

1. [Objetivo y alcance](#objetivo-y-alcance)  
2. [Visión general de la arquitectura](#visión-general-de-la-arquitectura)  
3. [Estructura de carpetas](#estructura-de-carpetas)  
4. [Patrones de UI: componentes en Flet](#patrones-de-ui-componentes-en-flet)  
5. [Estado y comunicación entre componentes](#estado-y-comunicación-entre-componentes)  
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

Arquitectura en capas, modular, para mantener claridad y facilidad de mantenimiento:

- **UI**  
  Pantallas (“pages”) y componentes reutilizables (`UserControl`), solo para presentación / interacción.

- **Estado global**  
  `AppState`: mantiene valores actuales como perfil de usuario, entradas de agua, configuración de recordatorios; permite suscripción de componentes.

- **Servicios (business logic)**  
  Lógica de métricas, persistencia (base de datos local), recordatorios, notificaciones.

- **Modelos de datos**  
  Estructuras que representan ingesta, usuario, configuraciones, etc.

- **Parte nativa / extensiones**  
  Sólo para código Android que permita notificaciones locales confiables en background.

---

## Estructura de carpetas
```bash
water_minder/
├─ app/
│ ├─ main.py
│ ├─ app_state.py
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
│   ├─ pages/
│   │ ├─ home.py
│   │ ├─ history.py
│   │ ├─ profile.py
│   │ └─ settings.py
│   └─ components/
│     ├─ progress_with_label.py
│     ├─ quick_intake_button.py
│     ├─ graph_view.py
│     └─ other reutilizables...
├─ assets/
│ ├─ icons/
│ └─ images/
├─ native/
│ └─ android_ext_code/ # código para extensión de notificaciones
├─ tests/
├─ requirements.txt
├─ README.md
└─ .gitignore
```
**Explicaciones de carpetas clave:**

| Carpeta | Contenido / responsabilidad |
|--------|-----------------------------|
| `app` | Código fuente principal de la aplicación. |
| `app_state.py` | Estado global, suscripciones de UI, cambio de valores. |
| `config.py` | Constantes; valores por defecto (meta diaria, intervalos, etc.). |
| `models/` | Definición de estructuras de datos: ingesta, usuario, ajustes de recordatorio. |
| `services/db.py` | Persistencia local (SQLite): agregar ingesta, leer datos. |
| `services/metrics.py` | Lógica de cálculo de IMC, promedios, streaks, etc. |
| `services/reminders.py` | Lógica que decide *cuándo* debe recordarse beber agua. |
| `services/notifications.py` | Interfaz/adapter para programación de notificaciones; puede tener múltiples implementaciones. |
| `ui/pages/` | Pantallas completas para el usuario: Home, Historial, Perfil, Ajustes. |
| `ui/components/` | Componentes reutilizables: botones, gráficas, barra de progreso, etc. |
| `native/android_ext_code/` | Código específico de Android (Java/Kotlin / Plugin Flutter) para manejar notificaciones locales confiables. |

---

## Patrones de UI: componentes en Flet

- Utilizar `UserControl` para componentes que combinan varios controles, tienen estado local o lógica de actualización (ej. barra de progreso con etiqueta, gráfica, botón rápido).  
- Pantallas (“pages”) ensamblan esos componentes. Cada página es también un `UserControl`.  
- Componentes simples que no requieren lógica interna pueden ser funciones o clases muy ligeras.  
- Reutilizar componentes que aparecen en varias páginas, evitando duplicar código.  
- Mantener estilos comunes (colores, fuentes, márgenes) en un módulo de estilos/configuración (`config.py` u `ui/common_styles`).

---

## Estado y comunicación entre componentes

- `AppState` central como punto único de verdad: perfil de usuario, metas, entradas, configuraciones.  
- Componentes se **suscriben** al `AppState` para recibir notificaciones de cambio.  
- Cuando servicios modifican datos (por ejemplo, al guardar una nueva ingesta o al actualizar configuración de recordatorio), deben llamar a `AppState.notify()`.  
- Componentes que escuchan usan su método de actualización (`update()` en `UserControl`) para refrescar visual.  
- Esta separación minimiza acoplamientos entre UI y lógica de negocio.

---

## Servicios y separación de responsabilidades

- **DB**: todas las operaciones de lectura/escritura se hacen en `services/db.py` — UI no debe acceder directamente a la base de datos.  
- **Metrics**: funciones puras para calcular IMC, promedios, streaks, valores históricos para gráficas.  
- **Reminders**: lógica para calcular cuándo se debe disparar notificación basado en:
  1. Configuración del usuario (intervalos, horarios permitidos, snooze).  
  2. Última ingesta registrada.  
  Luego delega al `NotificationService` la tarea de programarla.  
- **NotificationService**: adapter / interfaz. Hay al menos dos implementaciones:
  - Una “dev” para pruebas y desarrollo.  
  - Una nativa para Android con notificaciones locales confiables.  

---

## Notificaciones locales: estrategia y limitaciones

- **Objetivo**: que los recordatorios funcionen incluso si la app está cerrada.  
- **En desarrollo**: usar librería comunitaria o fallback “dev implementation” para validar lógica, interfaz, horarios, snooze.  
- **Producción (Android)**: implementar extensión nativa (user extension de Flet) con `flutter_local_notifications` para programar notificaciones locales.  
- **Permisos**: solicitar permisos de notificación al usuario al instalar o al iniciar app.  
- **Limitaciones posibles**: versiones de Android con restricciones de batería, OEMs agresivos con background tasks, permisos de usuario. Probar en dispositivos reales.  

---

## Flujo de desarrollo y checklist de validación

1. Diseñar UI minimalista + perfil + lógica de métricas.  
2. Persistir datos con SQLite local.  
3. Implementar recordatorios automáticos basados en la última ingesta, usando el adapter dev.  
4. Crear pantalla de “Ajustes” que permita configurar intervalos, horarios permitidos, snooze, activación/desactivación.  
5. Crear extensión Android y reemplazar adapter dev por implementación nativa para notificaciones fiables.  
6. Probar en dispositivo real: notificaciones con app cerrada + app abierta + acciones de snooze.  

**Checklist mínimo:**

- [ ] Registro de agua rápido (botones y entrada custom).  
- [ ] Perfil con cálculo de IMC.  
- [ ] Métricas: promedio semanal, streaks, gráfica.  
- [ ] Progreso diario visible (barra + valor).  
- [ ] Recordatorios locales funcionan con app cerrada.  
- [ ] Permisos solicitados correctamente.  
- [ ] Datos persistentes entre cierres de app / reinicios.

---

## Convenciones y buenas prácticas

- **Nomenclatura**: clases en `PascalCase`, archivos en `snake_case`.  
- **Componentes**: piezas reutilizables como `UserControl`.  
- **Lógica fuera de UI**: UI solo presentaciones + eventos; servicios hacen cálculos, persistencia.  
- **Constantes / configuraciones** en un archivo central (`config.py`).  
- **Estilo coherente**: colores, tipografía, márgenes uniformes.  
- **Pruebas unitarias** (mínimo para servicios/DB/metrics).  
- **Documentación mínima**: docstrings + comentarios clave.

---

## Futuro / features fase 2

- Sincronización / respaldo en la nube.  
- Recordatorios push remotos o ajustes vía servidor.  
- Personalización avanzada de notificaciones: sonidos, vibraciones, horarios “no molestar”.  
- Más visuales o panoramas estadísticos, recomendaciones automáticas.

---

## Referencias clave

- Flet — custom controls / `UserControl`.  
- Flet — user extensions (integrar paquetes Flutter externos).  
- Flet — build / publish Android (APK / AAB).  
- `flutter_local_notifications` — para notificaciones locales confiables en Android.  
- `flet_notifications` u otras librerías dev como fallback.

---

**Licencia / privacidad**

- Datos personales anónimos, usados localmente, sin cuentas de usuario.  
- Permisos de notificación solicitados claramente, explicando beneficio al usuario.

---

*Fin del README*  
