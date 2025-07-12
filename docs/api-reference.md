# API リファレンス

## 概要

Batch Voice APIは音声ファイルの文字起こしをバッチ処理で行うREST APIです。

### ベースURL
- 開発環境: `http://localhost:8000`

### API仕様書
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI仕様: `http://localhost:8000/openapi.json`

## 認証

現在の実装では認証は不要です（開発段階）。

## エンドポイント

### 1. ヘルスチェック

APIの動作状況を確認します。

```http
GET /api/health
```

#### レスポンス

```json
{
  "status": "ok",
  "message": "API is running"
}
```

#### ステータスコード
- `200 OK` - API正常動作中

---

### 2. ジョブ作成（ファイルアップロード）

音声ファイルをアップロードし、文字起こしジョブを作成します。

```http
POST /api/jobs
```

#### リクエスト

**Content-Type:** `multipart/form-data`

| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| `file` | File | ✓ | 音声ファイル（MP3, WAV, M4A, FLAC） |
| `user_id` | string | - | ユーザーID（デフォルト: "default_user"） |

#### レスポンス

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### ステータスコード
- `200 OK` - ジョブ作成成功
- `400 Bad Request` - 無効なファイル形式
- `500 Internal Server Error` - サーバーエラー

#### curl例

```bash
curl -X POST "http://localhost:8000/api/jobs" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.mp3;type=audio/mpeg"
```

---

### 3. ジョブ状態確認

指定されたジョブの現在の状態と詳細情報を取得します。

```http
GET /api/jobs/{job_id}
```

#### パラメータ

| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| `job_id` | string | ✓ | ジョブID（UUID形式） |

#### レスポンス

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "default_user",
  "file_name": "audio.mp3",
  "file_path": "default_user/550e8400-e29b-41d4-a716-446655440000.mp3",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "completed_at": null,
  "error_message": null
}
```

#### ジョブステータス

| ステータス | 説明 |
|-----------|------|
| `pending` | 処理待ち |
| `processing` | 文字起こし処理中 |
| `completed` | 処理完了 |
| `failed` | 処理失敗 |

#### ステータスコード
- `200 OK` - ジョブ情報取得成功
- `404 Not Found` - ジョブが見つからない

#### curl例

```bash
curl -X GET "http://localhost:8000/api/jobs/550e8400-e29b-41d4-a716-446655440000" \
  -H "accept: application/json"
```

---

## データモデル

### Job（ジョブ）

```typescript
interface Job {
  job_id: string;          // ジョブID（UUID）
  user_id: string;         // ユーザーID
  file_name: string;       // 元のファイル名
  file_path: string;       // S3上のファイルパス
  status: JobStatus;       // ジョブステータス
  created_at: string;      // 作成日時（ISO 8601）
  updated_at: string;      // 更新日時（ISO 8601）
  completed_at?: string;   // 完了日時（ISO 8601）
  error_message?: string;  // エラーメッセージ
}
```

### JobStatus（ジョブステータス）

```typescript
enum JobStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  COMPLETED = "completed",
  FAILED = "failed"
}
```

---

## エラーレスポンス

APIエラーは以下の形式で返されます：

```json
{
  "detail": "エラーメッセージ"
}
```

### 一般的なエラーコード

| ステータスコード | 説明 |
|----------------|------|
| `400 Bad Request` | リクエストパラメータが無効 |
| `404 Not Found` | リソースが見つからない |
| `422 Unprocessable Entity` | バリデーションエラー |
| `500 Internal Server Error` | サーバー内部エラー |

---

## 使用例

### 1. 音声ファイルアップロード〜状態確認の流れ

```bash
# 1. ファイルアップロード
response=$(curl -s -X POST "http://localhost:8000/api/jobs" \
  -F "file=@sample.mp3;type=audio/mpeg")

# 2. job_idを取得
job_id=$(echo $response | jq -r '.job_id')

# 3. ジョブ状態確認
curl -X GET "http://localhost:8000/api/jobs/$job_id"
```

### 2. 複数ファイルの一括処理

```bash
#!/bin/bash
for file in *.mp3; do
  echo "Processing: $file"
  curl -s -X POST "http://localhost:8000/api/jobs" \
    -F "file=@$file;type=audio/mpeg" | jq .
done
```

---

## 技術仕様

### 依存サービス
- **DynamoDB**: ジョブ情報・結果保存
- **S3**: 音声ファイル保存  
- **SQS**: バッチ処理キュー

### 対応ファイル形式
- MP3 (audio/mpeg)
- WAV (audio/wav)  
- M4A (audio/mp4)
- FLAC (audio/flac)

### 制限事項
- ファイルサイズ制限: 未実装（今後設定予定）
- 同時処理数制限: 未実装（今後設定予定）
- レート制限: 未実装（今後設定予定）

---

## 開発・デバッグ

### ローカル環境起動

```bash
# LocalStack + API起動
make setup
docker compose up -d api

# ヘルスチェック
curl http://localhost:8000/api/health
```

### ログ確認

```bash
# APIコンテナのログ
docker logs batch-voice-api

# LocalStackのログ  
docker logs batch-voice-localstack
```

### AWS リソース確認

```bash
# DynamoDB テーブル一覧
aws --endpoint-url=http://localhost:4566 dynamodb list-tables

# S3 バケット確認
aws --endpoint-url=http://localhost:4566 s3 ls

# SQS キュー確認
aws --endpoint-url=http://localhost:4566 sqs list-queues
```