$files = @("lang-zh-CN.ab3e4ec6.js", "lang-zh-CN-legacy.14052c67.js", "lang-zh-TW.4c287017.js", "lang-zh-TW-legacy.c5cdb6ce.js")
$keys = @("dashboard.analysis.market.CNETF", "dashboard.analysis.market.CNE", "aiAssetAnalysis.opportunities.market.CNETF", "aiAssetAnalysis.opportunities.market.CNE", "dashboard.analysis.market.CNStock")
$results = foreach ($f in $files) {
    if (Test-Path $f) {
        $content = [System.IO.File]::ReadAllText((Resolve-Path $f).Path)
        $obj = New-Object PSObject
        $obj | Add-Member NoteProperty File $f
        foreach ($k in $keys) {
            $obj | Add-Member NoteProperty $k ($content.Contains($k))
        }
        $obj
    }
}
$results | Format-Table -AutoSize
