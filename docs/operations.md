# KabeRadio Operations

## 基本方針

KabeRadio Repositoryは、壁ラジの公式アーカイブおよび将来の公式サイト用Canonical Sourceとして管理する。

現在のRepository可視性にかかわらず、**常にPublic化可能な内容だけを保存するPublic-facing Sourceとして扱う**。

運用上の手作業を可能な限り増やさない。

## Security / Publication Boundary

KabeRadio Repositoryはコンテンツ公開面であり、実行環境・認証・セキュリティ設定の正本にはしない。

以下の情報は保存禁止とする。

- API key、Access token、Bot token、Password、Secret、Credential
- Telegram等のUser ID / Chat ID、Allowlist、認証用識別子
- ローカル絶対パス、PCユーザー名、端末固有パス、TTS executable path
- `config.local.json`、`.env`、秘密鍵、証明書などの環境固有設定
- 内部管理URL、非公開Endpoint、セキュリティ構成や認証手順の詳細
- 公開を意図していない個人情報・家族情報・勤務先情報・位置情報
- その他、RepositoryをPublic化した際に公開すべきでない情報

これらは`amakawa-chan/amakawachan-assistant`側のRuntime、環境変数、ローカル設定、または適切なSecret管理へ分離する。

台本、README、Character Profile、Episode Package、Prompt、Documentを追加・更新する際も、**「公式サイトからそのまま公開されても問題ないか」**を保存判断の基準とする。

Git履歴を公開履歴として扱うため、秘密情報は「後で消す」のではなく、最初から一度もコミットしないことを優先する。

## Episode

エピソードは原則として以下の単位で保存する。

```text
episodes/
└─ <episode-key>/
   ├─ README.md
   └─ script.md
```

### script.md

Amakawachan Radioで使用する正式な台本。

壁打ちから台本が完成した時点でRepositoryへ保存する。

### README.md

そのエピソードの紹介ページ。

台本作成時に同時生成し、原則として公開後の手動更新を必要としない内容にする。

最低限、以下を含める。

- タイトル
- エピソード紹介
- Cast
- `script.md`へのリンク

## 公開後情報

Spotify、YouTubeなどの各エピソードURLは、手動更新を前提とした必須情報にしない。

自動取得・自動同期できる仕組みを実装した場合に、GitHub Pagesなどの表示層で追加する。

チャンネル・番組全体へのリンクは `links/` で管理する。

## Character

キャラクターの現在の設定は `characters/` をCanonical Sourceとする。

最初からすべての設定を固定せず、エピソードを通じて自然に生まれた性格・関係性・設定を必要に応じてCharacter Historyへ追加する。

設定追加時には、その設定が生まれたエピソードを記録する。

Git履歴そのものもキャラクター設定の変遷記録として扱う。

### Persona Maintenance

Character Profileは増やすこと自体を目的としない。

基本原則は **Personaは薄く、履歴は厚く** とする。

- Core Personalityは、そのキャラクターを演じるために必要な少数の強い原則に留める。
- Episodeで生まれた単発の冗談、反応、出来事は原則としてCharacter Historyに記録し、すぐにPersonaへ固定しない。
- 台本生成・Episode保存時には、新しい性格・関係性・世界認識が生まれた可能性がある場合のみCharacter Historyへの追記を検討する。変化がなければ更新しない。
- 同じ性質が複数Episodeで自然に繰り返される、今後その設定を知らないとキャラクターが不自然になる、恒常的な関係性として定着した、などの場合にPersonaへの昇格を検討する。
- 数Episodeごと、またはCharacter Historyがある程度蓄積した段階で履歴を見直し、定着した性質だけをPersonaへ昇格・整理する。
- 単発ネタをすべてPersona化して設定を肥大化させない。

Episode Historyはキャラクターがどのように育ったかを残す記録であり、すべてを毎回のロールプレイへ読み込ませるための設定集ではない。

## Update History

NEWSやCHANGELOGを手動で二重管理しない。

RepositoryのGit履歴を正式な更新履歴として扱う。

将来GitHub Pagesを作成する場合は、Git履歴からUPDATE表示を生成する。

## Workflow

基本フロー：

```text
壁打ち
↓
台本整形
↓
script.md + README.md生成
↓
KabeRadio Repositoryへ保存
↓
PC側でRepositoryを同期
↓
Amakawachan Radioでscript.mdを読み込み
↓
Podcast / Video Render
↓
公開
```

iPhoneのメモなどを中継地点として使用することは必須としない。

## Principle

> 自動化できない公開後情報は、原則としてMarkdownの必須項目にしない。

> Character Profileは増やすことを目的としない。Episode Historyを蓄積し、繰り返し現れる性質だけをPersonaへ昇格する。

> Repositoryの内容は、現在の可視性設定にかかわらず、常に公式サイトから公開可能な状態を保つ。

Repositoryを維持するための手作業を増やすより、台本とキャラクターの記録を残すことを優先する。
