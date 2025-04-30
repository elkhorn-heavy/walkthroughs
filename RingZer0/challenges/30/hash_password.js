// Produce a SHA-1 hash for a given password. Uses the sha1.js file used by
// RingZer0 CTF challenge #30.
//
// Usage:
//    node hash_password.js <target_hash> <text_to_hash>
//    node hash_password.js b89356ff6151527e89c4f3e3d30c8e6586c63962 pencil
//

const path = require("path");

const Sha1 = require("./sha1.js");

// The two parameters that are read from the command line.
const targetHash = process.argv[2];
const input = process.argv[3];

// Check that the parameters were provided, and exit if not.
if (!targetHash || !input) {
  const scriptName = path.basename(process.argv[1]);
  console.error(`Usage: node ${scriptName} <target_hash> <text_to_hash>`);

  process.exit(1);
}

// The real work: compute the hash for the user input.
const computedHash = Sha1.hash(input);

console.log(`Input:       ${input}`);
console.log(`Input Hash:  ${computedHash}`);
console.log(`Target Hash: ${targetHash}`);

// Check if the hash matches - this is less error prone than having a human look
// at the hashes.
if (computedHash.toLowerCase() === targetHash.toLowerCase()) {
  console.log("✅ Match!");
} else {
  console.log("❌ No match.");
}
