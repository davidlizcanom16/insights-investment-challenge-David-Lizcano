# Consulta de Balances por Asesor, Rango de Fechas y Tipo de Portafolio

# Contexto
El objetivo de la prueba fue extraer los balances de portafolios para un rango de fechas y tipo de portafolio específico, filtrando únicamente los usuarios que pertenecen a un asesor determinado.

Para lograrlo, se construye una pipeline de transformación que conecta las cuatro tablas disponibles (Portafolios, Usuarios, Asesores, Balances) usando joins progresivos, eliminando campos innecesarios en cada etapa para mantener la tabla de trabajo limpia.
La lógica central es: primero identificar qué portafolios pertenecen al asesor objetivo, y luego traer los balances filtrados sobre ese subconjunto.


-- Paso 1: Unir portafolios con sus usuarios
join(Portafolios, Usuarios, id_usuario, Usuarios_portafolios)
-- Resultado: id_portafolio | id_usuario | tipo_portafolio | email(usuario) | id_asesor | perfil_riesgo

-- Paso 2: Eliminar campos del usuario que no necesitamos (dado en el enunciado)
drop(Usuarios_portafolios, email & perfil_riesgo)
-- Resultado: id_portafolio | id_usuario | tipo_portafolio | id_asesor

-- Paso 3: Incorporar información del asesor
join(Usuarios_portafolios, Asesores, id_asesor, Portafolios_asesores)
-- Resultado agrega: email(asesor) | num_clientes
-- Nota: el email del usuario ya fue eliminado en el paso 2, no hay ambigüedad de campos

-- Paso 4: Filtrar solo los registros del asesor objetivo
filter(Portafolios_asesores, email = "insightswm@gmail.com")
-- Resultado: solo portafolios gestionados por ese asesor

-- Paso 5: Limpiar campos del asesor, ya no son necesarios
drop(Portafolios_asesores, id_usuario & id_asesor & email & num_clientes)
-- Resultado: id_portafolio | tipo_portafolio

-- Paso 6: Traer los balances para esos portafolios
join(Portafolios_asesores, Balances, id_portafolio, Resultado)
-- Resultado: id_portafolio | tipo_portafolio | fecha | balance

-- Paso 7: Filtrar por rango de fechas
filter(Resultado, fecha >= "YYYY-MM-DD" & fecha <= "YYYY-MM-DD")

-- Paso 8: Filtrar por tipo de portafolio
filter(Resultado, tipo_portafolio = "acciones")  -- o el tipo deseado

-- Paso 9 (opcional): Eliminar la llave técnica si la salida es para visualización
drop(Resultado, id_portafolio)
-- Resultado final: tipo_portafolio | fecha | balance
