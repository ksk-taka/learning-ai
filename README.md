# AI / Web エンジニア学習プロジェクト

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

---

## 目次

1. [プロジェクト概要](#プロジェクト概要)
2. [背景と動機](#背景と動機)
3. [12ヶ月ロードマップ](#12ヶ月ロードマップ)
4. [Phase 1: 基盤構築 — Python Web開発の土台](#phase-1-基盤構築--python-web開発の土台)
5. [Phase 2: AI/LLM基礎 — 生成AIの実装力](#phase-2-aillm基礎--生成aiの実装力)
6. [Phase 3: フロントエンド + フルスタック](#phase-3-フロントエンド--フルスタック)
7. [Phase 4: 実践とインフラ深化](#phase-4-実践とインフラ深化)
8. [Phase 5: ポートフォリオ + 案件準備](#phase-5-ポートフォリオ--案件準備)
9. [ディレクトリ構成](#ディレクトリ構成)
10. [開発環境](#開発環境)
11. [技術スタック](#技術スタック)
12. [進捗管理](#進捗管理)
13. [学習リソース](#学習リソース)

---

## プロジェクト概要

本プロジェクトは、**AI/MLエンジニア + Webバックエンド/インフラ** のスキルを
**12ヶ月間で実務レベルに引き上げる**ための体系的な学習プログラムです。

組込みエンジニアとしての経験（ハードウェア制御、リアルタイムシステム、センサ技術）を
基盤に、AI/Web 領域のスキルセットを段階的に習得します。

### 最終ゴール

1. **AI/LLM エンジニアとして**: RAGシステムの設計・実装、LLM APIを活用したアプリ開発ができる
2. **Web バックエンドエンジニアとして**: FastAPI / Next.js でのAPI設計・実装、DB設計、Docker化、クラウドデプロイができる
3. **副業として**: 月5万円以上の案件を獲得・遂行できる技術力とポートフォリオがある

---

## 背景と動機

### なぜ AI / Web なのか

- **LLM の進化**により、AIアプリケーション開発の需要が急増
- **組込み × AI/Web** の掛け算で独自のポジションを確立できる
- IoTデバイスの管理基盤や、ハードウェア関連のAI活用など、経験を活かせる案件が豊富

### 組込みエンジニアの強み

組込みシステムの経験は、Web/AI 領域でも大きなアドバンテージになります：

| 組込みの知識 | Web/AI での対応概念 |
|------------|-------------------|
| 割り込みハンドラ | async/await（非同期処理） |
| HAL（ハードウェア抽象化層） | 依存性注入（DI） |
| RTOS タスク | Docker コンテナ |
| OTA アップデート | DBマイグレーション（Alembic） |
| BLE ペアリングキー | JWT トークン（認証） |
| メモリマップドI/O | ORM（データベース抽象化） |

---

## 12ヶ月ロードマップ

### 全体像

```
Month  1-2   ████████░░░░░░░░░░░░░░░░  Phase 1: Python Web 基盤構築
Month  3-4   ░░░░░░░░████████░░░░░░░░  Phase 2: AI/LLM 基礎
Month  5-6   ░░░░░░░░░░░░░░░░████████  Phase 3: フロントエンド + フルスタック
Month  7-9   ░░░░░░░░░░░░████████████  Phase 4: 実践とインフラ深化
Month 10-12  ░░░░░░░░░░░░░░░░████████  Phase 5: ポートフォリオ + 案件準備
```

### フェーズ構成

```
Phase 1                Phase 2                Phase 3
FastAPI + DB + Docker  LLM API + RAG +        React + TypeScript +
                       エージェント            Next.js
        │                      │                      │
        └──────────┬───────────┘                      │
                   │                                  │
              Phase 4                            Phase 5
              AWS + CI/CD +                      ポートフォリオ +
              画像認識 + セキュリティ              案件獲得
```

---

## Phase 1: 基盤構築 — Python Web開発の土台

> **目標**: FastAPIでCRUD APIを作り、PostgreSQLと接続してDockerでデプロイできる

### Week 1-2: Python Web フレームワーク入門

| トピック | 内容 |
|---------|------|
| FastAPI 基本 | ルーティング、リクエスト/レスポンスモデル、Pydantic |
| 非同期処理 | async/await、asyncio.gather() |
| 課題 | TODO アプリの REST API を作成 |

### Week 3-4: データベースと ORM

| トピック | 内容 |
|---------|------|
| PostgreSQL | SQL クエリ、テーブル設計、CRUD 操作 |
| SQLAlchemy | ORM モデル定義、リレーション、Depends |
| Alembic | マイグレーション（autogenerate、upgrade/downgrade） |
| 認証 | bcrypt パスワードハッシュ化、JWT トークン、OAuth2 |
| 課題 | TODO アプリに DB 接続 + ユーザー認証を実装 |

### Week 5-6: コンテナとデプロイ

| トピック | 内容 |
|---------|------|
| Docker | Dockerfile、docker-compose |
| コンテナ環境 | FastAPI + PostgreSQL のコンテナ化 |
| AWS 基礎 | EC2 or Lambda + API Gateway |
| 課題 | TODO アプリを Docker 化してクラウドにデプロイ |

### Week 7-8: Phase 1 総合演習

| トピック | 内容 |
|---------|------|
| テスト | pytest によるテスト駆動開発 |
| API 設計 | OpenAPI / Swagger ベストプラクティス |
| 総合課題 | 「IoT デバイス管理 API」を設計・実装・デプロイ |

---

## Phase 2: AI/LLM基礎 — 生成AIの実装力

> **目標**: LLM API を使ったアプリを作れる。RAGの仕組みを理解し実装できる

### Week 9-10: LLM API 入門

- OpenAI API / Anthropic API の基本
- プロンプトエンジニアリング（System prompt、Few-shot、CoT）
- ストリーミングレスポンスの実装
- **課題**: CLI チャットボットを作成（会話履歴管理付き）

### Week 11-12: RAG（検索拡張生成）

- Embedding の仕組み（テキスト → ベクトル変換）
- ベクトル DB（ChromaDB → Pinecone / Weaviate）
- ドキュメントのチャンク分割戦略
- LangChain or LlamaIndex での RAG パイプライン構築
- **課題**: 「技術メモを RAG で検索できるシステム」を構築

### Week 13-14: Function Calling & エージェント

- Function Calling / Tool Use の仕組み
- 簡易 AI エージェントの実装
- **課題**: 「天気とニュースを取得して要約する AI アシスタント」

### Week 15-16: Phase 2 総合演習

- RAG + FastAPI + フロントの統合
- **総合課題**: 「データシート検索 AI」— 電子部品のデータシート PDF を RAG で検索

---

## Phase 3: フロントエンド + フルスタック

> **目標**: React + TypeScript で基本的な Web アプリの UI を作れる

- TypeScript の型システム
- React 基礎（コンポーネント、State、Props、Hooks）
- Next.js（App Router、Server Components）
- Phase 1-2 のバックエンドとの連携
- リアルタイム通信（WebSocket / SSE）
- 認証（NextAuth or Clerk）
- **総合課題**: 「社内文書 RAG 検索アプリ」フルスタック版

---

## Phase 4: 実践とインフラ深化

> **目標**: 本番運用を意識したインフラ構築と、実案件レベルのプロジェクト完遂

- AWS 実践（Lambda、RDS、S3、CloudFront、SQS）
- IaC（Terraform or CDK）基礎
- CI/CD（GitHub Actions）
- 画像認識（OpenCV、YOLO）、OCR（Tesseract、EasyOCR）
- マルチモーダル AI（GPT-4V / Claude Vision）
- セキュリティ（OAuth2、JWT、環境変数管理）
- **総合課題**: 本番品質の RAG アプリをセキュリティ込みでデプロイ

---

## Phase 5: ポートフォリオ + 案件準備

> **目標**: 副業案件を獲得できるポートフォリオと面談対応力を完成させる

- ポートフォリオプロジェクトの構築
- GitHub 整備（README、アーキテクチャ図）
- 技術面談の模擬練習
- 案件応募・提案書作成

---

## ディレクトリ構成

```
learning-ai/
├── README.md                # 本ファイル
├── CLAUDE.md                # Claude Code 学習エージェント設定
├── progress.json            # 進捗データ
├── .gitignore
│
├── notes/                   # 学習メモ（トピック別）
│   ├── week1-2_fastapi-basics.md
│   ├── week1-2_async-await.md
│   ├── week3-4_postgresql.md
│   ├── week3-4_sqlalchemy-orm.md
│   ├── week3-4_alembic.md
│   └── week3-4_authentication.md
│
├── projects/                # 課題・プロジェクトのコード
│   ├── phase1/              # Phase 1: Web基盤（FastAPI + PostgreSQL + 認証）
│   │   ├── main.py          # FastAPI アプリケーション
│   │   ├── models.py        # SQLAlchemy ORM モデル
│   │   ├── schemas.py       # Pydantic スキーマ
│   │   ├── auth.py          # JWT + bcrypt 認証
│   │   ├── database.py      # DB 接続設定
│   │   ├── alembic/         # マイグレーション
│   │   └── docker-compose.yml
│   ├── phase1-review/       # Phase 1 復習用コード
│   ├── phase2/              # Phase 2: AI/LLM（予定）
│   ├── phase3/              # Phase 3: フロントエンド（予定）
│   ├── phase4/              # Phase 4: インフラ（予定）
│   └── phase5/              # Phase 5: ポートフォリオ（予定）
│
└── weekly_retros/           # 週次振り返り記録
```

---

## 開発環境

### ソフトウェア

| カテゴリ | ツール | バージョン |
|---------|--------|-----------|
| **OS** | Windows 11 Home | 10.0.26200 |
| **エディタ** | VS Code + Claude Code | — |
| **言語** | Python | 3.10+ |
| **フレームワーク** | FastAPI | 0.100+ |
| **DB** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **マイグレーション** | Alembic | 1.x |
| **コンテナ** | Docker Desktop | — |
| **バージョン管理** | Git + GitHub | — |

---

## 技術スタック

### 習得済み・学習中

```
Phase 1（学習中）
├── FastAPI          ✅ 基本ルーティング、CRUD、Pydantic
├── async/await      ✅ 非同期処理、asyncio.gather()
├── PostgreSQL       ✅ SQL クエリ、テーブル設計
├── SQLAlchemy       ✅ ORM モデル、リレーション
├── Alembic          ✅ マイグレーション（autogenerate）
├── JWT + bcrypt     ✅ ユーザー認証
├── Docker           ⬚ 次の学習予定
└── AWS              ⬚ 次の学習予定
```

### これから習得する技術

```
Phase 2: LLM API, RAG, Embedding, ベクトルDB, LangChain
Phase 3: TypeScript, React, Next.js, WebSocket
Phase 4: AWS (Lambda/RDS/S3), Terraform, GitHub Actions, 画像認識, OCR
Phase 5: ポートフォリオ構築、案件獲得
```

---

## 進捗管理

### 現在の状況

- **Phase**: 1（基盤構築）
- **Week**: 3-4 完了 → Week 5-6（コンテナとデプロイ）に進行予定

### マイルストーン

| マイルストーン | 内容 | 状態 |
|-------------|------|------|
| M1 | FastAPI で TODO API 作成 | ✅ 完了 |
| M2 | PostgreSQL + SQLAlchemy 接続 | ✅ 完了 |
| M3 | Alembic マイグレーション | ✅ 完了 |
| M4 | JWT ユーザー認証 | ✅ 完了 |
| M5 | Docker 化 | ⬚ 未着手 |
| M6 | クラウドデプロイ | ⬚ 未着手 |
| M7 | Phase 1 総合課題（IoT API） | ⬚ 未着手 |

### 学習エージェント

本プロジェクトでは Claude Code を学習パートナーとして活用しています。
`CLAUDE.md` に定義された6つのモードで学習を支援します：

| コマンド | モード | 説明 |
|---------|--------|------|
| `@curriculum` | カリキュラム管理 | 学習計画の作成・進捗トラッキング |
| `@challenge` | コード課題 | 実践的な課題の出題と自動採点 |
| `@review` | コードレビュー | レビュー・ペアプログラミング |
| `@quiz` | 理解度テスト | 知識確認の Q&A |
| `@mock` | 模擬面談 | 技術面談の練習 |
| `@retro` | 振り返り | 週次レトロスペクティブ |

---

## 学習リソース

### 公式ドキュメント

| リソース | リンク |
|---------|--------|
| FastAPI | https://fastapi.tiangolo.com/ |
| SQLAlchemy | https://docs.sqlalchemy.org/ |
| Alembic | https://alembic.sqlalchemy.org/ |
| Docker | https://docs.docker.com/ |
| PostgreSQL | https://www.postgresql.org/docs/ |

### 今後利用予定

| リソース | リンク |
|---------|--------|
| Anthropic API | https://docs.anthropic.com/ |
| LangChain | https://python.langchain.com/ |
| React | https://react.dev/ |
| Next.js | https://nextjs.org/docs |
| AWS | https://docs.aws.amazon.com/ |

---

> **注記**: 本プロジェクトは個人の学習目的で作成されています。
