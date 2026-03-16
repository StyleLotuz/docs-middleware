const express = require('express');
const jwt = require('jsonwebtoken');
const { buildLegacyResponse, buildTaxeableResponse } = require('./factories');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

const BASIC_AUTH_USERNAME = process.env.BASIC_AUTH_USERNAME || 'legacy_user';
const BASIC_AUTH_PASSWORD = process.env.BASIC_AUTH_PASSWORD || 'legacy_pass';
const JWT_SECRET = process.env.JWT_SECRET || 'mock-jwt-secret';
const JWT_ISSUER = process.env.JWT_ISSUER || 'middleware-mock';
const JWT_AUDIENCE = process.env.JWT_AUDIENCE || 'taxeable-api';

function parseBasicAuth(header) {
  if (!header || !header.startsWith('Basic ')) return null;
  const base64 = header.slice(6);
  const decoded = Buffer.from(base64, 'base64').toString('utf8');
  const [username, password] = decoded.split(':');
  return { username, password };
}

function parseBearerToken(header) {
  if (!header || !header.startsWith('Bearer ')) return null;
  return header.slice(7);
}

app.post('/legacy', (req, res) => {
  const auth = parseBasicAuth(req.headers.authorization);

  if (!auth || auth.username !== BASIC_AUTH_USERNAME || auth.password !== BASIC_AUTH_PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized', message: 'Invalid Basic Auth credentials' });
  }

  const response = buildLegacyResponse(req.body);
  res.status(200).json(response);
});

app.post('/taxeable', (req, res) => {
  const token = parseBearerToken(req.headers.authorization);

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized', message: 'Missing or invalid Bearer token' });
  }

  try {
    jwt.verify(token, JWT_SECRET, {
      issuer: JWT_ISSUER,
      audience: JWT_AUDIENCE,
    });
  } catch (err) {
    return res.status(401).json({ error: 'Unauthorized', message: 'Invalid JWT', details: err.message });
  }

  const body = req.body.document ? req.body : { document: req.body };
  const response = buildTaxeableResponse(body);
  res.status(200).json(response);
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'middleware-mock' });
});

app.listen(PORT, () => {
  console.log(`Mock server running on http://localhost:${PORT}`);
  console.log('  POST /legacy   - Basic Auth');
  console.log('  POST /taxeable - Bearer JWT');
});
