Add-Type -AssemblyName System.Drawing
$assetRoot=$PSScriptRoot
$manifest=Get-Content (Join-Path $assetRoot 'production-v2.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$cards=@()
$qa=@()
$sheet=[System.Drawing.Bitmap]::new(1500,2240)
$g=[System.Drawing.Graphics]::FromImage($sheet)
$g.Clear([System.Drawing.Color]::FromArgb(241,239,227))
$font=[System.Drawing.Font]::new('Yu Gothic',12)
$n=0
foreach($s in $manifest.stickers){
  $path=Join-Path $assetRoot ('output/'+$s.id+'.png')
  $img=[System.Drawing.Bitmap]::FromFile($path)
  $x=($n%5)*300;$y=[Math]::Floor($n/5)*280
  $g.DrawImage($img,[int]($x+20),[int]($y+6),260,225)
  $label=$s.id+' '+$s.text
  $g.DrawString($label,$font,[System.Drawing.Brushes]::Black,[single]($x+15),[single]($y+240))
  $alphaMin=255;$alphaMax=0
  for($py=0;$py -lt $img.Height;$py++){for($px=0;$px -lt $img.Width;$px++){$a=$img.GetPixel($px,$py).A;$alphaMin=[Math]::Min($alphaMin,$a);$alphaMax=[Math]::Max($alphaMax,$a)}}
  $qa += [pscustomobject]@{file=$s.id+'.png';width=$img.Width;height=$img.Height;bytes=(Get-Item $path).Length;alpha_min=$alphaMin;alpha_max=$alphaMax}
  $img.Dispose()
  $cards += '<figure><img src="output/'+$s.id+'.png" alt="'+$label+'"><figcaption>'+$label+'</figcaption></figure>'
  $n++
}
$sheet.Save((Join-Path $assetRoot 'contact-sheet.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$font.Dispose();$g.Dispose();$sheet.Dispose()
$html='<!doctype html><html lang="ja"><meta charset="utf-8"><title>壁ラジPOP Vol.1</title><style>body{font-family:system-ui;margin:24px;background:#f1efe3;color:#122d32}h1{margin-bottom:8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}figure{margin:0;padding:12px;background:#fff;border-radius:16px}img{width:100%;height:auto}figcaption{text-align:center;font-weight:bold}body.dark{background:#172b35;color:white}body.dark figure{background:#304754}button{padding:10px;margin:12px 0}</style><h1>壁ラジPOP Vol.1 — 40枚</h1><p>新版の制作画像。クリックで背景色を切り替え、文字と輪郭を見比べられます。</p><button onclick="document.body.classList.toggle(''dark'')">明るい背景 / 暗い背景</button><div class="grid">'+($cards -join "`n")+'</div><h2>メイン・タブ</h2><img style="width:240px" src="output/main.png"><img style="width:96px" src="output/tab.png"></html>'
Set-Content (Join-Path $assetRoot 'preview.html') $html -Encoding UTF8
foreach($id in @('main','tab')){
  $path=Join-Path $assetRoot ('output/'+$id+'.png')
  $img=[System.Drawing.Bitmap]::FromFile($path)
  $qa += [pscustomobject]@{file=$id+'.png';width=$img.Width;height=$img.Height;bytes=(Get-Item $path).Length;corner_alpha=$img.GetPixel(0,0).A;dpi=$img.HorizontalResolution}
  $img.Dispose()
}
$qa | ConvertTo-Json | Set-Content (Join-Path $assetRoot 'export-check.json') -Encoding UTF8
Compress-Archive -Path (Join-Path $assetRoot 'output/*.png') -DestinationPath (Join-Path $assetRoot 'kaberadio-pop-vol1-40.zip') -Force
