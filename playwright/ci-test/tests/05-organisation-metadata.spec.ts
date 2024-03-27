import { test, expect } from '@playwright/test';

let url = '/';

test.use({
  storageState: 'auth.json'
});

test('add organisation metadata', async ({ page }) => {
  await page.goto(url);

  await expect(page.locator('#title-header')).toContainText('Welcome to the SAEOSS Portal');

  await expect(page.getByText('Welcome to the SAEOSS Portal')).toBeVisible();

  await page.getByRole('link', { name: 'Organisations' }).click();

  await expect(page.getByRole('link', { name: ' Add Organisation' })).toBeVisible();

  await expect(page.getByRole('complementary')).toContainText('What are Organisations?');

  await expect(page.getByRole('link', { name: 'View Test' })).toBeVisible();

  await page.getByRole('link', { name: 'View Test' }).click();

  await expect(page.locator('h1')).toContainText('Test');

  await expect(page.getByRole('complementary')).toContainText('This is a test organisation.');

  await expect(page.getByRole('link', { name: ' Metadata Record' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' Activity Stream' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' About' })).toBeVisible();

  await expect(page.getByRole('link', { name: ' Add metadata record' })).toBeVisible();

  await page.getByRole('link', { name: ' Add metadata record' }).click();

  await expect(page.getByRole('heading')).toContainText('What are metadata records?');

  await expect(page.getByRole('complementary')).toContainText('A Metadata Record is a collection of data resources (such as files), together with a description and other information, at a fixed URL. Metadata Records are what users see when searching for data.');

  await expect(page.getByText('Create metadata record')).toBeVisible();

  await expect(page.getByPlaceholder('eg. A descriptive title')).toBeEmpty();

  await page.getByPlaceholder('eg. A descriptive title').click();

  await page.getByPlaceholder('eg. A descriptive title').fill('test2 metadata');

  await page.getByLabel('Feature metadata record on').check();

  await page.getByLabel('DOI').click();

  await page.getByPlaceholder('eg. Some useful notes about').click();
  await page.getByPlaceholder('eg. Some useful notes about').fill('test2 metadata');

  await page.getByText('Visibility', { exact: true }).click();
  await page.getByLabel('Visibility').selectOption('False');
  await expect(page.getByLabel('Visibility')).toHaveValue('False');

  await page.getByLabel('* Individual name').click();
  await page.getByLabel('* Individual name').fill('admin');

  await page.getByLabel('* Position name').click();
  await page.getByLabel('* Position name').fill('admin');

  //await page.getByRole('textbox', { name: 'Tags:' }).fill('environment');

  await page.getByLabel('Dataset language').click();
  await page.getByLabel('Dataset language').fill('English');

  await page.getByLabel('* Metadata language').click();
  await page.getByLabel('* Metadata language').fill('English');
  
  await page.getByLabel('* Lineage statement').click();
  await page.getByLabel('* Lineage statement').fill('testing');
  
  await page.getByLabel('Individual contact name').fill('tester');
  
  await page.getByLabel('Role / Position of the').click();
  await page.getByLabel('Role / Position of the').fill('tester');
  
  await page.getByLabel('* Metadata record distribution format name').fill('Electronic');
  await page.getByPlaceholder('1.0').click();
  await page.getByPlaceholder('1.0').fill('1');
  
  await page.getByLabel('* Spatial resolution').click();
  await page.getByLabel('* Spatial resolution').fill('1:5000');
  
  await page.getByLabel('Spatial Reference System').click();
  await page.getByLabel('Spatial Reference System').fill('EPSG:4326');
  
  await page.getByLabel('* Reference datetime').click();
  await page.getByLabel('* Reference datetime').fill('2024-01-26T11:05');
  
  await page.getByLabel('* Metadata stamp date').click();
  await page.getByLabel('* Metadata stamp date').fill('2024-01-26T11:12');
  
  await page.getByRole('button', { name: 'Next: Add links' }).click();

  await expect(page.getByText('Metadata record details')).toBeVisible();
  
  await expect(page.getByRole('heading')).toContainText('What\'s a resource?');
  
  await expect(page.getByRole('complementary')).toContainText('A resource can be any file or link to a file containing useful data.');
  
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByLabel('File').click();
  const fileChooser = await fileChooserPromise;

  await fileChooser.setFiles('tests/fixtures/data2.json');
  //await page.getByLabel('File').setInputFiles('data.json');
  
  await page.getByPlaceholder('eg. January 2011 Gold Prices').click();
  await page.getByPlaceholder('eg. January 2011 Gold Prices').fill('test-data');
  
  await page.getByRole('link', { name: 'eg. CSV, XML or JSON' }).click();
  await page.getByRole('combobox', { name: 'Format:' }).fill('JSON');
  await page.getByRole('option', { name: 'JSON', exact: true }).click();
  await page.getByRole('button', { name: 'Finish' }).click();
  
  await expect(page.getByRole('heading', { name: 'test2 metadata' })).toBeVisible();
  
  //await expect(page.getByRole('article')).toContainText('Test metadata');
  
  await expect(page.getByRole('heading', { name: 'Data and Resources' })).toBeVisible();
  
  await expect(page.getByRole('link', { name: 'test-data JSON' })).toBeVisible();

  await page.keyboard.press('PageDown');
  
  await expect(page.getByRole('heading', { name: 'Additional Info' })).toBeVisible();
  
  await expect(page.getByText('Additional Info Field Value')).toBeVisible();
  
  await expect(page.getByRole('heading', { name: 'Test', exact: true })).toBeVisible();
});