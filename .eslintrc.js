module.exports = {
  env: {
    node: true,
    es2020: true,
  },
  extends: ['eslint:recommended'],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  rules: {
    'no-unused-vars': 'warn',
    'no-console': 'off',
    'prefer-const': 'error',
  },
  ignorePatterns: [
    'node_modules/', 
    'dist/',
    'scripts/data-processor.js',
    'scripts/api-payload-builder.js', 
    'scripts/conditional-router.js',
    'scripts/file-processor.js'
  ],
};
