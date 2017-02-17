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
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Fully Curated</title>

    <!-- Bootstrap Core CSS -->
    <link href="bootstrap-3.0.0/dist/css/bootstrap.3.2.min.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="bootstrap-3.0.0/dist/css/sb-admin.css" rel="stylesheet">
    <!-- Morris Charts CSS -->
    <link href="bootstrap-3.0.0/dist/css/plugins/morris.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/customs/upload.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="bootstrap-3.0.0/font-awesome-4.1.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href="bootstrap-3.0.0/customs/footer.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            <!-- Brand and toggle get grouped for better mobile display -->
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

            <!-- Sidebar Menu Items - These collapse to the responsive navigation menu on small screens -->
            <div class="collapse navbar-collapse navbar-ex1-collapse">
                <ul class="nav navbar-nav side-nav">
                    <li>
                        <a href="admin_dash.php"><i class="fa fa-fw fa-dashboard"></i> Dashboard</a>
                    </li>
                    <li>
                        <a href="upload_csv.php"><i class="fa fa-fw fa-file"></i> Upload CSV File</a>
                    </li>
                    <li>
                        <a href="curated.php"><i class="fa fa-fw fa-file"></i>Non Curated</a>
                    </li>
                    <li>
                        <a href="partial_curated.php"><i class="fa fa-fw fa-file"></i>Partially Curated</a>
                    </li>
                    <li class="active">
                        <a style="background-color:#080808;" href="fully_curated.php"><i class="fa fa-fw fa-file"></i>Fully Curated</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </nav>
       <div id="page-wrapper">

            <div class="container-fluid">

                <!-- Page Heading -->
                <div class="row">
		  <div class="col-lg-12">
                        <h1 class="page-header">
                           	Curated Feeds
                            <small>Showing The finished work </small>
                        </h1>

		
			<?php
		//	$page  = isset($_GET['page']) ? (int) $_GET['page'] : 1;
			if(empty($_GET['page']))
				$_GET['page'] = 1;
			$page=$_GET['page'];
			$limit = 10;
			$skip  = ($page - 1) * $limit;
			$next  = ($page + 1);
			$prev  = ($page - 1);?> 


                        <ol class="breadcrumb">
                            <li>
                                <i class="fa fa-dashboard"></i>  <a href="admin_dash.php">Dashboard</a>
                            </li>
                            <li class="active">
                                <i class="glyphicon glyphicon-upload"></i> ShowFiles
                            </li>
                        </ol>
                    </div>

                </div>
                <!-- /.row -->
<?php
			$query= array("Curated" => 2); //3=>Non-Curated
			$cursor = $collection->find($query, array("_id" => false));
//			print_r($cursor);
//			echo "<br>-----------------------------------------------------<br>";
			$arr_list = iterator_to_array($cursor);
			$total =  (sizeof($arr_list));
//			print_r($arr_list);
			echo "<div class='jumbotron'>
					<div class='container resultcont' id='results'>";
			echo "<h1>Results</h1><br>";
			echo "<h2>".$skip.'-'.$limit*$page."</h2>";
			$item_list1 = array("TP", "CMP", "Date");
			$item_list2 = array("Company_Name", "Sector", "Industry", "FirmName", "Analyst F name", "Analyst L name", "RecoAction_Mow",  "Curated", "Horizon");
			$item_list3 = array("TICKER", "Analyst tc", "Analyst email", "RecoAction_orig", "RecoType_orig", "RecoType_Mow", "Headline", "notes", "Status", "Raw", "SourceLink");

			$count =0;
			//echo $page.'\n';
			if($page >= 1 && $page*$limit < $total)
			{
				echo '<button class="active"> <a href="?page=' . $prev . '">Previous </a> </button>';
				echo ' <button class="active"> <a href="?page=' . $next . '">Next </a> </button>';
			}

			else
				echo '<button class="active"> <a href="?page=' . $prev . '">Previous </a> </button>';			

			foreach($arr_list as $doc)
			{
//				print_r($doc);

				$count++;

				if($count < $skip +1)
					continue;

				if($count > $skip + $limit)
					break;

//				print_r($doc);
				echo "<h2><a class='headline' href='" . $doc["SourceLink"] ."'>" .  $doc["Headline"] . "</a></h2><hr>";
				if( !empty($doc["CMP"]) and $doc["CMP"][0] != "$")
				{
					$doc["CMP"] = "$" . $doc["CMP"];
				}
				if(!empty($doc["PriceTarget"]) and $doc["PriceTarget"][0] != "$")
				{
					$doc["PriceTarget"] = "$" . $doc["PriceTarget"];
				}
				echo "<form method='post' action='edit_query.php'>";
				foreach($item_list1 as $item) 
				{
					if( !empty($doc[$item]))
					{
						echo "<p>" . $item . " : " . $doc[$item] . "</p>";
					}
					echo "<input type='hidden' name='" . $item . "' value='" . $doc[$item] . "'/>";
				}
				$i = 1;
				echo "<div class='dropdown'>";
				echo "<a href='#' class='headline' data-toggle='dropdown' class='dropdown-toggle'> More<b class='caret'></b></a>";
				echo "<ul class='dropdown-menu'>";
				$i += 1;
				foreach($item_list2  as $item)	// display on dropdown
				{	
					echo "<li style='padding-left: 5px;padding-right:5px'><p>" . (($item == "Reco_action_mow") ? 'MoW Recommendation' : $item) . " : " . (($doc[$item] == "Curated") ? 'No' : $doc[$item]) . "</p></li>";
					echo "<input type='hidden' name='" . $item . "' value='" . $doc[$item] . "'/>";
				}
				echo "</ul>";
				foreach($item_list3 as $item)	// not for display. just to pass
				{
					 if($item == "Raw")
					{
						for($i = 0; $i<strlen($doc[$item]); $i++)  
						{
							if($doc[$item][$i] == "'")
								 $doc[$item][$i] = '"';
						}
					}
					echo"<input type='hidden' name='" . $item . "' value= '" . $doc[$item] . "' />";
				}
			echo "<input type=submit value='Edit' /></div><br>";
				echo "</form>";
			}
		
		echo "<br><br><br></div></div>";
?>

		</div>
            <!-- /.container-fluid -->
 
        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->

         <!-- Sticky Footer  -->
    <div class="footer">
      <div class="container">
            <div class="pull-left"><p>&copy; 2014 MilkorWater</p></div>
            <div class="pull-right"><p>Build: 1.0 Rev 3933 </p></div>
      </div>
    </div>
  <!-- Footer Complete  -->


    <!-- jQuery Version 1.11.0 -->
    <script src="bootstrap-3.0.0/dist/js/jquery-1.11.0.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="bootstrap-3.0.0/dist/js/bootstrap.min.js"></script>

    <!-- Morris Charts JavaScript -->
    <script src="bootstrap-3.0.0/dist/js/plugins/morris/raphael.min.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/morris/morris.min.js"></script>
    <script src="bootstrap-3.0.0/dist/js/plugins/morris/morris-data.js"></script>
    <script src="bootstrap-3.0.0/customs/upload.js"></script>

</body>

</html>
 
