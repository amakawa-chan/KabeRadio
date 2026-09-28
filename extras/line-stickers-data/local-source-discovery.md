# 既存スタンプのローカル制作データ発見

2026-09-28。過去Codex worktreeとDocumentsを検索。原本は変更せず、照合用データだけ本repoへ抽出。

## 日常・体調編40枚（スクリーンショットA相当）

原本: `C:/Users/naritake/.codex/worktrees/c2a2/kawaii-assistant/output/stickers/daily-health-final-v2/`

- manifest.json: 40枚の文言、キャラ、ポーズ、生成・修正プロンプト、原稿パス。
- source/: 原稿とmanifest。
- files/: 入稿PNG。
- daily-health-40-LINE.zip: 40枚＋main＋tab。
- preview-1.png / preview-2.png: 一覧。
- build.py / prepare.py / validation.json: 制作処理と過去の検証記録。
- READMEには36「いいね」を「やだやだやだー！」へ差し替えた記録あり。旧版を重複確認の正本にしない。

抽出: [recovered-daily-health.json](recovered-daily-health.json)

## 掛け合い編40枚（スクリーンショットB相当）

制作元: `C:/Users/naritake/Documents/kawaii-assistant/kaberadio-line-stickers/source/astra-new-concept-20260907/approved-pop-series/`

入稿データ: `C:/Users/naritake/Documents/kawaii-assistant/kaberadio-line-stickers/output/submission/kaberadio-pop-20260910/`

- order-and-provenance.json: 表示順、固定管理ID、文言、元画像、出力名、SHA256。
- kaberadio-pop-40.zip、files/、transparent-source/、preview.html、validation.json。
- 制作元にall-40-review.md、display-order.json、batch別プロンプトと画像。

抽出: [recovered-dialogue-order.json](recovered-dialogue-order.json)

## 旧読み取りの訂正

B11 そのうち慣れますよ、15 それ、結構気に入ってる、16 でも楽しそうでしたよ、17 ちょっと思いついたんですけど、18 試してみよっか、20 でも便利そうですよ、23 優先順位は大事です、24 そこは後回しで、26 今、頭の中で整理してる、27 それはちょっと見たい、31 聞かれなかったので、32 気のせいです、34 あ、じゃないんよ、35 そういう話じゃない、36 便利で済ませるな、38 本当に分かった？、39 一回回復したのに。

これらは制作・入稿台帳上の文言。販売中ファイルとの完全同一性やVol.1/2との正式対応は別途確認対象。旧スクリーンショット復元は出典として保持する。

POP設計への影響: 22「それでいこ！」のB34との類似指摘は撤回（B34は「あ、じゃないんよ」）。37「全員そろった」はB28「全員いますね」と引き続き類似。未確定13件は制作台帳で補完可能となった。画像生成前にこの抽出データを優先して照合する。
