# batch-voice

音声ファイルの文字起こしをバッチ処理で行うWebアプリケーション

## 概要

ユーザーが音声ファイルをアップロードし、AIによる文字起こしを非同期で実行するWebアプリケーションです。
- AWS上での稼働を想定（DynamoDB、SQS、ECS Tasks）
- ローカル開発環境としてLocalStackを使用
- 現在バックエンドAPIが実装済み、フロントエンドUIを開発中

## 技術スタック

### フロントエンド
- React.js + TypeScript
- Vite
- Tailwind CSS

### バックエンド
- FastAPI (Python)
- boto3 / aiobotocore (AWS SDK)
- SQS + ECS Tasks (バッチ処理)

### インフラ
- AWS DynamoDB (データベース)
- AWS S3 (ファイルストレージ)
- AWS SQS (メッセージキュー)
- AWS ECS (バッチ処理)

### 文字起こし
- OpenAI Whisper API

## ローカル開発環境

### 必要な環境
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- AWS CLI (optional)

### セットアップ

1. リポジトリをクローン
```bash
git clone <repository-url>
cd batch-voice
```

2. 環境設定ファイルをコピー
```bash
cp .env.example .env
```

3. LocalStackとインフラサービスを起動
```bash
make setup
```

4. 全サービスを起動
```bash
make up
```

### 利用可能なサービス

| サービス | URL | 説明 | 状況 |
|----------|-----|------|------|
| LocalStack | http://localhost:4566 | AWS サービスエミュレーション | ✅ 利用可能 |
| API | http://localhost:8000 | バックエンド API | ✅ 実装済み |
| API Docs | http://localhost:8000/docs | Swagger UI | ✅ 利用可能 |
| Frontend | http://localhost:3000 | フロントエンド UI | ⏳ 実装予定 |

### APIエンドポイント

| メソッド | エンドポイント | 説明 |
|----------|---------------|------|
| GET | `/api/health` | ヘルスチェック |
| POST | `/api/jobs` | ファイルアップロード・ジョブ作成 |
| GET | `/api/jobs/{job_id}` | ジョブ状態確認 |

### クイックテスト

```bash
# ヘルスチェック
curl http://localhost:8000/api/health

# ファイルアップロード例
curl -X POST "http://localhost:8000/api/jobs" \
  -F "file=@sample.mp3;type=audio/mpeg"
```

### 開発コマンド

```bash
# インフラのみ起動
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

## プロジェクト構造

```
batch-voice/
├── docs/                        # ドキュメント
│   ├── system-design.md         # システム設計書
│   ├── architecture.md          # アーキテクチャ設計書
│   ├── technology-decisions.md  # 技術選定書
│   └── api-reference.md         # API リファレンス
├── backend/                     # バックエンド ✅ 実装済み
│   ├── app/                     # FastAPI アプリケーション
│   ├── Dockerfile               # コンテナ設定
│   └── requirements.txt         # Python依存関係
├── frontend/                    # フロントエンド ⏳ 実装予定
├── scripts/                     # セットアップスクリプト
├── docker-compose.yml           # Docker構成
├── Makefile                     # 開発コマンド
└── README.md                    # このファイル
```

## 開発フェーズ

### フェーズ1: 基盤構築 ✅ **完了**
- [x] プロジェクト設計
- [x] ローカル開発環境構築
- [x] 基本的なAPI設計・実装

### フェーズ2: コア機能開発 🔄 **進行中**
- [x] ファイルアップロード機能（S3連携）
- [x] バッチ処理基盤（SQSキュー投入）
- [x] FastAPI バックエンド実装
- [ ] 文字起こし処理ワーカー（OpenAI Whisper API）
- [ ] 基本的なフロントエンド画面

### フェーズ3: 機能拡張 ⏳ **予定**
- [ ] ユーザー管理機能
- [ ] 処理履歴管理
- [ ] 結果編集機能

### フェーズ4: 運用準備 ⏳ **予定**
- [ ] テスト実装
- [ ] デプロイ環境構築
- [ ] 監視・ログ設定

## ドキュメント

- [システム設計書](docs/system-design.md) - プロジェクト全体設計
- [アーキテクチャ設計書](docs/architecture.md) - 技術アーキテクチャ
- [技術選定書](docs/technology-decisions.md) - 技術選択の理由
- [API リファレンス](docs/api-reference.md) - API仕様書

## 貢献

1. Issue作成
2. Feature branchを作成
3. Pull Request作成

## ライセンス

MIT License