# CLAUDE.md

このファイルは、このリポジトリでコードを作業する際にClaude Code (claude.ai/code) にガイダンスを提供します。

## プロジェクト概要

`batch-voice` は音声ファイルの文字起こしをバッチ処理で行うWebアプリケーションです。ユーザーが音声ファイルをアップロードし、AIによる文字起こしを非同期で実行します。

### 主要機能
- 音声ファイルアップロード（MP3, WAV, M4A, FLAC対応）
- バッチ処理による文字起こし
- 結果表示・編集・ダウンロード機能
- ユーザー管理と処理履歴

## 技術スタック

### フロントエンド
- React.js + TypeScript
- Vite (ビルドツール)
- Tailwind CSS

### バックエンド
- FastAPI (Python)
- SQLAlchemy (ORM)
- Celery + Redis (タスクキュー)

### 文字起こし
- OpenAI Whisper API

### データベース
- PostgreSQL

### インフラ
- Docker + Docker Compose
- AWS S3 / MinIO (ファイルストレージ)

## リポジトリ構造

- `docs/` - プロジェクトドキュメント
  - `system-design.md` - システム設計書
- `.claude/` - Claude Code 設定ディレクトリ

## 開発状況

プロジェクトは設計段階です。基本設計書が完成し、これから実装フェーズに入ります。

## 開発コマンド

実装開始後、以下のコマンドが使用される予定です：

### バックエンド (FastAPI)
```bash
# 依存関係インストール
pip install -r requirements.txt

# 開発サーバー起動
uvicorn main:app --reload

# テスト実行
pytest

# リント
flake8 .
black .
```

### フロントエンド (React)
```bash
# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev

# ビルド
npm run build

# テスト実行
npm test

# リント
npm run lint
```

### Docker
```bash
# 開発環境起動
docker-compose up -d

# 停止
docker-compose down
```