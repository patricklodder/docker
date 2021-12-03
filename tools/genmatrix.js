'use strict';
const path = require('path');
const fs = require('fs');

const CI_FILES = [
  ".github/workflows/build-ci.yml",
  "tools/genmatrix.js"
];

const VERSION_DIR_RE=/^\d+\.\d+\.\d+$/;

const readVersions = (baseDir) =>
  fs.readdirSync(baseDir, { withFileTypes: true })
    .filter(f => f.isDirectory() && f.name.match(VERSION_DIR_RE))
    .map(f => f.name);

const readVariants = (baseDir) =>
  fs.readdirSync(baseDir, { withFileTypes: true })
    .filter(f => f.isDirectory())
    .map(f => f.name);

const readPlatforms = (baseDir) => {
  const platformFile = path.resolve(baseDir, "PLATFORMS");
  return fs.readFileSync(platformFile).toString("utf-8")
         .split("\n").slice(0,-1);
}

const filterVariants = (version, variants, changedFiles) => variants.filter(variant => {

  const relPath = path.resolve(version, variant);
  const matchRegex = new Regex(relPath);
  return changedFiles.some(f => f.match(matchRegex));

});

const generateMatrix = (baseDir, changedFiles) => {

  const ciHasChanged = CI_FILES.some(f => changedFiles.indexOf(f) !== -1);

  if (ciHasChanged) console.log("CI HAS CHANGED! RUNNING ALL BUILDS!");

  const matrix = readVersions(baseDir)
    .map(version => [version, readVariants(path.resolve(baseDir,version))])
    .reduce((out, entry) => {
      const [version, variants] = entry;

      // If the CI has changed, test all builds, otherwise, just build what's changed
      const filteredVariants = ciHasChanged ? variants : filterVariants(version, variants, changedFiles);

      filteredVariants.forEach(variant => {

        const platforms = readPlatforms(path.resolve(baseDir, version, variant));
        platforms.forEach(platform => out.push({ version, variant, platform }));

      });

      return out;
    }, []);

  console.log("BUILD LIST: \n" + matrix.map(o => Object.values(o).join(", ")).join("\n"));

  return matrix.length ? { include: matrix } : null;
}

module.exports = generateMatrix;
