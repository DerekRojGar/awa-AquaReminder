# awa (AquaReminder)

**Versión MVP para Android**

Aplicación móvil desarrollada con **Flet (Python + Flutter)** para ayudar al usuario a recordar que debe beber agua, registrar su consumo, ver métricas y recibir recordatorios locales aun cuando la app esté cerrada.

---

## Tabla de contenidos

1. [Objetivo y alcance](#objetivo-y-alcance)
2. [Instalación y configuración](#instalación-y-configuración)
3. [Versiones y compatibilidad](#versiones-y-compatibilidad)
4. [Configuración importante para compilación](#configuración-importante-para-compilación)
5. [Estructura del proyecto](#estructura-del-proyecto)
6. [Arquitectura de la aplicación](#arquitectura-de-la-aplicación)
7. [Patrones de UI](#patrones-de-ui)
8. [Compilación para Android](#compilación-para-android)
9. [Funcionalidades implementadas](#funcionalidades-implementadas)
10. [Solución de problemas](#solución-de-problemas)
11. [Desarrollo futuro](#desarrollo-futuro)

---

## Objetivo y alcance

- Desarrollar un MVP para **Android**, gestionado por una sola persona (sin cuentas de usuario, independiente por dispositivo)
- Funciones principales:
  1. **Registro rápido de agua**: Botones con iconos visuales (vaso, botella, termo) + ingestas personalizadas
  2. **Métricas avanzadas**: Total diario, promedio semanal, streaks, gráficas de progreso
  3. **Perfil personalizado**: Peso, altura, cálculo automático de IMC
  4. **Recordatorios inteligentes**: Notificaciones locales confiables incluso con la app cerrada
- **UX moderna y minimalista**: Diseño con paleta de colores moderna, interfaz responsive para móviles

---

## Instalación y configuración

### Prerrequisitos

- **Python 3.9+** instalado en el sistema
- **Git** para clonar el repositorio
- **Android Studio** (opcional, pero recomendado para emuladores y debugging)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/awa-AquaReminder.git
cd awa-AquaReminder
```

### Paso 2: Crear y activar entorno virtual

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación en modo desarrollo

```bash
cd app
flet run
```

### Paso 5: Ejecutar en dispositivo móvil

Para probar en dispositivo móvil conectado via USB:
```bash
flet run --android
```

Para ejecutar en modo web (desarrollo):
```bash
flet run --web
```

---

## Versiones y compatibilidad

| Tecnología | Versión utilizada | Notas |
|------------|-------------------|-------|
| **Python** | 3.9+ | Versión mínima requerida |
| **Flet** | 0.28.3 | Versión actual del proyecto |
| **Flutter** | 3.24.0+ | SDK interno de Flet |
| **Serious Python** | 0.9.2 | Runtime de Python para Flutter |

### Dependencias del proyecto

El archivo `requirements.txt` contiene:
- `flet==0.28.3` - Framework principal para la aplicación

---

## Configuración importante para compilación

### Configuración de pubspec.yaml

El proyecto incluye dos archivos importantes para la compilación:

1. **`pubspec_overrides.yaml`** (en la raíz del proyecto):
```yaml
dependency_overrides:
  webview_flutter_android: ^3.16.7
  wakelock_plus: ^1.2.10
  web: ^1.0.0
  window_manager: ^0.4.3
```

2. **`build/flutter/pubspec.yaml`** (generado automáticamente por Flet):
```yaml
dependency_overrides:
  webview_flutter_android: ^3.16.7
  wakelock_plus: ^1.2.10
  web: ^1.0.0
  window_manager: ^0.4.3
  flet: 0.28.3
```

**⚠️ CRÍTICO:** La configuración `webview_flutter_android: ^3.16.7` es esencial para evitar errores de compilación en Android. Esta debe estar presente en `pubspec_overrides.yaml` antes de compilar.

---

## Estructura del proyecto

```
awa-AquaReminder/
├── app/                          # Código fuente principal
│   ├── main.py                   # Punto de entrada de la aplicación
│   ├── config.py                 # Configuración global (colores, diseño)
│   ├── models/                   # Modelos de datos
│   │   ├── intake.py            # Modelo de ingesta de agua
│   │   ├── user.py              # Modelo de usuario/perfil
│   │   └── reminder_settings.py # Configuración de recordatorios
│   ├── services/                # Lógica de negocio
│   │   ├── db.py                # Acceso a base de datos SQLite
│   │   ├── metrics.py           # Cálculos de métricas e IMC
│   │   ├── reminders.py         # Lógica de recordatorios
│   │   └── notifications.py     # Servicio de notificaciones
│   └── ui/                      # Interfaz de usuario
│       └── pages/               # Páginas de la aplicación
│           ├── home.py          # Página principal
│           ├── history.py       # Historial de consumo
│           ├── profile_setup.py # Configuración de perfil
│           ├── settings.py      # Ajustes de la app
│           └── onboarding.py    # Proceso de incorporación
├── build/                       # Archivos de compilación Flutter
│   └── flutter/
│       └── pubspec.yaml         # Configuración Flutter generada
├── pubspec_overrides.yaml       # Override de dependencias Flutter
├── requirements.txt             # Dependencias Python
└── README.md                    # Este archivo
```

---

## Arquitectura de la aplicación

### Capas de la aplicación

1. **UI Layer** (`ui/pages/`)
   - Páginas construidas como funciones que retornan `ft.View`
   - Navegación basada en rutas con `page.go()`
   - Sin componentes separados, UI directa por página

2. **Services Layer** (`services/`)
   - **DB**: Persistencia con SQLite local
   - **Metrics**: Cálculos de IMC, promedios, streaks
   - **Reminders**: Lógica de recordatorios automáticos
   - **Notifications**: Interfaz para notificaciones locales

3. **Models Layer** (`models/`)
   - Estructuras de datos para ingesta, usuario y configuraciones
   - Sin ORM, clases simples de Python

4. **Config Layer** (`config.py`)
   - Paleta de colores moderna
   - Constantes de diseño (espaciados, tipografías)
   - Utilidades de compatibilidad para diferentes versiones de Flet

### Paleta de colores

La aplicación utiliza una paleta moderna basada en gradientes:
- **Dark Navy**: `#040513` (fondo principal)
- **Coral Red**: `#FB5B4B` (botones primarios)
- **Peach**: `#FBAD8C` (acentos)
- **Vibrant Red**: `#E6433C` (alertas/progress)
- **Dark Brown**: `#341F23` (textos secundarios)

---

## Patrones de UI

### Principios de diseño

- **Minimalismo funcional**: Interfaz limpia con acciones claras
- **Mobile-first**: Diseño responsive optimizado para Android
- **Iconografía intuitiva**: Botones con iconos visuales (vaso, botella, termo)
- **Feedback inmediato**: Animaciones y estados visuales claros

### Componentes principales

1. **Botones de ingesta rápida**: Iconos con cantidad predefinida
2. **Ingesta personalizada**: Modal para crear medidas custom con iconos
3. **Barra de progreso**: Visualización del progreso diario
4. **Navegación inferior**: Acceso rápido a todas las secciones
5. **Cards de métricas**: Información organizada en tarjetas

### Navegación

- `/` - Página principal (home)
- `/profile` - Configuración de perfil
- `/history` - Historial de consumo
- `/settings` - Ajustes de la aplicación
- `/onboarding` - Proceso de configuración inicial

---

## Compilación para Android

### Preparación del entorno

1. **Verificar instalación de Flet:**
   ```bash
   flet doctor
   ```

2. **Asegurar configuración correcta:**
   - Verificar que `pubspec_overrides.yaml` existe en la raíz
   - Confirmar versiones en el archivo

### Proceso de compilación

1. **Build para desarrollo:**
   ```bash
   flet build apk
   ```

2. **Build para release:**
   ```bash
   flet build apk --release
   ```

3. **Build con configuración específica:**
   ```bash
   flet build apk --build-version 1.0.1 --build-number 2
   ```

### Archivos generados

- APK de desarrollo: `dist/awa_aquareminder.apk`
- APK de release: `dist/awa_aquareminder-release.apk`

---

## Funcionalidades implementadas

### ✅ Core Features

- [x] **Registro rápido de agua** - Botones visuales con cantidades predefinidas
- [x] **Ingestas personalizadas** - Modal para crear medidas custom con iconos
- [x] **Progreso diario** - Barra de progreso y contador en tiempo real
- [x] **Perfil de usuario** - Peso, altura, cálculo automático de IMC
- [x] **Historial completo** - Registro detallado de consumo con filtros
- [x] **Métricas avanzadas** - Promedios, streaks, estadísticas semanales
- [x] **Navegación fluida** - Rutas optimizadas y transiciones suaves
- [x] **Diseño responsive** - Interfaz adaptable a diferentes tamaños de pantalla

### ✅ UI/UX Enhancements

- [x] **Paleta de colores moderna** - Esquema visual actualizado
- [x] **Iconografía intuitiva** - Símbolos claros para cada acción
- [x] **Feedback visual** - Animaciones y estados de botones
- [x] **Layout optimizado** - Espaciado y tipografía consistentes

### 🔄 En desarrollo

- [ ] **Notificaciones locales** - Recordatorios automáticos
- [ ] **Configuración de horarios** - Personalización de recordatorios
- [ ] **Exportación de datos** - Backup y restore de información

---

## Solución de problemas

### Errores comunes de instalación

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'flet'` | Entorno virtual no activado | Activar venv: `venv\Scripts\activate` |
| `flet: command not found` | Flet no instalado globalmente | Instalar: `pip install flet==0.28.3` |

### Errores de compilación Android

| Error | Causa | Solución |
|-------|-------|----------|
| `webview_flutter_android` version conflict | Versión incompatible | Verificar `pubspec_overrides.yaml` |
| Build fails with dependency errors | Caché corrupto | `flet clean` y rebuild |
| APK no instala en dispositivo | Permisos o firma | Habilitar "Unknown sources" |

### Errores de runtime

| Error | Causa | Solución |
|-------|-------|----------|
| `AttributeError: module 'flet' has no attribute 'X'` | Incompatibilidad versión | Verificar versión Flet 0.28.3 |
| Base de datos no se crea | Permisos de escritura | Verificar permisos en directorio app |
| UI se ve cortada en móvil | Layout no responsive | Revisar configuración de SafeArea |

### Debugging

Para debugging detallado:
```bash
flet run --verbose
```

Para logs específicos de Android:
```bash
flet run --android --verbose
```

---

## Desarrollo futuro

### Fase 2 - Features avanzadas

- **Sincronización en la nube** - Backup automático de datos
- **Notificaciones push** - Recordatorios remotos configurables
- **Análisis predictivo** - Recomendaciones basadas en patrones
- **Integración con wearables** - Conexión con smartwatches

### Fase 3 - Expansión de plataforma

- **Versión iOS** - Port completo para App Store
- **Aplicación web** - PWA para uso en navegadores
- **Desktop apps** - Versiones para Windows/macOS/Linux

### Optimizaciones técnicas

- **Performance** - Optimización de consultas DB y rendering
- **Batería** - Reducción de consumo energético
- **Tamaño APK** - Minimización de dependencias
- **Accesibilidad** - Mejoras para usuarios con discapacidades

---

## Contribución y soporte

### Para desarrolladores

1. **Fork** del repositorio
2. **Clone** del fork local
3. **Branch** para nueva feature: `git checkout -b feature/nueva-funcionalidad`
4. **Commit** cambios: `git commit -m "Add nueva funcionalidad"`
5. **Push** al fork: `git push origin feature/nueva-funcionalidad`
6. **Pull Request** al repositorio principal

### Reportar bugs

Crear un issue con:
- Descripción detallada del problema
- Pasos para reproducir
- Screenshots (si aplica)
- Información del dispositivo
- Logs de error

### Contacto

- **Issues**: GitHub Issues para bugs y features
- **Discusiones**: GitHub Discussions para preguntas generales

---

## Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para detalles completos.

### Privacidad

- **Datos locales**: Toda la información se almacena localmente en el dispositivo
- **Sin tracking**: No se recopilan datos de uso ni analytics
- **Sin cuentas**: No requiere registro ni autenticación
- **Permisos mínimos**: Solo se solicitan permisos esenciales (notificaciones)

---

**Desarrollado con ❤️ usando Flet + Python + Flutter**

*Última actualización: Septiembre 2025*
