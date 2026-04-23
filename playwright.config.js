const { defineConfig, devices } = require("@playwright/test");

const externalBaseUrl = process.env.PLAYWRIGHT_BASE_URL;

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30_000,
  expect: {
    timeout: 5_000
  },
  use: {
    baseURL: externalBaseUrl || "http://127.0.0.1:4174",
    trace: "on-first-retry"
  },
  projects: [
    {
      name: "chromium-desktop",
      use: { ...devices["Desktop Chrome"] }
    },
    {
      name: "chromium-mobile",
      use: { ...devices["Pixel 7"] }
    }
  ],
  webServer: externalBaseUrl
    ? undefined
    : {
        command: "PORT=4174 node server.js",
        url: "http://127.0.0.1:4174",
        reuseExistingServer: false,
        timeout: 120_000
      }
});
