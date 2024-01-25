import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('test elements on landing page', async ({ page }) => {
  await page.goto(url);

  await expect(page.locator('#title-header')).toContainText('Welcome to the SAEOSS Portal');

  await expect(page.getByRole('link', { name: 'METADATA', exact: true })).toBeVisible();

  await expect(page.getByRole('heading')).toContainText('Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision making.');

  await expect(page.getByText('Welcome to the SAEOSS Portal METADATA Discover a world of data-driven')).toBeVisible();

  await expect(page.locator('.social-inner').first()).toBeVisible();

  await expect(page.locator('.social-main > div:nth-child(2)')).toBeVisible();

  await expect(page.locator('.social-main > div:nth-child(3)')).toBeVisible();

  await expect(page.locator('div:nth-child(4)').first()).toBeVisible();

  await page.keyboard.press('PageDown');

  await expect(page.locator('div').filter({ hasText: 'Explore our metadata through' }).nth(3)).toBeVisible();

  await expect(page.locator('.img-card').first()).toBeVisible();

  await expect(page.locator('section')).toContainText('Explore our metadata through an interactive map viewer. Discover geographic data and availible metadata records displayed visually');

  await expect(page.getByRole('link', { name: 'Explore map' })).toBeVisible();

  await expect(page.locator('div').filter({ hasText: 'Search and filter through a' }).nth(3)).toBeVisible();

  await expect(page.locator('div:nth-child(2) > .card > .card-body > .img-card-main > .img-card')).toBeVisible();

  await expect(page.locator('section')).toContainText('Search and filter through a vast library of public records using different filter types to find the exact data you need quickly and efficiently.');

  await expect(page.getByRole('link', { name: 'Search' })).toBeVisible();

  await expect(page.locator('div').filter({ hasText: 'Browse through our' }).nth(3)).toBeVisible();

  await expect(page.locator('div:nth-child(3) > .card > .card-body > .img-card-main > .img-card')).toBeVisible();

  await expect(page.locator('section')).toContainText('Browse through our comprehensive metadata repository. Access detailed information about our data resources, making informed decisions for your projects. Your gateway to well-organized data.');

  await expect(page.getByRole('link', { name: 'Metadata Browser' })).toBeVisible();

  await expect(page.getByLabel('Open chat')).toBeVisible();

  await expect(page.locator('.navbar-brand')).toBeVisible();

  await expect(page.getByTestId('loggedin_user_icon')).toBeVisible();

  await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Metadata', exact: true })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Map', exact: true })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Organisations' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'About' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Help' })).toBeVisible();

  await page.locator('#home-carousel').getByRole('listitem').first().click();

  await page.locator('#home-carousel').getByRole('listitem').nth(1).click();

  await page.locator('#home-carousel').getByRole('listitem').nth(2).click();

});