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
- boto3 / aiobotocore (AWS SDK)
- SQS + ECS Tasks (バッチ処理)

### 文字起こし
- OpenAI Whisper API

### データベース
- DynamoDB

### インフラ
- Docker + Docker Compose
- AWS S3 (ファイルストレージ)
- AWS DynamoDB (データベース)
- AWS SQS (メッセージキュー)
- AWS ECS (バッチ処理)

## リポジトリ構造

```
batch-voice/
├── docs/                   # ドキュメント
│   ├── system-design.md    # システム設計書
│   ├── architecture.md     # アーキテクチャ設計書
│   └── technology-decisions.md # 技術選定書
├── backend/                # バックエンド（実装予定）
├── frontend/               # フロントエンド（実装予定）
├── scripts/                # セットアップスクリプト
│   └── setup-localstack.sh # LocalStack初期化
├── docker-compose.yml      # Docker構成
├── Makefile               # 開発コマンド
├── .env.example           # 環境設定例
├── .gitignore             # Git除外設定
└── .claude/               # Claude Code設定
```

## 開発状況

プロジェクトは設計段階です。基本設計書が完成し、これから実装フェーズに入ります。

## ローカル開発環境

### セットアップ
```bash
# 環境設定ファイルをコピー
cp .env.example .env

# LocalStackとインフラサービスを起動・セットアップ
make setup

# 全サービスを起動
make up
```

### 開発コマンド
```bash
# インフラのみ起動（開発時推奨）
make up-infra

# 全サービス起動
make up-full

# ログ確認
make logs

# サービス停止
make down

# 環境リセット
make clean

# LocalStackの状態確認
make localstack-status
```

### 利用可能なサービス
- **LocalStack**: http://localhost:4566 (AWS サービスエミュレーション)
- **API**: http://localhost:8000 (実装後)
- **Frontend**: http://localhost:3000 (実装後)

### AWS サービス (LocalStack)
- **DynamoDB**: batch-voice-users, batch-voice-jobs, batch-voice-results
- **S3**: batch-voice-files
- **SQS**: batch-voice-jobs