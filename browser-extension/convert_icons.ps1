
Add-Type -AssemblyName System.Drawing

$icoPath = "E:\xcode\openwrt-manager\favicon_io\2vqp8-p3fth-001.ico"
$outputDir = "e:\xcode\openwrt-manager\browser-extension\public"

$sizes = @(16, 32, 48, 128)

try {
    $icon = [System.Drawing.Icon]::ExtractAssociatedIcon($icoPath)
    # Note: ExtractAssociatedIcon might behave differently than reading bytes. 
    # Let's try reading specifically.
    $icon = new-object System.Drawing.Icon $icoPath
} catch {
    Write-Host "Error loading icon: $_"
    exit 1
}

foreach ($size in $sizes) {
    $outFile = Join-Path $outputDir "icon-$size.png"
    
    # Create empty bitmap
    $bitmap = New-Object System.Drawing.Bitmap $size, $size
    $graph = [System.Drawing.Graphics]::FromImage($bitmap)
    $graph.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    
    # Scan for best matching size in ICO (naive approach: just resize largest)
    # For a perfect extraction we'd loop icon.ToBitmap() but ICO handling in .NET basic shim is tricky.
    # We will resize the main icon image to target size.
    
    $graph.DrawIcon($icon, 0, 0, $size, $size)
    
    $bitmap.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Host "Generated $outFile"
    
    $bitmap.Dispose()
    $graph.Dispose()
}

$icon.Dispose()
