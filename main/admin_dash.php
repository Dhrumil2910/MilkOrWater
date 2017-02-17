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

    <title>Admin Dashboard</title>

    <!-- Bootstrap Core CSS -->
    <link href="bootstrap-3.0.0/dist/css/bootstrap.3.2.min.css" rel="stylesheet">
    <link href="bootstrap-3.0.0/dist/css/bootstrap-theme.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="bootstrap-3.0.0/dist/css/sb-admin.css" rel="stylesheet">
    <!-- Morris Charts CSS -->
    <link href="bootstrap-3.0.0/dist/css/plugins/morris.css" rel="stylesheet">

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
                    <li class="active">
                        <a style="background-color:#080808;" href="admin_dash.php"><i class="fa fa-fw fa-dashboard"></i> Dashboard</a>
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
                    <li>
                        <a href="fully_curated.php"><i class="fa fa-fw fa-file"></i>Fully Curated</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </nav>

        <div id="page-wrapper">

            <div class="container-fluid">

                <div class="row">
                    <div class="col-lg-12">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h3 class="panel-title"><i class="glyphicon glyphicon-comment"></i>&nbsp&nbspHeadlines</h3>
                            </div>
                            <div class="panel-body">
                                <div class="list-group">
				    <?php
				       $m = new MongoClient();
				       $db = $m->ssad;
				       $col = $db->rss;
				       $cursor = $col->find();
				       $arr_list = iterator_to_array($cursor);
				       $length = sizeof($arr_list) -10;
				       $count = 0;
				       $count1 = 0;	
						
				       foreach($arr_list as $doc)
					{

					 if($count < $length)
						{
							$count++;
							continue;
						}
					

                                   	  echo "<a href='". $doc["SourceLink"] . "' class='list-group-item'>";
                                          echo "<span class='badge'>" . $doc["Company_Name"] . "</span>";
					  echo "<span class='badge'>" . $doc["FirmName"] . "</span>";
                                          echo "<i class='glyphicon glyphicon-info-sign'></i>" ."  " .$doc["Headline"] . "</a>";
					}
				     ?>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-12">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h3 class="panel-title"><i class="glyphicon glyphicon-usd"></i> Price Targets</h3>
                            </div>
                            <div class="panel-body">
                                <div class="table-responsive">
                                    <table class="table table-bordered table-hover table-striped">
                                        <thead>
                                            <tr>
                                                <th>Company Name</th>
                                                <th>Sector</th>
                                                <th>Price Target</th>
						<th>Date</th>
						<th>FirmName</th>				
                                            </tr>
                                        </thead>
                                        <tbody>
					    <?php 
					    foreach($arr_list as $doc)
					    {
						if($count1 < $length)
						{
							$count1++;
							continue;
						}
						
						if(!empty($doc["TP"])) 
						{
							//if(!$doc[""][0] == "$")
						//	{
								$doc["PriceTarget"] = "$" . $doc["PriceTarget"];
						//	}
                                           		echo "<tr>";
                                            	echo "<td><i class='fa fa-forward'></i>" . "  ". $doc["Company_Name"] . "</td>";
                                           		echo "<td>" . $doc["Sector"] . "</td>";
                                            		echo "<td>" . $doc["TP"] . "</td>";
							echo "<td>" . $doc["Date"] . "</td>";
                                            		echo "<td>" . $doc["FirmName"] . "</td>";
                                            		echo "</tr>";
						}
					    }
					    ?>

                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- /.row -->

            </div>
            <!-- /.container-fluid -->
 
        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->

         <!-- Sticky Footer  -->
    <div class="footer">
      <div class="container">
	    <p class="divider" style="background-color:black;"></p>
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

</body>

</html>
