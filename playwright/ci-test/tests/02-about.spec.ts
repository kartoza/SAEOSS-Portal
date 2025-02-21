import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test elements on about page', async ({ page }) => {
  await page.goto(url);

  await expect(page.getByText('Welcome to the SAEOSS Portal')).toBeVisible();

  await expect(page.getByRole('link', { name: 'METADATA', exact: true })).toBeVisible();

  await expect(page.getByRole('heading')).toContainText('Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision making.');

  await expect(page.getByTestId('loggedin_user_icon')).toBeVisible();

  await expect(page.getByLabel('Open chat')).toBeVisible();

  await page.getByRole('link', { name: 'About' }).click();

  await expect(page.locator('#title-header')).toContainText('The SAEOSS-Portal is the result of a pioneering collaboration between SANSA (South African National Space Agency) and SAEON (South African Earth Observation Network). United by a common vision, the SAEOSS-Portal platform was conceived to revolutionize data sharing among diverse entities, fostering synergy and knowledge exchange.');

  await expect(page.locator('.social-inner').first()).toBeVisible();

  await expect(page.locator('.social-main > div:nth-child(2)')).toBeVisible();

  await expect(page.locator('.social-main > div:nth-child(3)')).toBeVisible();

  await expect(page.getByRole('heading', { name: 'Our Vision' })).toBeVisible();

  await expect(page.getByRole('img', { name: 'https://www.freepik.com/free-' })).toBeVisible({timeout: 20000});

  await expect(page.getByText('At the SAEOSS-Portal, we')).toBeVisible();

  await expect(page.locator('.blue-hr')).toBeVisible();

  await expect(page.getByRole('heading', { name: 'Join the Data Revolution' })).toBeVisible();

  await expect(page.getByText('We invite organizations,')).toBeVisible();

  await expect(page.locator('div:nth-child(2) > div > img')).toBeVisible();

  await expect(page.getByLabel('Open chat')).toBeVisible();
  
});