// Produce a SHA-1 hash for each password in a file. Uses the sha1.js file from
// RingZer0 CTF challenge #30.
//
// Usage:
//    node hash_password_file.js <target_hash> <filename>
//    node hash_password_file.js b89356ff6151527e89c4f3e3d30c8e6586c63962 /usr/share/dict/words
//

const fs = require("fs");
const path = require("path");
const readline = require("readline");

const Sha1 = require("./sha1.js");

// The two parameters that are read from the command line.
const targetHash = process.argv[2];
const filename = process.argv[3];

// Check that the parameters were provided, and exit if not.
if (!targetHash || !filename) {
  const scriptName = path.basename(process.argv[1]);
  console.error(`Usage: node ${scriptName} <target_hash> <filename>`);
  process.exit(1);
}

// Create a read stream and line reader.
const rl = readline.createInterface({
  input: fs.createReadStream(filename),
  crlfDelay: Infinity,
});

// Process each line from the file.
rl.on("line", (line) => {
  const word = line.trim();
  const hash = Sha1.hash(word);

  if (hash.toLowerCase() === targetHash.toLowerCase()) {
    console.log(`✅ Match found: "${word}" → ${hash}`);
    rl.close();
  }
});
