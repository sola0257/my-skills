// Playwright Codegen Recording: Data Analysis Workflow
// 录制时间: 2026-02-05
// 用途: 抓取文章统计数据

import { test, expect } from '@playwright/test';

test('data_analysis_workflow', async ({ page }) => {
  // 1. 导航到数据分析页面
  await page.goto('https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1631605521');
  await page.locator('.weui-desktop-menu__item.weui-desktop-menu_statistics > span > .menu-folder').click();
  await page.getByRole('link', { name: '内容分析' }).click();

  // 2. 选择时间范围
  await page.getByText('数据时间').first().click();
  await page.getByText('最近 30 天').click();

  // 3. 下载数据明细
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('link', { name: '下载数据明细' }).click();
  const download = await downloadPromise;

  // 下载的文件包含:
  // - 文章标题
  // - 发布时间
  // - 阅读数
  // - 分享数
  // - 收藏数
  // - 点赞数
  // - 评论数
  // - 等等...
});
