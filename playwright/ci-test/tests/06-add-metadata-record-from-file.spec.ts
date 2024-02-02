import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test.describe('add metadata record from file', () => {
  test.beforeEach(async ({ page }) => {
    // Go to the starting url before each test.
    await page.goto(url);
  });

  test('XML', async ({ page }) => {

    await expect(page.getByText('Welcome to the SAEOSS Portal METADATA Discover a world of data-driven')).toBeVisible();

    await expect(page.locator('#title-header')).toContainText('Welcome to the SAEOSS Portal');

    await expect(page.getByRole('link', { name: 'METADATA', exact: true })).toBeVisible();

    await expect(page.getByRole('heading')).toContainText('Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision making.');

    await expect(page.locator('.navbar-brand')).toBeVisible();

    await expect(page.getByTestId('loggedin_user_icon')).toBeVisible();

    await page.getByRole('link', { name: 'METADATA', exact: true }).click();

    await page.waitForURL('**/dataset/');

    await expect(page.getByRole('heading', { name: 'Metadata', exact: true })).toBeVisible();

    await expect(page.getByRole('link', { name: 'Add metadata record' })).toBeVisible();

    await expect(page.getByRole('button', { name: ' Add metadata record from' })).toBeVisible();

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByRole('button', { name: ' Add metadata record from' }).click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/SANS1878.xml');

    await page.waitForLoadState('load');

    await expect(page.getByText('all packages were created×')).toBeVisible();

    await page.getByRole('link', { name: '×' }).click();

    await page.reload();

    await expect(page.getByRole('heading', { name: 'Metadata', exact: true })).toBeVisible();

    await expect(page.getByLabel('Breadcrumb').getByRole('list')).toContainText('3 metadata records found');

    await expect(page.locator('li').filter({ hasText: 'test xml Abstract from the' })).toBeVisible();

    await page.locator('#content div').filter({ hasText: 'test xml Abstract from the' }).nth(2).click();

    await page.getByRole('link', { name: 'test xml' }).click();

    await expect(page.getByRole('heading', { name: 'test xml' })).toBeVisible();

    await expect(page.getByRole('heading', { name: 'Dataset extent' })).toBeVisible();

    await expect(page.getByRole('link', { name: ' Manage' })).toBeVisible();

    await page.getByRole('link', { name: ' Groups' }).click();

    await page.getByRole('link', { name: ' Activity Stream' }).click();

    await expect(page.getByText('admin created the metadata')).toBeVisible();

    await page.getByRole('link', { name: 'Metadata', exact: true }).first().click();

    await expect(page.getByRole('heading', { name: 'test xml' })).toBeVisible();
  });

  test('JSON', async ({ page }) => {

    await expect(page.getByText('Welcome to the SAEOSS Portal METADATA Discover a world of data-driven')).toBeVisible();

    await expect(page.locator('#title-header')).toContainText('Welcome to the SAEOSS Portal');

    await expect(page.getByRole('link', { name: 'METADATA', exact: true })).toBeVisible();

    await expect(page.getByRole('heading')).toContainText('Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision making.');

    await expect(page.locator('.navbar-brand')).toBeVisible();

    await expect(page.getByTestId('loggedin_user_icon')).toBeVisible();

    await page.getByRole('link', { name: 'METADATA', exact: true }).click();

    await page.waitForURL('**/dataset/');

    await expect(page.getByRole('heading', { name: 'Metadata', exact: true })).toBeVisible();

    await expect(page.getByRole('link', { name: 'Add metadata record' })).toBeVisible();

    await expect(page.getByRole('button', { name: ' Add metadata record from' })).toBeVisible();

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByRole('button', { name: ' Add metadata record from' }).click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/SANS1878.json');

    await page.waitForLoadState('load');

    await expect(page.getByText('all packages were created×')).toBeVisible();

    await page.getByRole('link', { name: '×' }).click();

    await page.reload();

    await expect(page.getByRole('heading', { name: 'Metadata', exact: true })).toBeVisible();

    await expect(page.getByLabel('Breadcrumb').getByRole('list')).toContainText('4 metadata records found');

    await expect(page.locator('li').filter({ hasText: 'test json Abstract from the' })).toBeVisible();

    await page.locator('#content div').filter({ hasText: 'test json Abstract from the' }).nth(2).click();

    await page.getByRole('link', { name: 'test json' }).click();

    await expect(page.getByRole('heading', { name: 'test json' })).toBeVisible();

    await expect(page.getByRole('heading', { name: 'Dataset extent' })).toBeVisible();

    await expect(page.getByRole('link', { name: ' Manage' })).toBeVisible();

    await page.getByRole('link', { name: ' Groups' }).click();

    await page.getByRole('link', { name: ' Activity Stream' }).click();

    await expect(page.getByText('admin created the metadata')).toBeVisible();

    await page.getByRole('link', { name: 'Metadata', exact: true }).first().click();

    await expect(page.getByRole('heading', { name: 'test json' })).toBeVisible();
  });

  test('YAML', async ({ page }) => {

    await expect(page.getByText('Welcome to the SAEOSS Portal METADATA Discover a world of data-driven')).toBeVisible();

    await expect(page.locator('#title-header')).toContainText('Welcome to the SAEOSS Portal');

    await expect(page.getByRole('link', { name: 'METADATA', exact: true })).toBeVisible();

    await expect(page.getByRole('heading')).toContainText('Discover a world of data-driven possibilities at the SAEOSS-Portal, where information converges to empower data sharing and decision making.');

    await expect(page.locator('.navbar-brand')).toBeVisible();

    await expect(page.getByTestId('loggedin_user_icon')).toBeVisible();

    await page.getByRole('link', { name: 'METADATA', exact: true }).click();

    await page.waitForURL('**/dataset/');

    await expect(page.getByRole('heading', { name: 'Metadata', exact: true })).toBeVisible();

    await expect(page.getByRole('link', { name: 'Add metadata record' })).toBeVisible();

    await expect(page.getByRole('button', { name: ' Add metadata record from' })).toBeVisible();

    const fileChooserPromise = page.waitForEvent('filechooser');

    await page.getByRole('button', { name: ' Add metadata record from' }).click();

    const fileChooser = await fileChooserPromise;

    await fileChooser.setFiles('tests/fixtures/SANS1878.yaml');

    await page.waitForLoadState('load');

    await expect(page.getByText('all packages were created×')).toBeVisible();

    await page.getByRole('link', { name: '×' }).click();

    await page.reload();

    await expect(page.getByRole('heading', { name: 'Metadata', exact: true })).toBeVisible();

    await expect(page.getByLabel('Breadcrumb').getByRole('list')).toContainText('5 metadata records found');

    await expect(page.locator('li').filter({ hasText: 'test yaml Abstract from the' })).toBeVisible();

    await page.locator('#content div').filter({ hasText: 'test yaml Abstract from the' }).nth(2).click();

    await page.getByRole('link', { name: 'test yaml' }).click();

    await expect(page.getByRole('heading', { name: 'test yaml' })).toBeVisible();

    await expect(page.getByRole('heading', { name: 'Dataset extent' })).toBeVisible();

    await expect(page.getByRole('link', { name: ' Manage' })).toBeVisible();

    await page.getByRole('link', { name: ' Groups' }).click();

    await page.getByRole('link', { name: ' Activity Stream' }).click();

    await expect(page.getByText('admin created the metadata')).toBeVisible();

    await page.getByRole('link', { name: 'Metadata', exact: true }).first().click();

    await expect(page.getByRole('heading', { name: 'test yaml' })).toBeVisible();
  });

});