<?php
$m = new MongoClient();
$db=$m->ssad;
$collection=$db->rss;
session_start();
if($_POST['admin_link']=="admin_dash") header("Location: admin_dash.php");
if($_POST['query_link']=="query") header("Location: ./query.php");
if($_POST['new_user']=="new_user") header("Location: ./addUser.php");
if($_POST['Logout']=="logout")
{
        session_destroy();
        header("Location: ./index.php");
}
if($_SESSION['username']==NULL)
{
        $_SESSION['log']=2;
        header("Location: ./index.php");
}
if(!empty($_POST['SourceLink']))
{
	//print_r($_POST);
	//echo isset($_POST['SourceLink']);  //$_POST['SourceLink']
	//echo isset($_POST['CMP']);
	//print_r($_POST);
	$query=array("SourceLink" => $_POST['SourceLink']);

	$cursor = $collection->remove($query);
	//print_r($cursor);
	
	if($_POST["Curated"]==3)
		header("Location: ./curated.php");
	else if($_POST["Curated"]==1)
		header("Location: ./partial_curated.php"); 
	if($_POST["Curated"]==2)
		header("Location: ./fully_curated.php"); 
}
/*else
	header("Location: ./curated.php"); */ 
?>
