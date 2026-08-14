# KabeRadio Operations

## 基本方針

KabeRadio Repositoryは、壁ラジの公式アーカイブおよび将来の公式サイト用Canonical Sourceとして管理する。

運用上の手作業を可能な限り増やさない。

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

Repositoryを維持するための手作業を増やすより、台本とキャラクターの記録を残すことを優先する。
