# pptx-to-markdown

`.pptx` ファイルを構造化された Markdown に変換する CLI ツールです。プレゼン資料・社内資料を LLM による分析にかけるための前処理用途を想定しています。

[English README is here](README.md)

## 特徴

- スライドのテキスト・箇条書き階層を Markdown に変換
- テーブルを Markdown テーブルとして出力
- 画像を base64 データ URI として埋め込み
- チャートのデータをテーブルとして抽出
- 発表者ノートをセクションとして出力

## インストール

**前提条件:** Python 3.11 以上と [uv](https://docs.astral.sh/uv/) が必要です。

```bash
git clone https://github.com/nlink-jp/pptx-to-markdown.git
cd pptx-to-markdown
uv sync
```

## 使い方

```bash
# stdout に出力
uv run pptx2md input.pptx

# ファイルに出力
uv run pptx2md input.pptx -o output.md

# 画像を省略（プレースホルダに置き換え）
uv run pptx2md input.pptx --no-images

# 発表者ノートを省略
uv run pptx2md input.pptx --no-notes

# チャートデータを省略
uv run pptx2md input.pptx --no-charts
```

### 出力形式

```markdown
# スライド 1: タイトル

- 箇条書き
  - ネスト

| 列A | 列B |
| --- | --- |
| 値1 | 値2 |

<!-- チャート: COLUMN_CLUSTERED -->
| カテゴリ | シリーズ1 |
| --- | --- |
| 項目A | 10 |

![スライド1_画像1](data:image/png;base64,...)

## ノート

発表者ノート

---

# スライド 2: 次のスライド
```

チャートコメントのタイプ名は python-pptx の `XL_CHART_TYPE` 列挙名（例: `COLUMN_CLUSTERED`, `BAR_CLUSTERED`, `LINE`, `PIE`）です。

## ビルド

```bash
# 依存関係インストール（dev含む）
uv sync

# テスト実行
make test

# ロックした依存の既知の勧告
make vuln

# カバレッジ付きテスト
uv run pytest --cov=pptx_to_markdown
```

## 制限事項

- `.ppt`（旧形式）は非対応
- アニメーション・トランジション情報は変換対象外
- グループシェイプ内の要素は変換対象外

## ライセンス

MIT © magifd2
