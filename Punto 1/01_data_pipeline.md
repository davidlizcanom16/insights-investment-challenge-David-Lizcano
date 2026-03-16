# Punto 1 — Consulta de Balances por Asesor, Rango de Fechas y Tipo de Portafolio

## Contexto

El objetivo es extraer los balances de portafolios para un rango de fechas
y tipo de portafolio específico, filtrando únicamente los usuarios que
pertenecen a un asesor determinado.

Para lograrlo, se construye una pipeline de transformación que conecta las
cuatro tablas disponibles — `Portafolios`, `Usuarios`, `Asesores`, `Balances` —
usando joins progresivos y eliminando campos innecesarios en cada etapa para
mantener la tabla de trabajo limpia.

La lógica central es simple: primero identificar qué portafolios pertenecen
al asesor objetivo, y luego traer los balances filtrados sobre ese subconjunto.

---

## Tablas disponibles

| Tabla | Campos clave |
|-------|-------------|
| `Usuarios` | id_usuario, email, id_asesor, perfil_riesgo |
| `Portafolios` | id_portafolio, id_usuario, tipo_portafolio |
| `Asesores` | id_asesor, email, num_clientes |
| `Balances` | id_portafolio, fecha, balance |

---

## Pipeline de transformación
```sql
-- Paso 1: Unir portafolios con sus usuarios
join(Portafolios, Usuarios, id_usuario, Usuarios_portafolios)
-- Resultado: id_portafolio | id_usuario | tipo_portafolio | email(usuario) | id_asesor | perfil_riesgo
```
```sql
-- Paso 2: Eliminar campos del usuario que no necesitamos
-- (pasos 1 y 2 dados en el enunciado)
drop(Usuarios_portafolios, email & perfil_riesgo)
-- Resultado: id_portafolio | id_usuario | tipo_portafolio | id_asesor
```
```sql
-- Paso 3: Incorporar información del asesor
join(Usuarios_portafolios, Asesores, id_asesor, Portafolios_asesores)
-- Resultado agrega: email(asesor) | num_clientes
-- Nota: el email del usuario fue eliminado en el paso 2,
--       no hay ambigüedad de campos al hacer este join
```
```sql
-- Paso 4: Filtrar solo los registros del asesor objetivo
filter(Portafolios_asesores, email = "insightswm@gmail.com")
-- Resultado: solo portafolios gestionados por ese asesor
```
```sql
-- Paso 5: Limpiar campos del asesor, ya no son necesarios
drop(Portafolios_asesores, id_usuario & id_asesor & email & num_clientes)
-- Resultado: id_portafolio | tipo_portafolio
```
```sql
-- Paso 6: Traer los balances para esos portafolios
join(Portafolios_asesores, Balances, id_portafolio, Resultado)
-- Resultado: id_portafolio | tipo_portafolio | fecha | balance
```
```sql
-- Paso 7: Filtrar por rango de fechas
filter(Resultado, fecha >= "YYYY-MM-DD" & fecha <= "YYYY-MM-DD")
```
```sql
-- Paso 8: Filtrar por tipo de portafolio
filter(Resultado, tipo_portafolio = "acciones")  -- o el tipo deseado
```
```sql
-- Paso 9 (opcional): Eliminar la llave técnica si la salida es para visualización
drop(Resultado, id_portafolio)
-- Resultado final: tipo_portafolio | fecha | balance
```

---

## Notas de diseño

**Sobre el orden de los filtros:**
Los pasos 7 y 8 son independientes entre sí y pueden aplicarse en cualquier
orden. En un sistema real, aplicar el filtro de fecha primero reduce el volumen
de datos antes del segundo filtro — esto equivale a un *predicate pushdown* en
motores de consulta como Spark o BigQuery.

**Sobre la ambigüedad de campos:**
El `drop` en el paso 2 elimina el email del usuario antes de hacer el join con
Asesores en el paso 3. Esto no es casualidad — si ambos emails estuvieran
presentes al momento del filtro en el paso 4, la condición
`email = "insightswm@gmail.com"` podría aplicarse sobre el campo equivocado.
El orden de los drops importa.

**Sobre el paso 9:**
Es opcional y depende del uso final del resultado. Si la salida alimenta otro
proceso, conviene mantener `id_portafolio` como llave de trazabilidad.
Si es para visualización o reporte, puede eliminarse para limpiar la tabla.
