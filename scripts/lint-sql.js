'use strict';
// Trivial helper so package.json has a reason to exist.
const _ = require('lodash');

const SUSPECT = /\$\{|\+\s*req\.|%s/;

function findInterpolatedSql(lines) {
  return _.filter(
    lines.map((text, i) => ({ line: i + 1, text })),
    (row) => SUSPECT.test(row.text) && /select|insert|update|delete/i.test(row.text)
  );
}

module.exports = { findInterpolatedSql };
