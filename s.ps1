param([int] $a,[int] $b,[int] $c,[int] $d)
If($c -eq 0){$t = Get-Content .\l
}
else{$t = Get-Content c:\windows\temp\l
}
if($b -eq 0){
   if($t.length -lt $a){
        sleep $d
   }
}
else{
   if($t.length -eq $a){
        sleep $d
   }   
}