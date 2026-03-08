# BiblioApp: Sistema de Gestión de Biblioteca

BiblioApp es una aplicación de escritorio robusta diseñada para la digitalización y administración de bibliotecas públicas. Permite un control integral sobre el inventario de libros, el registro de socios y el flujo de préstamos, garantizando una experiencia de usuario intuitiva y eficiente.

---

## 🚀 Características Principales

* **Control de Acceso:** Sistema de autenticación seguro para administradores (Registro, Login y recuperación de credenciales).
* **Gestión de Inventario:** CRUD completo de libros (Alta, consulta detallada, edición y bajas).
* **Administración de Socios:** Gestión eficiente del padrón de usuarios de la biblioteca.
* **Módulo de Circulación:** Control automatizado de préstamos y devoluciones en tiempo real.
* **Persistencia de Datos:** Implementación con SQLite para un manejo de datos ligero y fiable.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.8+
* **Interfaz Gráfica:** Tkinter
* **Base de Datos:** SQLite3
* **Arquitectura:** Pattern Model-View-Controller (MVC) para un código escalable y mantenible.

## 📂 Estructura del Proyecto

```text
├── components/          # Elementos reutilizables de la UI
├── controllers/         # Lógica de negocio y manejo de eventos
├── db/                  # Scripts de base de datos y esquemas
├── images/              # Recursos visuales del sistema
├── models/              # Definición de clases y acceso a datos
├── views/               # Definición de las interfaces de usuario
├── main.py              # Punto de entrada de la aplicación
└── requirements.txt     # Dependencias del proyecto
