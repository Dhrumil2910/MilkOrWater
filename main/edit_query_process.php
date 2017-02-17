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
if(!empty($_POST['Curated']))
{
	//print_r($_POST);
	//echo isset($_POST['SourceLink']);  //$_POST['SourceLink']
	//echo isset($_POST['CMP']);
	$query=array("SourceLink" => $_POST['SourceLink']);
	//print_r($query);
	$cursor = $collection->update($query,array('$set' => array("TP" => $_POST['TP'], "CMP" => $_POST['CMP'], "Company_Name" => $_POST['Company_Name'], "TICKER" => $_POST['TICKER'],  "FirmName" => $_POST['FirmName'], "Sector" => $_POST['Sector'], "Industry" => $_POST['Industry'], "RecoAction_orig" => $_POST['RecoAction_orig'], "RecoAction_Mow" => $_POST['RecoAction_Mow'], "Analyst F name" => $_POST['Analyst_F_name'], "Analyst L name" => $_POST['Analyst_L_name'], "Analyst tc" => $_POST['Analyst_tc'], "Analyst email" => $_POST['Analyst_email'], "Horizon" => $_POST['Horizon'], "notes" => $_POST['notes'], "Status" => $_POST['Status'], "Curated" =>(int)$_POST['Curated'] ))); //or die ("Some error Occurred");
	//print_r($cursor);
	//$arr = iterator_to_array($cursor);
	//print_r($_POST);
	if($_POST["Curated"]==3)
		header("Location: ./curated.php");
	else if($_POST["Curated"]==1)
		header("Location: ./partial_curated.php"); 
	if($_POST["Curated"]==2)
		header("Location: ./fully_curated.php");
}
//else
//	header("Location: ./curated.php"); */
?>
