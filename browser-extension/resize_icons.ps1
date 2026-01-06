
Add-Type -AssemblyName System.Drawing

$srcPath = "E:\xcode\openwrt-manager\browser-extension\.output\chrome-mv3\image (2).png"
$outputDir = "e:\xcode\openwrt-manager\browser-extension\public"

$sizes = @(16, 32, 48, 128)

try {
    $srcImage = [System.Drawing.Image]::FromFile($srcPath)
} catch {
    Write-Host "Error loading image: $_"
    exit 1
}

foreach ($size in $sizes) {
    $outFile = Join-Path $outputDir "icon-$size.png"
    
    $bitmap = New-Object System.Drawing.Bitmap $size, $size
    $graph = [System.Drawing.Graphics]::FromImage($bitmap)
    $graph.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graph.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graph.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

    $graph.DrawImage($srcImage, 0, 0, $size, $size)
    
    $bitmap.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Host "Generated $outFile"
    
    $bitmap.Dispose()
    $graph.Dispose()
}

$srcImage.Dispose()
