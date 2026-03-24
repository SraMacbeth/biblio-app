# 📋 Plan de Desarrollo: Sistema de Gestión de Biblioteca

## 🔴 Fase 1: Prioridad Alta (Cierre del MVP - Libros)

*Tareas indispensables para que el módulo de libros sea funcional y seguro antes de pasar a otras entidades.*

* [X] **Pruebas de Unidad (Modelo):** Finalizar los 3 tests básicos (Verificación de códigos, Integridad por préstamos y Continuidad de secuencia).

* [X] **Pruebas de Integración (Controlador):** Implementar los tests de búsqueda (formato de detalles) e inyección automática de `CURRENT_USER_ID`.

* [X] **Gestión de Ciclo de Vida:** Implementar reactivación de libros (Inactivo -> Activo) y sincronización de copias en update_book.

* [X] **Vista de Actualización:** Crear el formulario que se autopueble al eidtar un libro.

* [X] Integrar el `ttk.Treeview` para visualizar la lista de copias únicas y sus estados.

* [ ] **Reordenamiento Visual del formulario de Edición:** Reemplazo de tabla de copias y campo "Añadir" por botón de "Gestión de Copias" y separador visual.

* [ ] **Advertencia Informativa de Estado:** Implementar mensaje informativo al seleccionar un nuevo estado que explique consecuencias y alternativas de gestión individual.

* [ ] **Dinamismo en Motivos de Inactivación:** Crear selector de motivos (Dañado, Robo, Pérdida, Descatalogado, Donación) con visibilidad sujeta al estado "Inactivo".

* [ ] **Validación Decisoria y Guardado:**  Validar si existen modificaciones efectivas en el formulario antes de procesar la actualización.

* [ ] **Optimización de Cambios Reales:** Validar si existen modificaciones efectivas en el formulario antes de procesar la actualización.
> *​Nota: Incluye creación de test automatizado de flujo de control.*

* [ ] **Formulario de Gestión de Copias (Toplevel):** Crear ventana independiente para administración de ejemplares con lógica de reactivación automática del libro al añadir stock.
> *​Nota: Incluye creación de test automatizado de reglas de inventario.*

* [ ] **Gran Refactor de Libros:** Limpieza de código, eliminación de comentarios obsoletos y estandarización de nombres de variables en el CRUD de libros.

## 🟡 Fase 2: Expansión de Entidades (Flujo Principal)

*Una vez que Libros es sólido, replicar el esquema en los otros pilares del sistema.*

* [ ] **Búsqueda Global:**
* [ ] Test de Integración: Diseñar la prueba para get_all_inventory (esperando lista de libros).
* [ ] Modelo (book_model.py): Implementar get_all_books con SELECT y conteo de copias.
* [ ] Controlador (book_controller.py): Conectar el retorno del modelo y formatear los datos para el Treeview.
* [ ] Vista: Crear la pantalla de Inventario Total.

* [ ] **Módulo de Socios (Members):**
* [ ] Desarrollar CRUD completo (Modelo, Controlador, Vista).
* [ ] Implementar validación de DNI/ID único.

* [ ] **Módulo de Préstamos (Loans):**
* [ ] Lógica para asociar un `copy_id` con un `member_id`.
* [ ] Cambio automático de `status_loan` de "Disponible" a "Prestado".

* [ ] **Gestión de Sesión Real:**
* [ ] Limpiar campos de login tras ingreso exitoso.
* [ ] Reemplazar la constante `CURRENT_USER_ID = 1` por el ID capturado dinámicamente desde la vista Home hacia las demás capas.
* [ ] Implementar lógica de código de acceso único (OTP) para la validación de email en `resetPasswordScreen`.


## 🟢 Fase 3: Feedback Visual y UX (Pulido del MVP)

*Mejoras en la experiencia de usuario sin añadir complejidad en la base de datos.*

* [ ] **Alertas Visuales en el Treeview:**
* [ ] Configurar Tags de colores en `books_view.py`.
* [ ] Lógica: Fila **Rojo suave** para Stock = 0.
* [ ] Lógica: Fila **Gris** para libros "Inactivos".


* [ ] **Manejo de Errores en UI:** Asegurar que todos los mensajes de error del controlador se muestren en `messagebox` de Tkinter.

* [ ] **Estandarización de Flujo de Ventanas:** Asegurar que los formularios permanezcan abiertos ante errores de validación y solo se cierren tras una confirmación de éxito ("ok").

## 🔵 Fase 4: Versión Mejorada (Post-MVP / Futuro)

*Ideas para cuando el sistema base esté funcionando al 100%.*

* [ ] **Optimización de Consultas (SQL JOINs):** Unificar las llamadas en `get_book_by_id` para traer autores y géneros en una sola sentencia.
* [ ] **Múltiples Autores:** Rediseñar el modelo y la vista para permitir N autores por libro.
* [ ] **Gestión de Autores:** Investigar y normalizar el manejo de autores con un solo nombre (ej. Osho, Anónimo).
📋 Backlog (Versiones Futuras / Fase 3)
* [ ] **Gestión Individual de Copias:** Botón de edición por fila en el formulario de libro para cambiar estados puntuales (Dañado, Extraviado, etc.).
* [ ] **Buscador Avanzado:** Implementar un buscador dinámico con filtros avanzados (por autor, por género, título o ISBN, con búsqueda predictiva). Implementar el "Doble clic para editar" (paso de parámetros entre ventanas).
* [ ] **Validación de ISBN:** Implementar Regex para asegurar el formato estándar de 13 dígitos.
* [ ] **Carga de Imágenes:** Permitir vincular una ruta de imagen para la portada del libro.

