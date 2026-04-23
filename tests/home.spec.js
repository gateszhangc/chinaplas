const { test, expect } = require("@playwright/test");

test.describe("CHINAPLAS guide static site", () => {
  test("homepage renders core CHINAPLAS guide content and SEO tags", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/CHINAPLAS 2026 参观指南/);
    await expect(page.locator("h1")).toHaveText("CHINAPLAS 2026 参观指南");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /非官方/);
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", "index,follow,max-image-preview:large");
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://chinaplas.lol/");
    await expect(page.locator('link[rel="manifest"]')).toHaveAttribute("href", "site.webmanifest");
    await expect(page.locator('meta[property="og:locale"]')).toHaveAttribute("content", "zh_CN");

    await expect(page.getByText("本站不是 CHINAPLAS 官方网站")).toBeVisible();
    await expect(page.locator(".hero-meta").getByText("最近核对")).toBeVisible();
    await expect(page.locator(".hero-meta").getByText("2026 年 4 月 23 日", { exact: true })).toBeVisible();
    await expect(page.getByText("2026.4.21 - 24")).toBeVisible();
    await expect(page.locator(".quick-facts dd", { hasText: "上海虹桥国家会展中心" })).toBeVisible();
    await expect(page.getByText("390,000+")).toBeVisible();
    await expect(page.getByText("5,000+")).toBeVisible();
    await expect(page.getByText("320,000+")).toBeVisible();

    const officialLink = page.getByRole("link", { name: "查看官方参观信息" });
    await expect(officialLink).toHaveAttribute("href", /chinaplasonline\.com\/cps\/visitor\/visiting-information/);

    const themeCards = page.locator(".theme-grid article");
    await expect(themeCards).toHaveCount(4);

    const html = await page.content();
    expect(html).not.toContain("googletagmanager.com");
    expect(html).not.toContain("clarity.ms");

    const structuredData = await page.locator('script[type="application/ld+json"]').allTextContents();
    const pageGraph = JSON.parse(structuredData[0]);
    const webPageNode = pageGraph["@graph"].find((node) => node["@type"] === "WebPage");
    const eventNode = pageGraph["@graph"].find((node) => node["@type"] === "Event");

    expect(webPageNode.dateModified).toBe("2026-04-23");
    expect(eventNode.name).toBe("CHINAPLAS 2026");

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("navigation anchors and FAQ remain usable", async ({ page }) => {
    await page.goto("/");

    await page.locator(".nav").getByRole("link", { name: "重点主题", exact: true }).click();
    await expect(page.locator("#themes")).toBeInViewport();
    await expect(page.getByRole("heading", { name: "用四个主题判断是否值得到场。" })).toBeVisible();

    await page.locator(".nav").getByRole("link", { name: "FAQ", exact: true }).click();
    await expect(page.locator("#faq")).toBeInViewport();

    const ticketQuestion = page.getByText("可以在这里完成预登记或购票吗？");
    await ticketQuestion.click();
    await expect(page.getByText("登记、购票、展商后台、媒体订阅等操作都应在 CHINAPLAS 官方网站完成。")).toBeVisible();

    const freshnessQuestion = page.getByText("页面信息多久更新？");
    await freshnessQuestion.click();
    await expect(page.getByText("Google Search Console", { exact: false })).toBeVisible();
  });

  test("mobile layout stays within viewport", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    await expect(page.getByRole("link", { name: "查看官方参观信息" })).toBeVisible();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);

    await page.locator(".nav").getByRole("link", { name: "展会规模", exact: true }).click();
    await expect(page.locator("#scale")).toBeInViewport();
  });
});
