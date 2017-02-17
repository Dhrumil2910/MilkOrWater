<?php 
$m = new MongoClient();
$db=$m->ssad;
$collection=$db->rss;
session_start();
$cursor = NULL;
$doc = NULL;
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

	if($_POST['search']=="search")
{	
	
	if((empty($_POST['cname']) and empty($_POST['fname']) and  empty($_POST['aname'])))
	{
		$_SESSION['result'] = 3;
	}
	else
	{
		$query=array();
		if(!empty($_POST['cname']))
		{
			$regexObj = new MongoRegex("/.*" . $_POST['cname'] . ".*/i");
			$query1 = array("Company_Name" => array( '$regex' => $regexObj));
		}
		else
		{
			$regexObj = new MongoRegex("/.*/i"); 
			$query1= array("Company_Name" => array('$regex' => $regexObj));
		} 
		if(!empty($_POST['fname']))
		{
			$regexObj = new MongoRegex("/.*" . $_POST['fname'] . ".*/i");
			$query2 = array("FirmName" => array('$regex' => $regexObj));
		}
		else
		{	
			$regexObj = new MongoRegex("/.*/i"); 
			$query2 = array("FirmName"=>array('$regex' => $regexObj));
		}
		if(!empty($_POST['aname']))
		{
			list($fname, $lname) = explode(" ", $_POST['aname']);
		//	if( strlen($lname) == 0) //only fname or lname was given
			{
				$regexObj = new MongoRegex("/.*" . $fname . ".*/i");
				$query3 = array('$or' => array(array("Analyst F name" => array('$regex' => $regexObj)), array("Analyst_last_name" =>array('$regex' => $regexObj ))));
			}

		}
		else
		{
			$regexObj = new MongoRegex("/.*/i"); 
			$query3= array("Analyst F name"=>array('$regex' => $regexObj));
		}
		//$query = array("Company_Name"=>$query1["Company_Name"], "FirmName"=>$query2["FirmName"], '$or' => $query3['$or']);
		$query = array_merge($query1, $query2, $query3);
		//print_r($query);
		$cursor = $collection->find($query, array("_id" => false)); //, "Company_Name" => true, "Horizon" => true, "CMP" => true, "TP" => true, "SourceLink" => true , "Headline" => true));
		$arr_list = iterator_to_array($cursor);
		$_SESSION["list"] = $cursor;
		if(sizeof($arr_list) == 0)	
		{
			$_SESSION["result"] = 2;
		}	
		else
		{
			$_SESSION["result"] = 1;
		}
		
	}	
}




?>
<!DOCTYPE html>  
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Admin Login Portal</title>

    <!-- Bootstrap core CSS -->
    <link href="bootstrap-3.0.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="bootstrap-3.0.0/examples/jumbotron/jumbotron.css" rel="stylesheet">
    <!--link href="bootstrap-3.0.0/examples/sticky-footer-navbar/sticky-footer-navbar.css" rel="stylesheet"-->
    <!-- Custom styles for signin template -->
    <link href="bootstrap-3.0.0/customs/footer.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="bootstrap-3.0.0/assets/js/ie-emulation-modes-warning.js"></script>
   <link href="bootstrap-3.0.0/font-awesome-4.1.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
 
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <style>
      .headline:hover, .headline:link {
	      text-decoration: none;
      }
    </style>
  </head>

  <body>

  <!--  Page Header  -->
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand">MILKorWATER</a>
        </div>
        <div class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" method="post" role="form">
            <button type="submit" class="btn btn-success" name="admin_link" title="User Interface" value="admin_dash">Dashboard</button>
            <button type="submit" class="btn btn-primary" name="query_link" title="Query on databse" value="query">
	      <i class="glyphicon glyphicon-search"></i></button>
            <button type="submit" class="btn btn-primary" name="new_user" title="Create new users" value="new_user">
	      <img src="bootstrap-3.0.0/img/new_user.png" style="width:20px; height:20px;"></button>
	    <p class="navbar-text navbar-right" style="line-height:0;"><?php echo $_SESSION['username']?></p> 
	    <button type="submit" name="Logout" value="logout" id="logstatus" title="Logout" class="btn btn-default">
	      <i class="glyphicon glyphicon-log-out"></i></button>
          </form>
        </div><!--/.navbar-collapse -->
    </nav>
 <!--  Page Header Complete  -->

  <!--  Jumbotron  -->
    <div class="jumbotron">
      <div class="container">
        <p style="color:#888;">Enter one or more fields to perform a search</p>
        <div class="row">
          <div class="col-lg-6">
       	    <form method="POST" role="form">
	      <input type="text" style="width:50%" name="cname" autofocus="autofocus" class="form-control" placeholder="Company Name">
       	      <input type="text" style="width:50%" name="fname" class="form-control" placeholder="FirmName">
       	      <input type="text" style="width:50%" name="aname" class="form-control" placeholder="Analyst Name">
      	      <button class="btn btn-primary" name="search" value="search" type="submit">Search</button>
	      <!--img src="bootstrap-3.0.0/img/searchbutton.jpeg" height="100px; width:150px;"/-->
      	    </form><!-- /input-group -->
       	  </div><!-- /.col-lg-6 -->
        </div><!--row-->				    
      </div><!--container-->
    </div><!--Jumbotron-->
       <div class="container">
	<?php if($_SESSION["result"] == 3): 
		$_SESSION["result"] = -1;
 	?>
          <div class="alert alert-danger alert-error" id="alert_noresult">
	    <a href="#" class="close" data-dismiss="alert">&times</a> 
	    <strong>Error! </strong>Please fill at least one of the fields.
	  </div>
	  <script>
            $('#alert_noresult').css('opacity', 1);
	  </script>
	  <?php elseif($_SESSION["result"] == 2): 
	    $_SESSION["result"] = -1;
	  ?>
          <div class="alert alert-warning" id="alert_nofield">
	    <a href="#" class="close" data-dismiss="alert">&times</a> 
	    <strong>Alert! </strong>No results were found for this query.
	  </div>
	  <script>
            $('#alert_nofield').css('opacity', 1);
	  </script>
	  <?php endif; ?>
        </div>
    
    <?php
	  if($_SESSION["result"] == 1): 
	  	
       		echo "<div class='jumbotron'><div class='container resultcont' id='results'>";
		echo "<h1>Results</h1><br>";
		$item_list1 = array("TP", "CMP");
		$item_list2 = array("Company_Name", "Horizon", "FirmName", "Sector", "Industry", "RecoAction_Mow");
		foreach($arr_list as $doc)
		{

			echo "<h2><a class='headline' href='" . $doc["SourceLink"] ."'>" .  $doc["Headline"] . "</a></h2><hr>";
			if( !empty($doc["CMP"]) and $doc["CMP"][0] != "$")
			{
				$doc["CMP"] = "$" . $doc["CMP"];
			}
			if(!empty($doc["TP"]) and $doc["TP"][0] != "$")
			{
				$doc["TP"] = "$" . $doc["TP"];
			}
			/* foreach($doc as $key => $value) 
			{
				if($key != "Headline" and $key!="SourceLink" and !empty($value)) 
				{
					if($key == "CMP")
					{
						echo "<p>" . "<mark style='background-color:#b0c4de;'>" . $key . " : " . $value . "</mark></p>";
					}
					else 
					{
						echo "<p>" . $key . " : " . $value . "</p>";
					}
				}
			}*/
			foreach($item_list1 as $item) 
			{
					
					/*if($item == "CMP")
					{
						echo "<p>" . "<mark style='background-color:#b0c4de;'>" . $item . " : " . $doc[$item] . "</mark></p>";
					}*/
					if( !empty($doc[$item]))
					{
					
						echo "<p>" . $item . " : " . $doc[$item] . "</p>";
					}
					
			}
			$i = 1;
			echo "<div class='dropdown'>";
			echo "<a href='#' class='headline' data-toggle='dropdown' class='dropdown-toggle'> More<b class='caret'></b></a>";
			echo "<ul class='dropdown-menu'>";
			$i += 1;
			foreach($item_list2  as $item)
			{	
				echo "<li style='padding-left: 5px;padding-right:5px'><p>" . (($item == "RecoAction_Mow") ? 'MoW Recommendation' : $item) . " : " . $doc[$item] . "</p></li>";
			}
			echo "</ul></div><br>";

				
		}
		echo "</div></div>";


		$_SESSION["result"] = NULL;
	?> 
	<?php elseif($_SESSION["result"] == 2): 
		$_SESSION["result"] = NULL;
	?>
	<?php endif; ?>
  <!--  Jumbotron Complete  -->


  <!-- Sticky Footer  -->
    <div class="footer">
      <div class="container">
	    <div class="pull-left"><p>&copy; 2014 MilkorWater</p></div>
	    <div class="pull-right"><p>Build: 1.0 Rev 3933 </p></div>
      </div>
    </div>
  <!-- Footer Complete  -->

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="./bootstrap-3.0.0/dist/js/1.11.1_jquery.min.js"></script>
    <script src="./bootstrap-3.0.0/dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="./bootstrap-3.0.0/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
<script>
console.log(<?php echo $_SESSION['log']; echo $_SESSION['message'];?>)
console.log("<?php echo $_SESSION['username'];?>")
console.log(<?php echo $_SESSION['result']; ?>)
</script>
