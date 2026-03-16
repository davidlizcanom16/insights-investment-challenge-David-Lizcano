## 4.1 Investigación previa

### 4.1.1 ¿Cómo funciona ACH en EE.UU.?

Cuando un cliente de Insights deposita dinero desde su cuenta bancaria, lo que ocurre detrás no es una transferencia instantánea. El sistema ACH funciona como una red de pagos que procesa transacciones por lotes y que involucra a varias instituciones financieras. Por eso, completar una transferencia suele tardar entre uno y tres días hábiles.

El proceso comienza cuando Insights inicia la solicitud de débito desde la cuenta del cliente. En la terminología del sistema ACH, Insights actúa como el **Originator**, es decir, la entidad que origina la transacción.

Esa instrucción primero pasa por el banco de Insights, conocido como **ODFI (Originating Depository Financial Institution)**. Este banco reúne las instrucciones de pago del día y las envía en archivos por lotes hacia la red ACH.

La **red ACH**, operada por la Reserva Federal o por The Clearing House, actúa como intermediaria. Su función es enrutar cada transacción hacia el banco correcto.

El banco del cliente, llamado **RDFI (Receiving Depository Financial Institution)**, recibe la instrucción, verifica que la cuenta exista y que tenga fondos suficientes, y ejecuta el débito. En ese momento el dinero sale de la cuenta del cliente y finalmente se acredita en la cuenta de Insights.

En cuanto a los tiempos, el ACH estándar suele tardar entre **uno y tres días hábiles** en liquidarse. Existe también la modalidad **Same-Day ACH**, que permite que la transacción se procese el mismo día siempre que se envíe antes de las ventanas de corte establecidas por la red ACH.

Algo importante que muchos clientes no saben es que incluso cuando aparece un mensaje de “transferencia exitosa”, el banco todavía puede devolver la transacción si encuentra algún problema. Por esta razón, muchas plataformas financieras mantienen un período de espera de **tres a cinco días hábiles** antes de permitir que esos fondos se utilicen para invertir.

El Same-Day ACH tiene sentido recomendarlo cuando el cliente necesita que los fondos estén disponibles ese mismo día, por ejemplo para aprovechar una oportunidad de mercado o para corregir rápidamente un fondeo fallido. Para depósitos recurrentes o programados, el ACH estándar suele ser suficiente y además es más económico.

---

### 4.1.2 Requisitos para fondear una cuenta vía ACH

Para que Insights pueda debitar dinero desde la cuenta bancaria de un cliente, es necesario recopilar algunos datos básicos. En general se requiere el nombre del titular de la cuenta, el routing number del banco, el número de cuenta bancaria y el tipo de cuenta (corriente o de ahorros).

Además de estos datos, el cliente debe aceptar una **autorización ACH**, que es el consentimiento legal que permite a la plataforma iniciar débitos desde su cuenta bancaria.

Antes de realizar el primer débito, normalmente se requiere verificar que la cuenta realmente pertenece al cliente. Un método común para hacerlo es el de **micro-depósitos**. En este proceso se envían dos pequeños montos —normalmente de menos de un dólar— a la cuenta del cliente, y el cliente debe confirmar esos montos uno o dos días después.

Otra alternativa más moderna es la verificación instantánea mediante servicios como **Plaid o MX**, que permiten al cliente iniciar sesión en su banca en línea y confirmar la cuenta en segundos.

En cuanto a límites, las cuentas nuevas suelen tener restricciones de fondeo diario que normalmente se encuentran entre **cinco mil y veinticinco mil dólares**, aunque estos límites suelen aumentar conforme el cliente utiliza la plataforma y construye historial.

Incluso después de que el depósito se procesa, los fondos suelen mantenerse en espera durante **tres a cinco días hábiles** antes de poder invertirse. Este período de retención protege a la plataforma en caso de que la transacción sea devuelta por el banco.

Cuando una transacción ACH falla, el sistema utiliza códigos de devolución definidos por Nacha. Algunos de los más comunes son **R01**, que indica fondos insuficientes; **R02**, que significa que la cuenta está cerrada; y **R03**, que indica que los datos bancarios no coinciden con ningún registro válido del banco.

En todos estos casos, lo más importante es comunicar el problema al cliente de forma clara y decirle exactamente qué debe hacer para solucionarlo.

---

### 4.1.3 Routing numbers (ABA): lógica y lookup por banco y estado

El **ABA routing number** es un código de nueve dígitos que identifica a una institución financiera dentro del sistema de pagos de Estados Unidos. Es el número que aparece en la parte inferior izquierda de los cheques y que permite que las transferencias ACH lleguen al banco correcto.

El número tiene una estructura específica. Los primeros dígitos están asociados al distrito de la Reserva Federal donde opera el banco, los siguientes identifican a la institución financiera y el último funciona como un dígito de control que permite validar matemáticamente el número.

Algo que suele generar confusión es que un mismo banco puede tener distintos routing numbers dependiendo del estado donde se abrió la cuenta. Esto ocurre porque el sistema bancario estadounidense ha pasado por muchas fusiones y adquisiciones a lo largo del tiempo, y muchas instituciones mantuvieron los códigos regionales que ya existían.

Por ejemplo, un banco grande como Bank of America puede tener un routing number distinto en Texas que en California. Incluso si el cliente se muda de estado, normalmente seguirá utilizando el routing correspondiente al lugar donde abrió su cuenta originalmente.

Por esta razón, cuando se intenta encontrar el routing correcto no basta con saber el banco del cliente. También es importante saber en qué estado se abrió la cuenta. Con esa información es posible hacer el lookup correcto y confirmar que el número coincide con el que aparece en la app bancaria o en un cheque del cliente.

---

### 4.1.4 Comparativa: ACH vs Wire vs tarjeta de débito

Cuando un cliente quiere depositar dinero en su cuenta de inversión, normalmente tiene tres opciones principales: ACH, transferencia wire o tarjeta de débito.

El **ACH** es el método más común porque tiene un costo muy bajo y permite automatizar depósitos fácilmente. Por esa razón es la opción preferida para depósitos recurrentes o para clientes que están construyendo su portafolio poco a poco.

Las **transferencias wire**, en cambio, son mucho más rápidas y el dinero puede llegar el mismo día. Sin embargo, suelen tener costos mucho más altos, por lo que normalmente se utilizan para montos grandes o cuando el cliente necesita que los fondos estén disponibles inmediatamente.

La **tarjeta de débito** permite que el dinero se refleje casi de inmediato en la cuenta del cliente, pero también implica costos mayores para la plataforma. Por esta razón suele utilizarse principalmente para primeros depósitos pequeños, cuando lo más importante es que el cliente vea el dinero reflejado rápidamente y tenga una buena primera experiencia con la plataforma.

En la práctica, la mayoría de los clientes termina utilizando ACH como método principal porque combina bajo costo, facilidad de uso y la posibilidad de automatizar depósitos a largo plazo.

## 4.2 Diseño del agente — Arquitectura y flujo conversacional

**Propósito:** guiar a clientes de Insights a través del proceso
completo de fondeo vía ACH, desde la recopilación de datos bancarios
hasta la confirmación de la instrucción, manejando errores y
escalamientos de forma autónoma.

### Estados del agente

| # | Estado | Responsabilidad | Transición |
|---|--------|-----------------|------------|
| 1 | GREETING | Identificar intención del cliente | Si menciona fondeo → COLLECT_BANK_STATE |
| 2 | COLLECT_BANK_STATE | Preguntar banco y estado antes que cualquier otra cosa | Datos recibidos → COLLECT_ACCOUNT_INFO |
| 3 | COLLECT_ACCOUNT_INFO | Recopilar número de cuenta, tipo y monto | Datos completos → ROUTING_LOOKUP |
| 4 | ROUTING_LOOKUP | Inferir routing, aplicar checksum, confirmar | Cliente confirma → INSTRUCTIONS |
| 5 | INSTRUCTIONS | Guiar paso a paso la autorización ACH | Cliente autoriza → CONFIRMATION |
| 6 | CONFIRMATION | Resumen completo antes de ejecutar | Cliente confirma → éxito / error |
| 7 | ERROR_HANDLING | Comunicar fallo con código Nacha y siguiente paso | Reintento o escalar → humano |

### Diagrama de flujo
```
Cliente inicia conversación
        ↓
[GREETING] — ¿En qué puedo ayudarte?
        ↓
¿Intención = fondeo ACH?
   NO → redirigir o escalar
   SÍ ↓
[COLLECT_BANK_STATE]
"¿Con qué banco y en qué estado tienes tu cuenta?"
        ↓
¿Hay memoria previa del cliente?
   SÍ → "Veo que usas {banco} en {estado}, ¿seguimos?"
   NO → recopilar desde cero
        ↓
[COLLECT_ACCOUNT_INFO]
— Número de cuenta
— Tipo: cheques o ahorros
— Monto a fondear
        ↓
[ROUTING_LOOKUP]
— Lookup banco + estado → routing number
— Validar checksum internamente
— Confirmar con cliente
        ↓
[INSTRUCTIONS] → paso a paso
        ↓
[CONFIRMATION] → resumen + confirmación explícita
        ↓
   ✅ Éxito → fondeo iniciado → guardar memoria
   ⚠️ R01  → fondos insuficientes → reintentar
   ❌ R03  → cuenta no encontrada → revisar datos
   ❓ Otro → escalar a asesor humano con historial
```

### Reglas de diseño

1. **Banco + estado siempre primero.** Sin excepción.
2. **Memoria entre sesiones.** Si el cliente ya fondeo, el agente
   recupera banco y estado y pregunta si desea usar la misma cuenta.
3. **Confirmación explícita antes de ejecutar.** El agente muestra
   un resumen completo y pide confirmación antes de procesar.
4. **Escalamiento con contexto.** Si el agente no puede resolver el
   fallo, escala a un asesor humano enviando el historial completo.
5. **Tono consistente.** Profesional y cercano. Los códigos Nacha
   son internos — el cliente recibe mensajes en lenguaje natural.

---

## 4.3 System prompt — El cerebro del agente

El system prompt completo está implementado en `agent.py` dentro de
la función `build_system_prompt()`. A continuación se documenta cada
sección y la razón de su inclusión.

### Secciones y justificación

| Sección | Contenido | Por qué está ahí |
|---------|-----------|-----------------|
| **Rol y nombre** | Sofia, asistente ACH de Insights WM | Define identidad consistente. Sin esto el LLM improvisa nombre y rol entre turnos |
| **Regla de idioma** | Detecta español/inglés y responde en el mismo | Los clientes de Insights son latinos en EE.UU. — la barrera de idioma no puede ser un obstáculo |
| **Tono** | Profesional, cercano, sin jerga técnica | Un cliente que recibe "ODFI" o "Nacha" en una respuesta pierde confianza |
| **Regla banco+estado primero** | Obligatoria antes de cualquier información | Previene dar routing incorrecto. Es también la regla más importante del enunciado |
| **Flujo ordenado** | 7 pasos secuenciales explícitos | Un LLM sin flujo explícito salta pasos. El orden es la columna vertebral del agente |
| **Routing table interna** | Tabla banco+estado → routing, nunca expuesta al cliente | El agente resuelve sin preguntar al cliente. Experiencia fluida |
| **Checksum interno** | Fórmula de validación ABA aplicada en silencio | Capa de protección que el cliente nunca ve pero que previene errores de tipeo |
| **Error handling por código** | Mensajes humanos para R01, R02, R03 y error desconocido | El cliente nunca ve códigos técnicos. Empatía primero, solución después |
| **Disclaimer** | Una vez por sesión antes de la confirmación final | Protección legal mínima. Estándar en cualquier producto fintech |
| **Memoria** | Instrucciones para usar y guardar datos del cliente | Reduce fricción en sesiones futuras |

### Ver system prompt

Ver archivo en System Prompt.md

También el system prompt completo está disponible en `agent.py`.

---

## 4.4 Implementación

Ver código completo en:
- `app.py` — Interfaz Streamlit
- `agent.py` — Integración Gemini API + system prompt
- `routing_table.py` — Tabla ABA + validación checksum
- `memory.py` — Persistencia entre sesiones


---


## 4.5 Demo y Reflexión

### Pruébalo tú mismo

Mejor que cualquier video, el agente está desplegado y disponible
ahora mismo. Puedes entrar, escribirle en español o en inglés, y
ver cómo responde en tiempo real. El sidebar tiene un selector que
te permite simular los tres escenarios sin configuración adicional.

👉 **[Abrir Sofia — ACH Funding Agent]([https://tuapp.streamlit.app](https://insights-investment-challenge-david-lizcano-123456789.streamlit.app/))**

---

### Transcripciones reales — 3 escenarios

#### Escenario 1 — Flujo exitoso (español)

Este fue el escenario más limpio. El cliente inició en español,
Sofia detectó el idioma correctamente y mantuvo el tono hasta
el final sin desviarse.

> **Sofia:** Bienvenido a Insights Wealth Management. Soy Sofía,
> tu asistente de fondeo. Estoy aquí para ayudarte a depositar
> fondos en tu cuenta de inversión vía transferencia ACH.
> ¿En qué puedo ayudarte hoy?

> **Cliente:** Hola, quiero fondear mi cuenta

> **Sofia:** ¡Hola! Con gusto te ayudaré. Para empezar, ¿podrías
> decirme el nombre de tu banco y el estado de EE. UU. donde
> abriste tu cuenta?

> **Cliente:** Bank of America, Texas

> **Sofia:** Excelente. ¿Podrías proporcionarme tu número de
> cuenta bancaria?

> **Cliente:** 123456789

> **Sofia:** ¿Es una cuenta de cheques o de ahorros?

> **Cliente:** Cheques, personal

> **Sofia:** ¿Qué cantidad en dólares deseas transferir?

> **Cliente:** 1000

> **Sofia:** El número de ruta para Bank of America en Texas es
> **111000025**. ¿Coincide con el que encuentras en tu chequera
> o app del banco?

> **Cliente:** Confirmo

> **Sofia:** *(instrucciones paso a paso + disclaimer)*
> ¿Te gustaría que resuma todo para confirmación final?

> **Cliente:** No, procede enseguida

> **Sofia:** Hemos iniciado la transferencia de $1,000 USD.
> Los fondos deberían estar disponibles en 1 a 3 días hábiles.

---

#### Escenario 2 — R01 Fondos insuficientes (inglés)

El cliente escribió en inglés y Sofia cambió de idioma
automáticamente. El routing fue identificado correctamente.
El error R01 fue comunicado con empatía y sin tecnicismos.
Vale notar que en esta sesión el agente se presentó como
"Alexa" en lugar de "Sofia" — una inconsistencia real que
se documenta en la reflexión.

> **Sofia:** Welcome to Insights Wealth Management. I'm here
> to help you fund your investment account via ACH.
> How can I help you today?

> **Cliente:** I want to fund my account

> **Sofia:** To get started, could you tell me your bank name
> and the US state where your account was opened?

> **Cliente:** Wells Fargo, California

> **Sofia:** *(recopila: 987654321, savings, personal, $5,000)*
> For Wells Fargo in California, the routing number is
> **121000248**. Does this match your checkbook or bank app?

> **Cliente:** yes it is

> **Sofia:** It looks like the transfer couldn't be completed
> due to insufficient funds in your account. Please check your
> balance and let me know when you're ready to retry. I can also
> help you set up a transfer for a smaller amount if needed.

---

#### Escenario 3 — R03 Cuenta no encontrada (español)

Este fue el escenario más interesante desde el punto de vista
técnico — y el más honesto para documentar. El agente manejó
el error R03 de forma incorrecta: en lugar de señalar que los
datos bancarios del cliente no coincidían con ningún registro,
interpretó el error como un problema con el número de cuenta de
Insights. Eso generó confusión y alargó innecesariamente la
conversación. El cliente terminó dando un número de cuenta de
inversión inventado, y el agente siguió adelante con él.

> **Sofia:** Bienvenido a Insights Wealth Management. Soy Sofía.
> ¿En qué puedo ayudarte hoy?

> **Cliente:** Necesito depositar dinero

> **Sofia:** ¿Cuál es tu banco y el estado donde abriste tu cuenta?

> **Cliente:** Chase, New York

> **Sofia:** *(recopila: 000111222, cheques, personal, $2,000)*
> El número de ruta para JPMorgan Chase en New York es **021000021**.
> ¿Coincide con el tuyo?

> **Cliente:** Si es

> **Sofia:** *(interpreta R03 como error en cuenta de Insights
> en lugar de error en cuenta bancaria del cliente)*
> Parece que hubo un problema al localizar tu cuenta de Insights.
> ¿Podrías verificar tu número de cuenta de inversión?

> **Cliente:** ah okay es 0456

> **Sofia:** *(acepta el número y continúa el flujo)*

> **Cliente:** si correcto

> **Sofia:** Lo siento, no pudimos localizar la cuenta de Insights
> con ese número. ¿Podrías revisarlo en un documento oficial?

---

### Reflexión

Construir este agente fue un ejercicio útil para entender dónde
