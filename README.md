# 📚 BiblioApp: Sistema de Gestión de Biblioteca

BiblioApp es una aplicación de escritorio diseñada para la administración integral de bibliotecas públicas. El sistema permite un control eficiente del inventario de libros, la gestión de socios y el flujo de préstamos, bajo una arquitectura sólida y mantenible.

---

## 🚀 Características Principales

* **Gestión de Usuarios:** Registro, login seguro y recuperación de contraseña para administradores.
* **Catálogo de Libros:** CRUD completo (Alta, Baja, Edición y Consulta) con fichas técnicas detalladas.
* **Administración de Socios:** Gestión eficiente de altas y bajas de los miembros de la biblioteca.
* **Módulo de Circulación:** Control automatizado de préstamos y devoluciones en tiempo real.
* **Arquitectura MVC:** Separación clara entre la lógica de negocio, la interfaz y los datos.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.8
* **Interfaz Gráfica:** Tkinter (GUI)
* **Base de Datos:** SQLite3 (Motor relacional ligero)

## 📁 Estructura del Proyecto

```text
├── components/          # Widgets y componentes de UI reutilizables
├── controllers/         # Lógica de control y comunicación MVC
├── db/                  # Scripts y archivos de base de datos
├── images/              # Recursos gráficos y assets
├── models/              # Definición de clases y acceso a datos
├── views/               # Interfaces de usuario y layouts
├── main.py              # Punto de entrada de la aplicación
└── requirements.txt     # Listado de dependencias
```

## ⚙️ Instalación

Sigue estos pasos para configurar el entorno local:

1. **Clonar el repositorio:**
   git clone https://github.com/tu-usuario/biblioapp.git

2. **Crear y activar el entorno virtual:**
   python -m venv venv
   
   En Windows: venv\Scripts\activate
   
   En macOS/Linux: source venv/bin/activate

3. **Instalar dependencias:**
   pip install -r requirements.txt

## 🖥️ Uso

Para lanzar la aplicación, ejecuta el siguiente comando desde la raíz del proyecto:

python3 main.py

---

## 📌 Estado del Proyecto
> **Nota:** Este proyecto se encuentra actualmente en fase de **MVP (Producto Mínimo Viable)**. Puedes consultar la hoja de ruta de futuras mejoras en el archivo TODO.md.

## 👩‍💻 Autor
**Emilia Poletti**