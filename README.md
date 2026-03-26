# pptx-to-markdown

`.pptx` ファイルを構造化された Markdown に変換する CLI ツールです。プレゼン資料・社内資料を LLM による分析にかけるための前処理用途を想定しています。

## 特徴

- スライドのテキスト・箇条書き階層を Markdown に変換
- テーブルを Markdown テーブルとして出力
- 画像を base64 データ URI として埋め込み
- チャートのデータをテーブルとして抽出
- 発表者ノートをセクションとして出力

## 必要環境

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/)

## インストール

```bash
git clone <repository-url>
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

## 出力形式

```markdown
# スライド 1: タイトル

本文テキスト

- 箇条書き
  - ネスト

| 列A | 列B |
|-----|-----|
| 値1 | 値2 |

<!-- チャート: 棒グラフ -->
| カテゴリ | シリーズ1 |
|----------|-----------|
| 項目A    | 10        |

![スライド1_画像1](data:image/png;base64,...)

## ノート

発表者ノート

---
```

## 開発

```bash
# 依存関係インストール
uv sync

# テスト実行
uv run pytest

# カバレッジ付きテスト
uv run pytest --cov=pptx_to_markdown
```

## 制限事項

- `.ppt`（旧形式）は非対応
- アニメーション・トランジション情報は変換対象外
- 複雑なレイアウト（重なり合った図形等）はテキスト抽出のみ

## ライセンス

MIT
