const fs = require('fs');
const path = require('path');

const root = __dirname;
const out = path.join(root, 'dist');

fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
fs.copyFileSync(path.join(root, 'CISSP_Study_Portal.html'), path.join(out, 'index.html'));
fs.copyFileSync(path.join(root, 'CISSP_Study_Portal.html'), path.join(out, 'CISSP_Study_Portal.html'));
fs.copyFileSync(path.join(root, 'cissp-data.js'), path.join(out, 'cissp-data.js'));
fs.cpSync(path.join(root, 'public'), out, { recursive: true });

console.log(`Static PWA built in ${out}`);
