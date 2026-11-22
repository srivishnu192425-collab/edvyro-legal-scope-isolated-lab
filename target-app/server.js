/**
 * OWASP Juice Shop / DVWA Emulated Practice Target
 * Task 02: Legal Scope and Isolated Lab
 * 
 * IMPORTANT ISOLATION CONSTRAINT:
 * This server binds strictly to the loopback interface (127.0.0.1).
 * It will NOT accept connections from external or public network interfaces.
 */

const http = require('http');
const url = require('url');

const HOST = '127.0.0.1'; // Strictly loopback - isolated from public network
const PORT = 3000;

// Mock database for educational lab testing
const products = [
  { id: 1, name: 'Apple Juice (1000ml)', category: 'Beverage', price: 1.99, description: 'The all-time classic.' },
  { id: 2, name: 'Orange Juice (1000ml)', category: 'Beverage', price: 2.49, description: 'Freshly squeezed citrus goodness.' },
  { id: 3, name: 'OWASP Juice Shop Iron-On Patch', category: 'Merchandise', price: 4.99, description: 'Show your security pride!' },
  { id: 4, name: 'Raspberry Juice (1000ml)', category: 'Beverage', price: 3.99, description: 'Tart and delicious.' }
];

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const clientIp = req.socket.remoteAddress;
  const timestamp = new Date().toISOString();

  console.log(`[${timestamp}] Incoming Request: ${req.method} ${parsedUrl.pathname} from ${clientIp}`);

  // Set security and CORS headers restricting to localhost
  res.setHeader('X-Lab-Environment', 'Isolated-Security-Testing');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:3000');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Root / Healthcheck
  if (parsedUrl.pathname === '/' || parsedUrl.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ONLINE',
      target: 'OWASP Juice Shop / DVWA Emulated Lab',
      binding: `${HOST}:${PORT}`,
      network_isolation: 'STRICT_LOOPBACK_ONLY',
      external_access: 'BLOCKED',
      authorized_scope: `http://${HOST}:${PORT}`,
      timestamp: timestamp,
      endpoints: [
        'GET  /',
        'GET  /health',
        'GET  /api/products',
        'GET  /api/search?q=<query>',
        'POST /api/login'
      ]
    }, null, 2));
    return;
  }

  // Product listing
  if (parsedUrl.pathname === '/api/products' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ success: true, count: products.length, data: products }, null, 2));
    return;
  }

  // Search endpoint (simulating vulnerable search for testing)
  if (parsedUrl.pathname === '/api/search' && req.method === 'GET') {
    const q = (parsedUrl.query.q || '').toLowerCase();
    const results = products.filter(p => p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q));
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      query: parsedUrl.query.q || '',
      matchCount: results.length,
      results: results,
      note: 'Target for authorized input validation testing within local scope only.'
    }, null, 2));
    return;
  }

  // Mock Authentication endpoint
  if (parsedUrl.pathname === '/api/login' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const creds = JSON.parse(body || '{}');
        if (creds.email === 'admin@juice-sh.op' && creds.password === 'admin123') {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: true, token: 'mock-jwt-token-lab-scope-only', role: 'admin' }));
        } else {
          res.writeHead(401, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, message: 'Invalid credentials in lab database.' }));
        }
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: 'Malformed JSON payload' }));
      }
    });
    return;
  }

  // Default 404
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Route not found', scope_violation_check: 'Request within 127.0.0.1 boundaries' }));
});

server.listen(PORT, HOST, () => {
  console.log('================================================================');
  console.log('   ISOLATED PRACTICE LAB TARGET - SECURITY ENVIRONMENT ACTIVE   ');
  console.log('================================================================');
  console.log(`[TARGET STATUS] Server successfully running at http://${HOST}:${PORT}/`);
  console.log(`[INTERFACE]     Bound strictly to: ${HOST} (Loopback Only)`);
  console.log(`[SECURITY]      Public / External Network interfaces REJECTED`);
  console.log(`[RULES OF ENG.] Only http://${HOST}:${PORT} is authorized for testing.`);
  console.log('================================================================');
});
