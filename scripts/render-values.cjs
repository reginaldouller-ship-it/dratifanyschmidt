// Evaluate only our local, versioned component's initial state; no browser/network.
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(process.argv[2], 'utf8');
const code = source.match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({ DCLogic: class {}, encodeURIComponent });
const values = vm.runInContext(code + '\nJSON.stringify(new Component().renderVals())', context, { timeout: 2000 });
process.stdout.write(values);
