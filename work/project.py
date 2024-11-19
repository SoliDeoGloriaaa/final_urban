import os
import csv

path = r'D:\DEV\final_urban\work'
COLUMN_NAME_PRODUCT = ['товар', 'название', 'наименование', 'продукт']
COLUMN_PRICE_PRODUCT = ['розница', 'цена']
COLUMN_WEIGHT_PRODUCT = ['вес', 'масса', 'фасовка']


class PriceMachine:
    def __init__(self):
        self.data = []

    def load_prices(self, file_path=''):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
        '''
        try:
            for filename in os.listdir(file_path):
                if 'price' in filename.lower() and filename.endswith('.csv'):
                    with open(filename, mode='r', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        headers = next(reader)
                        product_indices = self._search_product_price_weight(headers)
                        for row in reader:
                            product_info = {
                                'name': row[product_indices['name']],
                                'price': float(row[product_indices['price']]),
                                'weight': float(row[product_indices['weight']]),
                                'file': os.path.basename(filename)
                            }
                            product_info['price_per_kg'] = product_info['price'] / product_info['weight'] if product_info['weight'] > 0 else None
                            self.data.append(product_info)
        except Exception as error:
            print(error)

    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        return {
            'name': next(i for i, j in enumerate(headers) if j.lower() in COLUMN_NAME_PRODUCT),
            'price': next(i for i, j in enumerate(headers) if j.lower() in COLUMN_PRICE_PRODUCT),
            'weight': next(i for i, j in enumerate(headers) if j.lower() in COLUMN_WEIGHT_PRODUCT)
        }

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
            <style>
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Список продуктов</h1>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        for index, product in enumerate(self.data):
            result += f'''
                <tr>
                    <td>{index + 1}</td>
                    <td>{product['name']}</td>
                    <td>{product['price']:.2f}</td>
                    <td>{product['weight']}</td>
                    <td>{product['file']}</td>
                    <td>{product['price_per_kg']:.2f}</td>
                </tr>
            '''

        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as file:
            file.write(result)

        return fname

    def find_text(self, text):
        ''' Метод для поиска текста в загруженных данных '''
        results = [
            product for product in self.data if text.lower() in product['name'].lower()
        ]
        results = sorted(results, key=lambda x: x['price_per_kg'])
        print(f"{'№':<3} {'Наименование':<30} {'Цена':<8} {'Вес':<5} {'Файл':<15} {'Цена за кг.':<12}")
        for index, product in enumerate(results):
            print(f"{index + 1:<3} {product['name']:<30} {product['price']:<8} {product['weight']:<5} {product['file']:<15} {product['price_per_kg']:<12.2f}")
        return results


pm = PriceMachine()
pm.load_prices(path)

while True:
    user_input = input("Введите текст для поиска (или 'exit' для выхода): ")
    if user_input.lower() == 'exit':
        break
    results = pm.find_text(user_input)
    if len(results) == 0:
        print("Товары не найдены.")

print('the end')
print(pm.export_to_html())
