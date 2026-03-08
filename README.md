# BiblioApp: Sistema de Gestión de Biblioteca

BiblioApp es una aplicación de escritorio robusta diseñada para la digitalización y administración de bibliotecas públicas. Permite un control integral sobre el inventario de libros, el registro de socios y el flujo de préstamos, garantizando una experiencia de usuario intuitiva y eficiente.

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

⚙️ Instalación y Configuración
Sigue estos pasos para ejecutar el proyecto de forma local:
 * Clonar el repositorio:
   git clone [https://github.com/SraMacbeth/biblioapp.git](https://github.com/SraMacbeth/biblioapp.git)
cd biblioapp

 * Configurar el entorno virtual:
   python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

 * Instalar dependencias:
   pip install -r requirements.txt

🖥️ Uso
Para iniciar la aplicación, ejecuta el script principal desde la raíz del proyecto:
python main.py

📌 Estado del Proyecto
Actualmente el proyecto se encuentra en fase MVP (Producto Mínimo Viable).
> Puedes consultar la hoja de ruta de futuras mejoras y funcionalidades planificadas en el archivo TODO.md.
> 
👩‍💻 Autora
Emilia Poletti - Desarrolladora del proyecto

