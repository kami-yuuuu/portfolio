# 家計簿アプリ

## バックエンド開発時のメモ



### DBスキーマ
#### transacitonテーブル
| カラム名              | 型             | 説明                                |
| ----------------- | ------------- | --------------------------------- |
| id                | int (PK)      | 主キー                               |
| date              | date          | 取引日                               |
| type              | string        | 'income' / 'expense'              |
| category_id       | int (FK)      | カテゴリID（Categoryテーブル参照）            |
| amount            | float         | 金額                                |
| memo              | string        | メモ（任意）                            |
| payment_method_id | int (FK)      | 支払い方法ID（PaymentMethodテーブル参照）      |
| repeat            | string / JSON | 繰り返し設定（例：'monthly' または JSON 詳細指定） |
| receipt_image     | string        | レシート画像のパスやURL（オプション）              |
| created_at        | datetime      | 登録日時                              |
| updated_at        | datetime      | 更新日時                              |

#### Categoryテーブル
| カラム名  | 型        | 説明                   |
| ----- | -------- | -------------------- |
| id    | int (PK) | 主キー                  |
| name  | string   | カテゴリ名（食費、交通費など）      |
| type  | string   | 'income' / 'expense' |
| color | string   | 表示用カラー（任意）           |


#### PaymentMethodテーブル
| カラム名        | 型        | 説明                                 |
| ----------- | -------- | ---------------------------------- |
| id          | int (PK) | 主キー                                |
| name        | string   | 'cash', 'credit_card', 'PayPay' など |
| description | string   | 任意説明                               |



