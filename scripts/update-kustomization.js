const fs = require("fs");

const [filePath, imageName, imageTag] = process.argv.slice(2);

if (!filePath || !imageName || !imageTag) {
  console.error("Usage: node scripts/update-kustomization.js <file> <image-name> <image-tag>");
  process.exit(1);
}

let content = fs.readFileSync(filePath, "utf8");

if (!/(^\s*newName:\s*).+$/m.test(content) || !/(^\s*newTag:\s*).+$/m.test(content)) {
  console.error(`Expected ${filePath} to contain images.newName and images.newTag.`);
  process.exit(1);
}

content = content.replace(/(^\s*newName:\s*).+$/m, `$1${imageName}`);
content = content.replace(/(^\s*newTag:\s*).+$/m, `$1${imageTag}`);

fs.writeFileSync(filePath, content);
