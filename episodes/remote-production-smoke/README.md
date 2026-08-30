# Remote Production Smoke Test

Amakawachan RadioのRemote Production Pipelineを、GUI操作なしで確認するための短い検証回です。

このepisodeは次の経路を確認します。

```text
KabeRadio script.md
→ RemoteRadio CLI
→ Podcast Render
→ Video Render
→ Local Archive
→ ReadyToPublish Delivery
```

## Cast

- Host
- Guest

## Script

[台本を読む](script.md)

## Production

`production.json`の`status`が`ready`の間だけ、新規Render対象として検出されます。
