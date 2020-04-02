<?php
$list = scandir(__DIR__);
$list = array_filter($list, function($v){
   return stripos($v, '.htm') !== false;
});

array_walk($list,function(&$v){
    $v = str_replace(['.html', '.htm'], '', $v);
});

echo json_encode(array_values($list));