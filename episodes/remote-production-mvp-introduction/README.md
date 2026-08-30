# 一度だけ作って、あとは届ける

Amakawachan Radioへ追加したRemote Production MVPを紹介しながら、実際の非GUI RenderとDeliveryを確認する短い実証実験回です。

## Cast

- Host
- Guest

## Script

[台本を読む](script.md)

## Verification

このepisodeで次の経路を確認します。

```text
KabeRadio script.md
→ RemoteRadio CLI
→ Podcast Render
→ Video Render
→ M6 Local Archive
→ iCloud ReadyToPublish
```

Render前は`production.json`の`status`を`ready`にします。
