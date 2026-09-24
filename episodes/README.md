# EPISODES

壁ラジの正式Episode一覧です。

## Episode Package

現在の正式な保存単位は次です。

```text
episodes/<episode-key>/
├─ README.md
├─ script.md
└─ production.json
```

- `README.md`: 人が読むEpisode案内とCast
- `script.md`: Amakawachan Radioへ渡すCanonical Script
- `production.json`: Remote Productionの制作入力、初期Casting、公開状態

GitHub上の正式Episodeは原則`status: ready`で保存し、M6ローカルでRenderした制作状態とは分離します。

詳細:

- [ChatGPTから正式台本を保存する手順](../docs/chatgpt-episode-package-workflow-v1.md)
- [Runtime Integration Contract](../docs/runtime-integration-contract-v1.md)

## Episodes

- [知ってるAIと、やってた人間](ai-knows-but-didnt-live-it/)
- [モブ子の一言をnoteに載せたかっただけなのに、ジェネレーターが生えた](note-card-generator-grew/)
- [秋風のチューニング アフタートーク](autumn-opening-aftertalk/)
- [終わらない部室](endless-clubroom/)
- [未来の話をしたら、だいたいもう実装されてた](it-was-already-implemented/)
- [ミニキャラを出したら、踊り始めた](petite-live-arrives/)
- [終わるはずだったのに、ミニキャラをBPM同期したくなった](petite-live-beat-sync/)
- [ショートの時代に、ショートを狙いすぎない](shorts-strategy-meeting/)
- [体調で変わる、シャワーの締め方](shower-cooldown-routine/)
- [ASMRを作ろうとしたら空間音響スタジオになりそうな件](spatial-audio-studio/)
- [24時間、喋ることになりました](wallradio24-launch/)
- [本編が一番過疎なので、深夜ラジオに戻します](late-night-radio-reframe/)
- [壁ラジ、また機能が増えました](wallradio-feature-update-eyecatch-stickers/)
- [自分のキャラクターがスタンプになった](line-stickers-vol1-complete/)
- [Telegramから壁ラジ制作を呼び出せるようになりました](telegram-remote-production-introduction/)
- [AIが賢くなったら、人間が試され始めた](ai-prompt-engineering-reversal/)
- [一度だけ作って、あとは届ける](remote-production-mvp-introduction/)
- [Remote Production Casting Validation](remote-production-casting-validation/)
- [Remote Production Smoke](remote-production-smoke/)
- [この人なに？](kono-hito-nani/)
- [こうして深夜の壁打ちは終わらない](koushite-shinya-no-kabeuchi-wa-owaranai/)
- [なんか今日、違わない？](nanka-kyou-chigawanai/)
- [それ本人に聞かれます](sore-honnin-ni-kikaremasu/)

キャラクター主体回やアフタートークも、同じEpisode Package契約で記録します。
