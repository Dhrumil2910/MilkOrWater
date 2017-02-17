<?php
session_start();
ini_set('display_errors','On');
error_reporting(E_ALL);

if (!($_FILES["new_file"]["error"][0] && $_FILES["new_file"]["error"][1] && $_FILES["new_file"]["error"][2]  > 0)) {
	//$allowedExt = array("csv");
	//$temp = explode(".", $_FILES["new_file"]["name"]);
	//$extension = end($temp);
	 $_SESSION['error']=$_FILES["new_file"]["error"][0];
	if (($_FILES["new_file"]["type"][0] == "text/csv" && $_FILES["new_file"]["type"][1] == "text/csv" && $_FILES["new_file"]["type"][2] == "text/csv"))
	{
// case does not exists	if (file_exists("upload/" . $_FILES["new_file"]["name"])) {
//			echo $_FILES["file"]["name"] . " already exists. ";
//		} 

		//$s1 = str_replace(".csv", "1.csv", $_FILES["new_file"]["name"]);
		//echo $s1;		

		$s= move_uploaded_file($_FILES["new_file"]["tmp_name"][0],"./". $_FILES["new_file"]["name"][0]);
		$s1= move_uploaded_file($_FILES["new_file"]["tmp_name"][1],"./". $_FILES["new_file"]["name"][1]);
		$s2= move_uploaded_file($_FILES["new_file"]["tmp_name"][2],"./". $_FILES["new_file"]["name"][2]);
		//$s=1;

//		echo $s;
//		echo $s1;
//		echo $s2;

		//echo str_replace("world", "Dolly", "Hello world!");

		$counter = 0;
		$flag = 0;
		
		

		if(!strpos($_FILES["new_file"]["name"][0], "1.csv"))
		{
			if(!strpos($_FILES["new_file"]["name"][0], "2.csv"))
				$rss = $_FILES["new_file"]["name"][0];
			

			else
				$firm_company = $_FILES["new_file"]["name"][0];
		}

		else
			$firm = $_FILES["new_file"]["name"][0];

		
		if(!strpos($_FILES["new_file"]["name"][1], "1.csv"))
		{
			if(!strpos($_FILES["new_file"]["name"][1], "2.csv"))
				$rss = $_FILES["new_file"]["name"][1];
			

			else
				$firm_company = $_FILES["new_file"]["name"][1];
		}

		else
			$firm = $_FILES["new_file"]["name"][1];


		if(!strpos($_FILES["new_file"]["name"][2], "1.csv"))
		{
			if(!strpos($_FILES["new_file"]["name"][2], "2.csv"))
				$rss = $_FILES["new_file"]["name"][2];
			

			else
				$firm_company = $_FILES["new_file"]["name"][2];
		}

		else
			$firm = $_FILES["new_file"]["name"][2];
			

}}
		if(isset($rss) && isset($firm) && isset($firm_company))
		{
			$game = exec("mongoimport --db ssad --collection rss --type csv --headerline --file ./" . $rss);
			$game1 = exec("mongoimport --db ssad --collection firm --type csv --headerline --upsert --upsertFields FirmName --file ./" .   $firm);
			$game2 = exec("mongoimport --db ssad --collection firm_company --type csv --headerline --upsert --upsertFields Company_Name,FirmName  --file ./" . $firm_company);
		//	echo $game1;
		//	echo $game2;
		//	print_r($_FILES);
			$_SESSION['error']=3;

	        }
		else 
			$_SESSION['error']=1;
	

//else $_SESSION['error']=$_FILES["new_file"]["error"][0];
header("location:./upload_csv.php"); 
?> 
