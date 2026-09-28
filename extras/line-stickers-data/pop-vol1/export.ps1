Add-Type -AssemblyName System.Drawing
$assetRoot = $PSScriptRoot
$files = Get-ChildItem (Join-Path $assetRoot 'originals') -Filter '*.png' | Where-Object {$_.BaseName -match '^(\d{2}|main|tab)$'}
foreach ($file in $files) {
  $w=370; $h=320; $margin=12
  if ($file.BaseName -eq 'main') {$w=240; $h=240; $margin=8}
  if ($file.BaseName -eq 'tab') {$w=96; $h=74; $margin=4}
  $src=[System.Drawing.Image]::FromFile($file.FullName)
  $dst=[System.Drawing.Bitmap]::new($w,$h)
  $dst.SetResolution(96,96)
  $g=[System.Drawing.Graphics]::FromImage($dst)
  $g.Clear([System.Drawing.Color]::Transparent)
  $g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $scale=[Math]::Min(($w-2*$margin)/$src.Width,($h-2*$margin)/$src.Height)
  $dw=[int]($src.Width*$scale);$dh=[int]($src.Height*$scale)
  $g.DrawImage($src,[int](($w-$dw)/2),[int](($h-$dh)/2),$dw,$dh)
  $dst.Save((Join-Path $assetRoot ('output/'+$file.Name)),[System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose();$dst.Dispose();$src.Dispose()
}

