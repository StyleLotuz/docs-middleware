  # Prueba Técnica Take-Home - Middleware de Integración

## Contexto

En Finnecto integramos con distintos sistemas externos para procesar facturas. Algunos son sistemas legacy (antiguos) y otros son APIs modernas. Necesitamos un **middleware** que:

- Reciba requests con credenciales y un payload
- Transforme el payload según el tipo de sistema destino
- Se autentique de forma distinta según el sistema (Basic Auth vs JWT)
- Envíe los datos al sistema destino
- Estandarice la respuesta al formato original

El objetivo es evaluar tu capacidad para **decodificar auth, transformar datos, manejar distintos métodos de autenticación y reenviar requests**.

---

## Qué debes hacer

Debes implementar una **API** que pueda ser consumida (por ejemplo vía HTTP). La API puede estar desarrollada en **el lenguaje o stack que prefieras** (Node, Python, Go, etc.), pero debe **cumplir con los parámetros y el flujo descritos abajo**: recepción de JWT y body, transformación según tipo de conexión, autenticación ante el sistema destino y respuesta estandarizada.

---

## Configuración mínima del middleware

Tu implementación debe considerar estas variables de entorno mínimas:

| Variable | Descripción | Valor de ejemplo |
|----------|-------------|------------------|
| `MOCK_SERVER_URL` | Base URL del sistema destino mock | `http://localhost:3000` |
| `JWT_DECODE_SECRET` | Secret para decodificar/verificar el JWT entrante | `incoming-jwt-dev-secret` |

Para esta prueba, asume que los requests transformados se envían al mock:

- `POST ${MOCK_SERVER_URL}/legacy`
- `POST ${MOCK_SERVER_URL}/taxeable`

---

## Objetivo

Tu API debe:

1. Recibir un request con **JWT en el header `Authorization: Bearer <token>`** y un **body** con la estructura definida abajo
2. Decodificar el JWT y extraer: `connection_type`, `username`, `password` (y `secret` si es taxeable)
3. Transformar el body según `connection_type` al formato correspondiente (legacy o taxeable)
4. Si es `legacy`: calcular IVA del 19% en cada línea, actualizar el amount de cada línea y el total de la cabecera
5. Autenticarse ante el sistema destino (ambos via header `Authorization`):
   - **legacy** → Basic Auth (username + password)
   - **taxeable** → JWT (debes **generar** el token usando el `secret` del JWT entrante)
6. Enviar el body transformado al endpoint destino
7. Transformar la respuesta recibida de vuelta al formato original de entrada.

---

## Auth: JWT de entrada

El JWT contendrá al menos 3 claims base:

| Claim             | Valores posibles | Descripción                    |
|-------------------|------------------|--------------------------------|
| `connection_type` | `"legacy"` \| `"taxeable"` | Tipo de sistema destino        |
| `username`        | string           | Usuario para autenticación     |
| `password`        | string           | Contraseña para autenticación  |

Si `connection_type` es `"taxeable"`, el JWT incluirá además un claim `secret` que debes extraer para **generar** el token con el que te autenticarás ante el sistema destino.

Usa `JWT_DECODE_SECRET=incoming-jwt-dev-secret` para decodificar/verificar el JWT entrante.

### JWTs de ejemplo (entrada)

**Token legacy (ejemplo):**

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb25uZWN0aW9uX3R5cGUiOiJsZWdhY3kiLCJ1c2VybmFtZSI6ImxlZ2FjeV91c2VyIiwicGFzc3dvcmQiOiJsZWdhY3lfcGFzcyIsImlhdCI6MTc3MzE3Mjg2NywiZXhwIjoxNzczMjE2MDY3fQ.rxCeukk3IILqoaskPgs-LiesUenSmemfsUTzBmqJadQ
```

**Token taxeable (ejemplo):**

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb25uZWN0aW9uX3R5cGUiOiJ0YXhlYWJsZSIsInVzZXJuYW1lIjoidGF4X3VzZXIiLCJwYXNzd29yZCI6InRheF9wYXNzIiwic2VjcmV0IjoibW9jay1qd3Qtc2VjcmV0IiwiaWF0IjoxNzczMTcyODY3LCJleHAiOjE3NzMyMTYwNjd9.njAgitf4ftbrKA6aG2i_8HqtEXxecHEiRE5vjOYqCHM
```

---

## Body de entrada (formato estándar)

```json
{
  "number": "FNCT0006",
  "reception_date": "2026-03-03",
  "due_date": "2026-03-20",
  "currency": "COP",
  "total": 780000,
  "items": [
    {
      "description": "Corral Supergiftcard Digital Saldo 30.000",
      "unit_price": 30000,
      "total": 390000,
      "account": "VISTA"
    },
    {
      "description": "Corral Supergiftcard Digital Saldo 30.000",
      "unit_price": 30000,
      "total": 390000,
      "account": "CORRIENTE"
    }
  ]
}
```

---

## Formatos de transformación

### Formato Legacy (cuando `connection_type` = `"legacy"`)

- snake_case, nombres abreviados
- Estructura plana

```json
{
  "invoice_number": "FNCT0006",
  "recv_date": "2026-03-03",
  "expiry_date": "2026-03-20",
  "curr": "COP",
  "gross_total": 780000,
  "lines": [
    {
      "desc": "Corral Supergiftcard Digital Saldo 30.000",
      "unit_price": 30000,
      "line_total": 390000,
      "acct": "VISTA"
    },
    {
      "desc": "Corral Supergiftcard Digital Saldo 30.000",
      "unit_price": 30000,
      "line_total": 390000,
      "acct": "CORRIENTE"
    }
  ]
}
```

**Adicional para legacy**:
- Aplicar IVA del 19% sobre cada línea
- Actualizar `line_total` de cada línea (o `amount`, si usas ese nombre interno)
- Recalcular el total de cabecera (`gross_total`) con los valores con IVA
- No modificar `unit_price`

### Formato Taxeable (cuando `connection_type` = `"taxeable"`)

- camelCase
- Estructura anidada

```json
{
  "document": {
    "reference": "FNCT0006",
    "dates": {
      "reception": "2026-03-03",
      "due": "2026-03-20"
    },
    "currency": "COP",
    "total": 780000,
    "items": [
      {
        "description": "Corral Supergiftcard Digital Saldo 30.000",
        "unitPrice": 30000,
        "amount": 390000,
        "account": "VISTA"
      },
      {
        "description": "Corral Supergiftcard Digital Saldo 30.000",
        "unitPrice": 30000,
        "amount": 390000,
        "account": "CORRIENTE"
      }
    ]
  }
}
```

---

## Autenticación al enviar

Ambos métodos se envían mediante el header `Authorization`:

| connection_type | Método        | Cómo                          |
|-----------------|---------------|-------------------------------|
| `legacy`        | Basic Auth    | `Authorization: Basic base64(username:password)` |
| `taxeable`      | JWT           | `Authorization: Bearer <token>`. Genera el JWT con el `secret` extraído del token entrante. Incluye al menos `iss`, `aud`, `exp` |

Al generar el JWT para `taxeable`, usa estos valores para que el mock lo acepte:
- `iss: "middleware-mock"`
- `aud: "taxeable-api"`

---

## Respuesta

Una vez recibida la respuesta del sistema destino, transformarla de vuelta al **formato estándar de entrada** (number, reception_date, due_date, currency, total, items).

---

## Contrato mínimo de errores

Tu API debe manejar al menos estos casos:

| Código | Cuándo aplica | Respuesta mínima esperada |
|--------|----------------|---------------------------|
| `400` | Payload de entrada inválido (tipos/estructura incorrecta) | Mensaje simple indicando payload inválido |
| `401` | JWT entrante inválido o autenticación inválida | Mensaje simple de no autorizado |
| `502` | Falla al invocar el sistema destino (mock caído, timeout o error de red) | Mensaje simple de error de integración |

No es necesario usar un esquema complejo de errores para esta prueba.

---

## Formato de entrega

- Código del middleware
- Un **MD** con:
  - Happy path (flujo completo paso a paso)
  - Preguntas que hiciste durante el desarrollo (si las hubo)
  - Supuestos que tomaste

---

## Mock Server

Incluimos un servidor mock en `mock-server/` para que puedas probar tu middleware. Tiene su propio `docker-compose.yml`.

### Variables de entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `BASIC_AUTH_USERNAME` | Usuario para Basic Auth (/legacy) | `legacy_user` |
| `BASIC_AUTH_PASSWORD` | Contraseña para Basic Auth (/legacy) | `legacy_pass` |
| `JWT_SECRET` | Secret para validar JWT (/taxeable) | `mock-jwt-secret` |
| `JWT_ISSUER` | Issuer esperado en el JWT | `middleware-mock` |
| `JWT_AUDIENCE` | Audience esperado en el JWT | `taxeable-api` |

Revisa `mock-server/.env.example` para obtener o actualizar las variables.

### Ejecución

```bash
cd docs-middleware/mock-server
docker-compose up --build
```

**Sin Docker:**

```bash
cd mock-server && npm install && npm start
```

### Verificar

```bash
curl http://localhost:3000/health
```

### Endpoints

| Método | Ruta        | Auth       | Body             |
|--------|-------------|------------|------------------|
| POST   | `/legacy`   | Basic Auth | Formato legacy   |
| POST   | `/taxeable` | Bearer JWT | Formato taxeable |
| GET    | `/health`   | —----------| —----------------|

Credenciales por defecto: Basic Auth `legacy_user` / `legacy_pass`; JWT firmado con `JWT_SECRET`, `JWT_ISSUER`, `JWT_AUDIENCE`.

---

## Notas

- Si algo no está claro, **pregunta**. No hay penalización por hacer preguntas.
- Puedes usar el stack que prefieras (Node, Python, etc.).
