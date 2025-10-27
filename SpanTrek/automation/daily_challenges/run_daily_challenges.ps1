# PowerShell script to run daily challenges creation
# This script provides better error handling and logging

$projectPath = "d:\Wojtek\SpanTrek\SpanTrek"
$logFile = "d:\Wojtek\SpanTrek\SpanTrek\automation\daily_challenges\daily_challenges.log"

try {
    # Change to project directory
    Set-Location $projectPath
    
    # Run the Django management command
    $output = python manage.py create_daily_challenges 2>&1
    
    # Log successful execution
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "$timestamp - SUCCESS: $output"
    
    Write-Host "Daily challenges created successfully at $timestamp"
    
} catch {
    # Log any errors
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $errorMsg = $_.Exception.Message
    Add-Content -Path $logFile -Value "$timestamp - ERROR: $errorMsg"
    
    Write-Error "Failed to create daily challenges: $errorMsg"
    exit 1
}