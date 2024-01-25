import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('create organisation', async ({ page }) => {
  await page.goto(url);

  await expect(page.locator('#title-header')).toContainText('Welcome to the SAEOSS Portal');

  await expect(page.getByRole('link', { name: 'METADATA', exact: true })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Organisations' })).toBeVisible();

  await page.getByRole('link', { name: 'Organisations' }).click();

  await expect(page.getByRole('link', { name: ' Add Organisation' })).toBeVisible();

  await expect(page.getByRole('heading', { name: ' What are Organisations?' })).toBeVisible();

  await expect(page.getByRole('complementary')).toContainText('CKAN Organisations are used to create, manage and publish collections of datasets. Users can have different roles within an Organisation, depending on their level of authorisation to create, edit and publish.');

  await expect(page.getByPlaceholder('Search organisations...')).toBeEmpty();

  await page.getByRole('link', { name: ' Add Organisation' }).click();

  await expect(page.getByRole('heading', { name: 'Create an Organization' })).toBeVisible();

  await page.getByPlaceholder('My Organization', { exact: true }).click();

  await page.getByPlaceholder('My Organization', { exact: true }).fill('Test');

  await page.waitForTimeout(5000);

  await page.getByPlaceholder('A little information about my').click();

  await page.getByPlaceholder('A little information about my').fill('This is a test organisation.');

  await expect(page.getByRole('button', { name: 'Create Organization' })).toBeEnabled();

  await page.getByRole('button', { name: 'Create Organization' }).click();

  await expect(page.getByRole('heading', { name: 'Test' })).toBeVisible();

  await expect(page.getByRole('complementary')).toContainText('This is a test organisation.');

  await expect(page.getByRole('link', { name: ' Follow' })).toBeVisible();

  await expect(page.getByRole('button', { name: ' Organisations ' })).toBeVisible();

  await expect(page.getByRole('heading', { name: ' Tags ' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' Metadata Records' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' Activity Stream' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' About' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' Manage' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' Add metadata record' })).toBeVisible();

});