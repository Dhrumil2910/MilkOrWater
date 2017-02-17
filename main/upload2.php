<?php
session_start();
ini_set('display_errors','On');
error_reporting(E_ALL);
if (!($_FILES["new_file"]["error"] > 0)) {
	$allowedExt = array("csv");
	$temp = explode(".", $_FILES["new_file"]["name"]);
	$extension = end($temp);
	if (($_FILES["new_file"]["type"] == "text/csv") && in_array($extension, $allowedExt))
	{
// case does not exists	if (file_exists("upload/" . $_FILES["new_file"]["name"])) {
//			echo $_FILES["file"]["name"] . " already exists. ";
//		} 
		$s= move_uploaded_file($_FILES["new_file"]["tmp_name"],"./". $_FILES["new_file"]["name"]);
		$s=1;

		if($s==1)
		{
			$game = exec("mongoimport --db ssad --collection company --type csv --headerline --file ./" . $_FILES["new_file"]["name"]);
			$_SESSION['error']=3;
		}
		else if($s==0)
			$_SESSION['error']=2;
	}
	else {
//		echo $_FILES["new_file"]["type"] == "text/csv";
//		echo "invalid file";
		$_SESSION['error']=1;
	}
}
else $_SESSION['error']=$_FILES["new_file"]["error"];
header("location:./upload_csv.php");
?> 
