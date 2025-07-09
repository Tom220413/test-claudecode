# Todo アプリケーション仕様書

## 概要
このプロジェクトは、TDD（Test-Driven Development）手法を用いて開発されたシンプルなTodoアプリケーションです。FlaskフレームワークとSQLite3データベースを使用しています。

## 機能仕様

### 1. 基本機能
- **Todoアイテム追加**: テキスト入力フィールドから新しいTodoアイテムを追加
- **Todoリスト表示**: 登録されたTodoアイテムをWebページにリスト表示
- **完了状態切り替え**: チェックボックスによる完了/未完了の切り替え
- **データ永続化**: アプリケーション再起動後もTodoの状態を保持

### 2. 入力バリデーション
- 空文字列の投稿を防止
- 文字数制限（200文字以内）
- HTMLエスケープによるXSS対策

### 3. エラーハンドリング
- 存在しないTodoアイテムの操作時の例外処理
- データベース接続エラーの適切な処理

## 技術仕様

### 使用技術
- **バックエンド**: Python Flask 2.3.3
- **データベース**: SQLite3
- **テスト**: pytest 7.4.2
- **カバレッジ**: pytest-cov 4.1.0

### アーキテクチャ
```
project-claude-a/
├── app.py                   # Flask アプリケーション メイン
├── todo_model.py           # データベース操作モデル
├── templates/
│   └── index.html          # メイン画面テンプレート
├── tests/
│   ├── test_app.py         # Flask アプリケーションのテスト
│   └── test_todo_model.py  # データモデルのテスト
├── requirements.txt        # 依存関係
└── README.md              # プロジェクト説明
```

## データベーススキーマ

### todos テーブル
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);
```

## API仕様

### エンドポイント一覧

#### GET /
- **概要**: メイン画面の表示
- **戻り値**: Todoリストを含むHTMLページ
- **テンプレート**: templates/index.html

#### POST /add
- **概要**: 新しいTodoアイテムの追加
- **パラメータ**: 
  - `task` (string): 追加するTodoのテキスト（必須、200文字以内）
- **戻り値**: メイン画面へのリダイレクト

#### POST /toggle/<int:item_id>
- **概要**: 指定されたTodoアイテムの完了状態を切り替え
- **パラメータ**: 
  - `item_id` (int): 切り替え対象のTodoアイテムID
- **戻り値**: メイン画面へのリダイレクト

## テスト仕様

### テストカバレッジ
- **達成率**: 98%（目標80%以上を達成）
- **テスト数**: 10個

### テストケース

#### todo_model.py のテスト
1. `test_add_todo_item`: アイテム追加機能のテスト
2. `test_get_all_items`: 全アイテム取得機能のテスト
3. `test_toggle_completion`: 完了状態切り替えのテスト
4. `test_empty_list_initially`: 初期状態（空リスト）のテスト
5. `test_persistence_across_instances`: データ永続化のテスト

#### app.py のテスト
1. `test_index_page_shows_todo_list`: メインページ表示のテスト
2. `test_add_new_todo_item`: 新規アイテム追加のテスト
3. `test_toggle_todo_completion`: 完了状態切り替えのテスト
4. `test_empty_todo_list_initially`: 初期状態表示のテスト
5. `test_add_multiple_todos`: 複数アイテム追加のテスト

## 実行方法

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. アプリケーションの起動
```bash
python app.py
```

### 3. テストの実行
```bash
# 全テストの実行
python -m pytest

# カバレッジ付きテストの実行
python -m pytest --cov=. --cov-report=term-missing
```

## セキュリティ対策

### 実装済み対策
- **XSS対策**: Flask/Jinja2による自動HTMLエスケープ
- **SQLインジェクション対策**: パラメータ化クエリの使用
- **入力値検証**: 文字数制限、空文字列チェック

### 今後の改善点
- CSRFトークンの実装
- レート制限の実装
- HTTPSの強制
- セッション管理の実装

## パフォーマンス

### 最適化済み項目
- データベース接続の効率的な管理
- SQLクエリの最適化
- 軽量なHTMLテンプレート

## 今後の拡張可能性

### 機能拡張
- Todoアイテムの削除機能
- 優先度設定機能
- カテゴリ分類機能
- 期限設定機能

### 技術的拡張
- REST API化
- ユーザー認証機能
- リアルタイム同期
- モバイル対応

## 開発プロセス

このプロジェクトは**TDD（Test-Driven Development）**手法に従って開発されました：

1. **Red**: 失敗するテストを先に書く
2. **Green**: テストが通る最小限のコードを実装
3. **Refactor**: コードの品質を向上させる

この開発プロセスにより、高品質で保守性の高いコードを実現しています。

## 作成日時
2025年7月9日

## 作成者
Claude Code AI Assistant