// Playwright Codegen Recording: Collections Workflow
// 录制时间: 2026-02-05
// 用途: 抓取文章合集信息

import { test, expect } from '@playwright/test';

test('collections_workflow', async ({ page }) => {
  // 1. 导航到合集页面
  await page.goto('https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1631605521');
  await page.getByText('内容管理').click();
  await page.getByRole('link', { name: '合集' }).click();

  // 2. 查看合集列表
  // 页面显示的合集包括:
  const collections = [
    '绿植软装',
    '欣赏',
    '节气与绿植',
    '年宵花',
    '养护技巧',
    '修剪整形',
    '城市绿洲',
    '知识分享',
    '阳台种植',
    '#智能园艺'
  ];

  // 3. 提取合集信息
  // 可以通过以下选择器获取:
  // await page.getByRole('table').getByText('绿植软装')
  // await page.getByRole('table').getByText('欣赏')
  // ... 等等
});
