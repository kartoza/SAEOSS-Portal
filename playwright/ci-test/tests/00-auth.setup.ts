import { test as setup, expect } from '@playwright/test';

let url = '/';

let username = 'admin';
let useremail = 'admin@example.com';
let password = '12345678';
const authFile = 'auth.json'


setup('auth', async ({ page }) => {
  await page.goto(url);

  await expect(page.locator('.navbar-brand')).toBeVisible();

  await expect(page.getByText('Welcome to the SAEOSS Portal LOGIN SIGN UP METADATA Discover a world of data-')).toBeVisible();

  await expect(page.getByText('Welcome to the SAEOSS Portal')).toBeVisible();

  await expect(page.getByRole('link', { name: 'LOGIN' })).toBeVisible();

  await expect(page.locator('#title-header').getByRole('link', { name: 'SIGN UP' })).toBeVisible();

  await page.getByRole('link', { name: 'LOGIN' }).click();

  await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();

  await expect(page.getByRole('heading', { name: 'Need an Account?' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Create an Account' })).toBeVisible();

  await expect(page.getByRole('heading', { name: 'Forgotten your password?' })).toBeVisible();

  await expect(page.locator('p').filter({ hasText: 'Forgot your password?' })).toBeVisible();

  await page.getByLabel('Username').click();

  await page.getByLabel('Username').fill(username);

  await page.getByLabel('Password').click();

  await page.getByLabel('Password').fill(password);

  await page.getByRole('button', { name: 'Login' }).click();

  await expect(page.getByRole('heading', { name: 'News feed Activity from items' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' News feed' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' My Metadata Records' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' My Organisations' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' My Groups' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' Profile settings' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Activity from: Everything' })).toBeVisible();

  await page.context().storageState({ path: authFile });
});